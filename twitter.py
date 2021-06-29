import tweepy as tw
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import preprocessor as p
# Import stopwords
import nltk
from nltk.corpus import stopwords
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
# Import textblob
from textblob import Word, TextBlob
from datetime import datetime
from datetime import timedelta
begin = datetime.now()
## API KEYS -------------------------------------------------------------------
def intitialize():
    consumer_key = '3FmyEzN2CUBxtj8vgy9rxiZ6E'
    consumer_secret = 'rXuPfQQYXiE1ynTpOodmSgFrqHKkz6zYDxzv4fgUO0KBFwdHcN'
    access_token = '1404841426886619139-pnIagdlErQRIGsB0n9skgtgaD582z4'
    access_token_secret = 'NOPOJhGL3zLsRdwDpiaURhprzG2XiTa5nmO8Bee4CJIkA'
    # setup for the api
    # Authenticate
    auth = tw.OAuthHandler(consumer_key,    consumer_secret)
    # Set Tokens
    auth.set_access_token(access_token, access_token_secret)
    # Instantiate API
    api = tw.API(auth, wait_on_rate_limit=True)

def get_tweets(tag,start,api):
    hashtag = f'#{tag} -filter:retweets'
    query = tw.Cursor(api.search, q=hashtag,lang='en',since=start,result_type='mixed').items(100)
    tweets = [{'Tweet':tweet.text, 'Timestamp':tweet.created_at,'Likes':tweet.favorite_count,'RT':tweet.retweet_count} for tweet in query]
    print("Download-ready")
    return tweets

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

def preprocess_tweets(tweet, custom_stopwords,stop_words):
    processed_tweet = tweet
    processed_tweet.replace('[^\w\s]@$', '')
    processed_tweet = " ".join(word for word in processed_tweet.split() if word not in stop_words)
    processed_tweet = " ".join(word for word in processed_tweet.split() if word not in custom_stopwords)
    processed_tweet = " ".join(Word(word).lemmatize() for word in processed_tweet.split())
    processed_tweet = " ".join(deEmojify(word) for word in processed_tweet.split())
    processed_tweet = " ".join(p.clean(word) for word in processed_tweet.split())
    return(processed_tweet)

# t = datetime.date(datetime.now()-timedelta(days=1))
# start = t.strftime('%Y-%m-%d')
# tweets = get_tweets("dogecoin",start)
# df = pd.DataFrame.from_dict(tweets)
# stop_words = stopwords.words('english')
# custom_stopwords = ['RT', '#dogecoin','#Dogecoin','@elonmusk']
# df['Processed Tweet'] = df['Tweet'].apply(lambda x: preprocess_tweets(x, custom_stopwords))
# df["pos"] = 0
# df["neg"] = 0
# df["neu"] = 0
# df["compound"] = 0
# sid = SentimentIntensityAnalyzer()
# df['pos'] = df["Processed Tweet"].map(lambda x: sid.polarity_scores(x)['pos'])
# df['neg'] = df["Processed Tweet"].map(lambda x: sid.polarity_scores(x)['neg'])
# df['neu'] = df["Processed Tweet"].map(lambda x: sid.polarity_scores(x)['neu'])
# df['compound'] = df["Processed Tweet"].map(lambda x: sid.polarity_scores(x)['compound'])
# df.drop(['Tweet'],axis=1,inplace=True)
# new = df[df['compound']!=0]
# new.reset_index(drop=True, inplace=True)
# print(new)
# end = datetime.now()
# print((end-begin).total_seconds())

def sentiment_analyze():
    consumer_key = '3FmyEzN2CUBxtj8vgy9rxiZ6E'
    consumer_secret = 'rXuPfQQYXiE1ynTpOodmSgFrqHKkz6zYDxzv4fgUO0KBFwdHcN'
    access_token = '1404841426886619139-pnIagdlErQRIGsB0n9skgtgaD582z4'
    access_token_secret = 'NOPOJhGL3zLsRdwDpiaURhprzG2XiTa5nmO8Bee4CJIkA'
    # setup for the api
    # Authenticate
    auth = tw.OAuthHandler(consumer_key,    consumer_secret)
    # Set Tokens
    auth.set_access_token(access_token, access_token_secret)
    # Instantiate API
    api = tw.API(auth, wait_on_rate_limit=True)
    t = datetime.date(datetime.now()-timedelta(days=1))
    start = t.strftime('%Y-%m-%d')
    dataframes = {"eth":0,"doge":0,"btc":0}
    for i,j in zip(["ethereum","dogecoin","bitcoin"],dataframes.keys()):
        tweets = get_tweets(i,start,api)
        df = pd.DataFrame.from_dict(tweets)     
        stop_words = stopwords.words('english')
        custom_stopwords = ['RT', '#dogecoin','#Dogecoin','#Ethereum','#Bitcoin','@elonmusk']
        df['Processed Tweet'] = df['Tweet'].apply(lambda x: preprocess_tweets(x, custom_stopwords,stop_words))
        df["pos"] = 0
        df["neg"] = 0
        df["neu"] = 0
        df["compound"] = 0
        sid = SentimentIntensityAnalyzer()
        df['pos'] = df["Processed Tweet"].map(lambda x: sid.polarity_scores(x)['pos'])
        df['neg'] = df["Processed Tweet"].map(lambda x: sid.polarity_scores(x)['neg'])
        df['neu'] = df["Processed Tweet"].map(lambda x: sid.polarity_scores(x)['neu'])
        df['compound'] = df["Processed Tweet"].map(lambda x: sid.polarity_scores(x)['compound'])
        df.drop(['Tweet'],axis=1,inplace=True)
        df["sentiment"] = df.compound.map(lambda x: "pos" if x>0 else ("neg" if x<0 else "neu"))
        dataframes[j] = df
    #print(senti)
    # end = datetime.now()
    # print((end-begin).total_seconds())
    return dataframes
#sentiment_analyze()