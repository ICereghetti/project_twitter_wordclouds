# Esports Team Performance Tracker: Twitter Bot and Wordcloud Generation & Analysis
## Project Description

This personal project involves the creation of a Twitter Bot that analyzes the last 10 days of Tweets related to the most prominent Esports Teams (T1, FNATIC, Cloud9). Each day, the bot selects one team and generates a Wordcloud in the shape of that team's logo. The words in the Wordcloud are color-coded to match the team's official colors, providing a captivating visual representation of the team's performance.

To see the team's performance, sentiment analysis is applied to the tweets using the team's colors. When the team performs well, the Word Sensitive Analysis tends to be positive, displaying a predominance of positive sentiment words. If the team losses or gets disqualified from important competitions, the sentiment tends to be negative.

This project offers a dynamic and visually engaging solution for tracking the performance of top Esports Teams through automated analysis of Twitter data. It can also be useful for marketing professionals seeking for an automated and consistent way to generate quality content.

## Deliverables

The project includes the following deliverables:

* [Wordcloud's Control Panel](https://docs.google.com/spreadsheets/d/1MFIte9Rm4hXk713uXG4DOKKg2gwN8S_GJ-tqEwBi3tk/edit#gid=0): A Google Sheets document that acts as a control panel for changing Wordcloud configurations.
* [A different Wordcloud once a Day](https://github.com/ICereghetti/project_twitter_wordclouds/tree/5baa21324a5e5e0bbfacbb93ea6ea2755713acb8/wordcloud_samples): A collection of Wordcloud images generated daily, each representing a different team's performance.
* [Twitter Bot Code](https://github.com/ICereghetti/project_twitter_wordclouds/blob/5baa21324a5e5e0bbfacbb93ea6ea2755713acb8/code.py): The code used to create and update the Wordclouds and post them on Twitter.
* [Twitter Bot Profile](https://twitter.com/EsportsNews_bot) (Deprecated temporarily after May-22, since Twitter changed their Terms and Conditions): The Twitter profile of the bot used to post the Wordclouds.

## Skills Used in This Project

1) Data Scraping
2) Text Processing/Manipulation
3) Data Modeling
4) Data Mining
5) Data Visualization

## Tools Used

The following tools and technologies were used in this project:

1) Python (tweepy, WordCloud, BeautifulSoup, google.cloud, requests): Python libraries for data processing, web scraping, and generating Wordclouds.
2) Google Cloud Platform (BigQuery, Cloud Functions, Scheduler, Google Docs, Storage): Google Cloud services used for data storage, scheduling tasks, and managing the control panel.
3) Twitter: Twitter API is used to retrieve tweets, post Wordclouds, and manage the bot account.

## Highlights

### A) Create a list of teams to analyze their logo and create a Control Panel to change Wordcloud configurations

1. The Control Panel is implemented using the Google Sheets API, allowing for easy modification of Wordcloud parameters without changing the code. Options in the spreadsheet control the appearance of the Wordcloud.
2. Each day, a team is chosen based on the previous day's order to create the Wordcloud.

Deliverable:
- [Wordcloud's Control Panel](https://docs.google.com/spreadsheets/d/1MFIte9Rm4hXk713uXG4DOKKg2gwN8S_GJ-tqEwBi3tk/edit#gid=0)
![Wordcloud's Control Panel](https://github.com/ICereghetti/Cereghetti_Portfolio/blob/f4914a3740d8a269d538f12108a96f0d55c125b5/images/project_twitter_wordcloud_1.png)

### B) Create the Wordcloud of the chosen team based on the control panel's configuration

1. Once a team is chosen, the code looks for their main hashtag to analyze their last 10 days of tweets.
2. Utilizing libraries such as Pandas, Tweepy, BeautifulSoup, Counter, and STOPWORDS, the data is structured.
3. Sentiment analysis is performed using TextBlob, and averages are calculated for each relevant word.
4. The Wordcloud is created using libraries such as matplotlib, Wordcloud, BytesIO, and Image, generating an image in the shape of the team's logo and configured according to the parameters chosen in the spreadsheet.

Deliverables:
- [A different Wordcloud once a Day](https://github.com/ICereghetti/project_twitter_wordclouds/tree/5baa21324a5e5e0bbfacbb93ea6ea2755713acb8/wordcloud_samples)
![Wordcloud Sample](https://github.com/ICereghetti/Cereghetti_Portfolio/blob/a61458d7ca0c47664b3a89a042f665cda465c7e2/images/project_twitter_wordcloud_3.png)

### C) Upload and post the Wordcloud in the Twitter Bot Account using Twitter API

Deliverables:
- [Twitter Bot Code](https://github.com/ICereghetti/project_twitter_wordclouds/blob/5baa21324a5e5e0bbfacbb93ea6ea2755713acb8/code.py)
- [Twitter Bot Profile](https://twitter.com/EsportsNews_bot)

![Twitter Bot Wordcloud](https://github.com/ICereghetti/Cereghetti_Portfolio/blob/f4914a3740d8a269d538f12108a96f0d55c125b5/images/project_twitter_wordcloud_2.png)
