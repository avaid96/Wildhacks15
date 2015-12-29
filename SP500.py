import numpy as np
import scipy
import pandas
import requests
import feedparser
import json
import matplotlib.pyplot as plt

def getsentiment(tickr):
	ticker = tickr
	feed = requests.get("https://www.google.com/finance/company_news?q=" + ticker + "&output=rss")
	if(feed.status_code == 200):
		data = feedparser.parse(feed.text)
		d = pandas.DataFrame.from_dict(data['entries'])
		sentiments = []
		for link in d['link'].values:
			resp = requests.get("https://api.havenondemand.com/1/api/sync/analyzesentiment/v1?apikey=efcb119e-5470-4673-b22c-b00c32640257&url=" + link)
			if(resp.status_code == 200):
				resp = resp.json()
				sentiments.append(resp['aggregate']['score']*(1 if resp['aggregate']['sentiment'] == 'positive' else -1))
		print np.mean(sentiments)

getsentiment("aph")


