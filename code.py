import pandas as pd
import tweepy
from io import BytesIO
from PIL import Image
import requests
import json
import os
import re
from collections import Counter
from stop_words import get_stop_words
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from wordcloud import STOPWORDS
from google.cloud import storage
import numpy as np
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

#9 cambiar azul a azul francia 
#10 achicar logo

################### Authenticate with Twitter API
consumer_key = [CONSUMER_KEY]
consumer_secret = [CONSUMER_SECRET_KEY]
access_token = [ACCESS_TOKEN]
access_token_secret = [ACCESS_TOKEN_SECRET]

bearer_token=[BEARER_TOKEN]

################### Authenticate with google
# control_sheet
SHEET_ID = '1MFIte9Rm4hXk713uXG4DOKKg2gwN8S_GJ-tqEwBi3tk'
SHEET_NAME = 'data'

# authenticate with Google Sheets API using SA credentials
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
daily_data = pd.read_csv(url,index_col=0)

screen_name = "EsportsNews_Bot"

storage_client = storage.Client()

bucket_name = [BUCKET_NAME]

file_name = "tweet_analysis/day.txt"

bucket = storage_client.bucket(bucket_name)

new_blob = bucket.blob(file_name)

if not new_blob.exists():
    new_blob.upload_from_string('1')

current_value = new_blob.download_as_string()
day = int(current_value)

# Increment the value of the variable
if day < 10:
    next_value = day+1
else:
    next_value = 1

new_blob.upload_from_string(str(next_value))


hashtag = daily_data.loc[day,'hashtag']


# Define the API endpoint and parameters
url = "https://api.twitter.com/1.1/search/tweets.json?q="+hashtag+"&count=500&exclude=retweets&tweet_mode=extended&lang=en"
headers = {"Authorization": f"Bearer {bearer_token}"}

# Make the request and parse the JSON response
response = requests.get(url, headers=headers)
tweets = json.loads(response.content)["statuses"]


next_token = tweets[-1]["id_str"]


intento_ultimo=len(tweets)

while len(tweets) < 1000:
    # Define the API endpoint and parameters for the next page
    url = "https://api.twitter.com/1.1/search/tweets.json?q="+hashtag+f"&count=500&max_id={next_token}&exclude=retweets&tweet_mode=extended"
    headers = {"Authorization": f"Bearer {bearer_token}"}
        # Make the request and parse the JSON response
    response = requests.get(url, headers=headers)
    tweets_page  = json.loads(response.content)["statuses"]
    next_token = tweets[-1]["id_str"]
    # Add the tweets from the current page to the list of all tweets
    tweets += tweets_page[1:]
       
    intento_actual=len(tweets)
        
    if intento_actual==intento_ultimo: 
        break
    intento_ultimo=len(tweets)
        
df=pd.json_normalize(tweets)




# example tweet list

tweets = list(set(list(df['full_text'])))
# join tweets into a single string

exclusion_list=['የፋናቲክ ሊግ ኦፍ Legends ቡድንን ለማስቻል ስርዓቱን በማጠናቀቅ ወደ ደም መስመራችን እየተጓዝን']


filtered_tweets = [s for s in tweets if not any(s.startswith(start) for start in exclusion_list)]


## sentiment analysis

from textblob import TextBlob


polarity_scores = []
for tweet in filtered_tweets:
    blob = TextBlob(tweet)
    polarity_scores.append(blob.sentiment.polarity)



## preparo el texto


a=[re.sub(r'@\S+', '',re.sub(r'http\S+', '', tweet)) for tweet in filtered_tweets]

split_list = []
for tweet in filtered_tweets:
    text = re.sub(r'http\S+', '', tweet)
    text = re.sub(r'@\S+', '', text)
    split_list.append(text.split())

a=pd.DataFrame({'words':split_list,'sentiment':polarity_scores})

df_exploded = a.explode('words')


# Deelete punctiation

lista=df_exploded['words']

special_characters = "!%^&_'\"<>,.?`();"

