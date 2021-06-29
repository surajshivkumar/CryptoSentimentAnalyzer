import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
import re
import string
#from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
def get_data(crpyto_symbols):
    data = {}
    for i in crpyto_symbols:
        data[i] = yf.download(tickers=i, period = '1mo', interval = '1d')
    return data

        
