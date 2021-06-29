from flask import Flask , render_template
from init import get_data
from datetime import datetime
from twitter import sentiment_analyze
import numpy as np
crypto_symbols = ['DOGE-INR','ETH-INR','BTC-INR']
app = Flask(__name__)

@app.route("/")
def home():
    datac = get_data(crypto_symbols)
    labels = [datetime.strftime(i, "%d-%b") for i in datac['DOGE-INR'].index]
    labels = [str(i) for i in labels]
    sentiment = sentiment_analyze()
    cols = sentiment['doge'].columns
    records = {}
    scores = {}
    likes,retweets = {},{}
    sentiments = {}
    for i in sentiment.keys():
        records[i] = sentiment[i].to_dict('records')
        neg = sentiment[i].neg.values  
        pos = sentiment[i].pos.values
        neu = sentiment[i].neu.values
        pos = [i for i in pos]
        neg = [i for i in neg]
        neu = [i for i in neu]
        scores[i] = [pos,neg,neu]
        timeline = sentiment[i].Timestamp.values
        likes = sentiment[i].Likes.values
        retweets = sentiment[i].RT.values
        tweets = sentiment[i]["Processed Tweet"].values
        sentiments[i] = sentiment[i].sentiment.value_counts().values
        sentiments[i] = [i for i in sentiments[i]]

        for k,v in enumerate(scores[i]):
            scores[i][k] = np.mean(v)
    
    data = {"pos":pos,"neg":neg,"neu":neu,"timeline":timeline,"likes":likes,"retweets":retweets,"tweets":tweets}
    #labels = [str(i)[5:10] for i in datac['DOGE-INR'].index]
    values ={}
    values["DOGE-INR"] = [i[0] for i in datac['DOGE-INR'].values]
    values["BTC-INR"] =  [i[0] for i in datac['BTC-INR'].values]
    values["ETH-INR"] =  [i[0] for i in datac['ETH-INR'].values]
    return render_template ('graph3.html',data = values,labels = list(labels),scores = scores,sentiments = sentiments,columns = cols,records = records)

if __name__ == "__main__":
	app.run(debug=True)