# Remove special characters from the strings in the list
cleaned_list = ["".join(c for c in str(string) if c not in special_characters) for string in lista]


df_exploded['words']=cleaned_list

df_exploded=df_exploded[~(df_exploded['words']=='')]


#Delete stop words



stopwords_sp = get_stop_words('spanish')

stopwords=list(STOPWORDS)+stopwords_sp+['1','2','3','4','5','6','7','8','9']

word_list_clean = df_exploded[~df_exploded['words'].isin(stopwords)]


word_freq = Counter(word_list_clean['words'])

word_freq_df = pd.DataFrame.from_dict(word_freq, orient='index', columns=['frequency'])


word_value=word_list_clean.groupby('words').mean('sentiment')

word_value['color']=word_value['sentiment'].apply(lambda x: 'Positive' if x > 0.25 else ('Neutral' if x > -0.25 else 'Negative'))

sentiments = dict(zip(word_value.index, word_value['color']))


##I get the max rows

word_freq_df['lower']=word_freq_df.index.str.lower()


total_frequencies=word_freq_df.groupby('lower').sum('frequency')['frequency']

word_freq_df_filtered_final=pd.merge(word_freq_df.reset_index(),total_frequencies.reset_index(),left_on='lower',right_on='lower')

max_rows = word_freq_df_filtered_final.groupby('lower')['frequency_x'].idxmax()

result = word_freq_df_filtered_final.loc[max_rows]

word_freq_df_filtered=result[['index','frequency_y']].set_index('index').rename(columns={'frequency_y':'frequency'})


word_freq_counter=Counter(dict(zip(word_freq_df_filtered.index, word_freq_df_filtered['frequency'])))


## Add Custom Mask


# Convert the Counter to a pandas DataFrame
df = pd.DataFrame.from_dict(word_freq_counter, orient='index', columns=['Count'])


image_name=daily_data.loc[day,'image_name']



# Create a client to access the storage bucket
client = storage.Client()

# Specify the name of your storage bucket and the path to the image file
bucket_name = 'the-movie-database-project'
image_path = 'tweet_analysis/reference_files/'+image_name+'.png'

# Get a reference to the image file in your bucket
bucket = client.get_bucket(bucket_name)
blob = bucket.blob(image_path)

# Download the image data and create the mask
image_data = blob.download_as_bytes()

mask = np.array(Image.open(BytesIO(image_data)))

#mask = np.array(Image.open('imagenes/'+image_name+'.png'))

font_path = './STFangSong.ttf'


figsize_1=6*4 #(la imagen original esta x4)
figsize_2=4*4


fig, ax = plt.subplots(
    figsize=(figsize_1,figsize_2)
    )


wc = WordCloud(
    relative_scaling=0.3,
    repeat=True,
    colormap='Oranges',
    font_path='C:/Windows/Fonts/seguiemj.ttf',
    mask=mask, background_color=str(daily_data.loc[day,'background']),
    max_words=2000, max_font_size=256,
    min_font_size=3,
    random_state=42, width=mask.shape[1],
    height=mask.shape[0])
wc.generate_from_frequencies(word_freq_counter)

#### FONT LEGENDS

import matplotlib.font_manager as fm

font_path_legends = 'lustra-text-bold.ttf'
title_font = fm.FontProperties(fname=font_path_legends, size=figsize_1*2, weight='bold')
subtitle_font = fm.FontProperties(fname=font_path_legends, size=figsize_1*1.2, weight='normal')
legend_font = fm.FontProperties(fname=font_path_legends, weight='normal',size=figsize_1*0.9)

legends_color=str(daily_data.loc[day,'titles_legends'])

####

color_map = {'Positive': str(daily_data.loc[day,'color_positive']), 
             'Neutral': str(daily_data.loc[day,'color_neutral']), 
             'Negative': str(daily_data.loc[day,'color_negative'])}

wc.recolor(color_func=lambda word, font_size, position, orientation, random_state=None, **kwargs: color_map[sentiments[word]])

