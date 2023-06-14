# Esports Team Performance Tracker: Twitter Bot and Wordcloud Generation & Analysis
## Project Description

This personal project involves the creation of a Twitter Bot that analyzes the last 10 days of Tweets related to the most prominent Esports Teams (T1, FNATIC, Cloud9). Each day, the bot selects one team and generates a Wordcloud in the shape of that team's logo. The words in the Wordcloud are color-coded to match the team's official colors, providing a captivating visual representation of the team's performance.

To see the team's performance, sentiment analysis is applied to the tweets using the team's colors. When the team performs well, the Word Sensitive Analysis tends to be positive, displaying a predominance of positive sentiment words. If the team losses or gets disqualified from important competitions, the sentiment tends to be negative.

This project offers a dynamic and visually engaging solution for tracking the performance of top Esports Teams through automated analysis of Twitter data. It can also be useful for marketing professionals seeking for an automated and consistent way to generate quality content.

## Deliverables

* [Wordcloud's Control Pannel](https://docs.google.com/spreadsheets/d/1MFIte9Rm4hXk713uXG4DOKKg2gwN8S_GJ-tqEwBi3tk/edit#gid=0)
* [A different Wordcloud once a Day](https://github.com/ICereghetti/project_twitter_wordclouds/tree/5baa21324a5e5e0bbfacbb93ea6ea2755713acb8/wordcloud_samples)
* [Twitter Bot Code](https://github.com/ICereghetti/project_twitter_wordclouds/blob/5baa21324a5e5e0bbfacbb93ea6ea2755713acb8/code.py)
* [Twitter Bot Profile](https://twitter.com/EsportsNews_bot) (Deprecated temporarly after May-22, since Twitter changed their Therms and conditions)

## Skills Used in This Project
1) Data Scraping
2) Text Processing/Manipulation
3) Data Modeling
4) Data Mining

## Tools Used

1) Python (tweepy, WordCloud, BeautifulSoup, google.cloud, requests)
2) Google Cloud Platform (BigQuery,Cloud Functions, Scheduer, Google Docs, Storage)
3) Twitter


## Highlights
#### A) Create a list of teams to analyze their logo and create a Control Pannel to change Wordclouds condiguration 
1) The Control Pannel is read using Google Sheets API. In this way we can change the Charts parameters withouth changing the code, just changing the options in the Spreadsheet.
2) Following the previous day order, a team is chosen to create the wordcloud.

Deliverable:
   - [Wordcloud's Control Pannel](https://docs.google.com/spreadsheets/d/1MFIte9Rm4hXk713uXG4DOKKg2gwN8S_GJ-tqEwBi3tk/edit#gid=0)
![](https://github.com/ICereghetti/Cereghetti_Portfolio/blob/f4914a3740d8a269d538f12108a96f0d55c125b5/images/project_twitter_wordcloud_1.png)

#### B) Created the Wordcloud of the team chosen based on the control panel's config.
1) Once the team is chosen, the code looks for their main Hashtag to analyze their last 10 days tweets.
2) Leveraged Pandas, Tweepy, and BeautifulSoup, Counter and STOPWORDS for data structuring.
3) Sentiment analysis is made with TextBlob, then calculated an average for each relevant word.
4) matplotlib, Wordcloud, BytesIO and Image packages are used to create the image shaped like that team's logo and configurated for that team following the Spreadsheet parameters chosed for that team.

Deliverables:
   - [A different Wordcloud once a Day](https://github.com/ICereghetti/project_twitter_wordclouds/tree/5baa21324a5e5e0bbfacbb93ea6ea2755713acb8/wordcloud_samples)
![](https://github.com/ICereghetti/Cereghetti_Portfolio/blob/a61458d7ca0c47664b3a89a042f665cda465c7e2/images/project_twitter_wordcloud_3.png)

#### C) The Wordcloud is uploaded and posted in my Twitter Bot Account using Twitter API

Deliverable:
   - [Twitter Bot Code](https://github.com/ICereghetti/project_twitter_wordclouds/blob/5baa21324a5e5e0bbfacbb93ea6ea2755713acb8/code.py)
   - [Twitter Bot Profile](https://twitter.com/EsportsNews_bot)

![](https://github.com/ICereghetti/Cereghetti_Portfolio/blob/f4914a3740d8a269d538f12108a96f0d55c125b5/images/project_twitter_wordcloud_2.png)