# create a color legend
handles = []
for group, color in color_map.items():
    patch = plt.plot([],[], marker="o", ms=10, ls="", mec=None, color=color,
            label="{:s}".format(group))[0]
    handles.append(patch)

# add the legend to the plot


leg=plt.legend(handles=handles,
           prop=legend_font,
           framealpha=0,
           borderpad=3,
           labelspacing=0.75,
           markerscale=figsize_1/10,
           labelcolor=legends_color)

version=daily_data.loc[day,'texto_version']

if version == 1:
    leg=plt.legend(handles=handles,
               loc= str(daily_data.loc[day,'legend_position']), #### v1
    #           loc= 'upper left', #### v3
    #           ncol=3, #### v3
    #           bbox_to_anchor=(0.4, -0.04), #### v3
               prop=legend_font,
               framealpha=0,
               borderpad=3,
               labelspacing=0.75,
               markerscale=figsize_1/10,
               labelcolor=legends_color)
    
elif version == 2:
    leg=plt.legend(handles=handles,
    #           loc= str(daily_data.loc[day,'legend_position']), #### v1
               loc= 'upper left', #### v3
               ncol=3, #### v3
               bbox_to_anchor=(0.4, -0.04), #### v3
               prop=legend_font,
               framealpha=0,
               borderpad=3,
               labelspacing=0.75,
               markerscale=figsize_1/10,
               labelcolor=legends_color)



plt.imshow(wc, interpolation="bilinear",aspect='auto')


fig.set_facecolor(str(daily_data.loc[day,'background']))


if version == 1:
    plt.suptitle("Analyzing #"+hashtag,color=legends_color, fontproperties=subtitle_font,
    #             y=0.03,x=0.33 ### agregado para v3
                 )
    
    
    plt.title(str(daily_data.loc[day,'name'])+'\'s last 10 days on Twitter', fontproperties=title_font, 
              pad=10,color=legends_color,
    #          y=-0.13  ### agregado para v3
                 )
    
elif version == 2:
    plt.suptitle("Analyzing #"+hashtag,color=legends_color, fontproperties=subtitle_font,
                 y=0.03,x=0.33 ### agregado para v3
                 )
    
    
    plt.title(str(daily_data.loc[day,'name'])+'\'s last 10 days on Twitter', fontproperties=title_font, 
              pad=10,color=legends_color,
              y=-0.13  ### agregado para v3
                 )


plt.axis('off')

result_image_name='result_'+image_name+'.png'

plt.savefig(result_image_name, bbox_inches='tight', pad_inches=0.1,dpi=300)

plt.show()

############# Subo la imagen a DRIVE

# Set up the storage client


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credential.json"



# Set up the Drive API client
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credential.json'

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

drive_service = build('drive', 'v3', credentials=creds)

file_metadata = {'name': result_image_name}

media = MediaFileUpload(result_image_name, resumable=True)

file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

# Generate a shareable link for the file
try:
    permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    result = drive_service.permissions().create(
        fileId=file.get('id'),
        body=permission,
        fields='id'
    ).execute()
    link = f'https://drive.google.com/uc?id={file.get("id")}&export=download'
    print(f"Shareable link for the image: {link}")
except HttpError as error:
    print(f"An error occurred: {error}")


############## TWITTEO LA IMAGEN


# image manipulation
img = Image.open(result_image_name)

b = BytesIO()
img.save(b, "PNG")
b.seek(0)

auth=tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)

api=tweepy.API(auth)


# Upload media to Twitter APIv1.1
ret = api.media_upload(filename=result_image_name, file=b)

# Attach media to tweet
#api.update_status(media_ids=[ret.media_id_string], status=str(hashtag))

media = api.media_upload(result_image_name)

tweet = "#"+str(hashtag)+" "+ str(daily_data.loc[day,'account'])+'\n' + 'HD image: '+link

post_result = api.update_status(status=tweet, media_ids=[media.media_id])

