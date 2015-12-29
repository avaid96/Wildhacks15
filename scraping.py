from bs4 import BeautifulSoup
import csv
import webbrowser
import urllib
import json
import urllib2
import numpy as np
import scipy
import pandas
import requests
import feedparser
import matplotlib.pyplot as plt


SITE = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
b=open("tickers.csv", "wb")
cwrite = csv.writer(b)

def price_info(tickr):
	page= 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20("'+tickr+'")%0A%09%09&env=http%3A%2F%2Fdatatables.org%2Falltables.env&format=json'
	data = json.load(urllib2.urlopen(page))
	return data

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
        return np.mean(sentiments)
        print "ran"
    # return -2

def scrape_list(site):
    req = urllib2.Request(site)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
    table = soup.find('table', {'class': 'wikitable sortable'})
    sector_tickers = dict()
    cwrite.writerow(["ticker", "sector","DaysLow", "DaysHigh", "volume", "OneyrTargetPrice"])
    for row in table.findAll('tr'):
        col = row.findAll('td')
        if len(col) > 0:
            ticker = str(col[0].string.strip())
            sector=str(col[3].string.strip())
            info=price_info(ticker)
            sentiment=getsentiment(ticker)
            print sentiment
            if(info['query']['results']['quote']['OneyrTargetPrice']!="none"):
                if(sentiment!=-2):
                    cwrite.writerow([ticker, sector,info['query']['results']['quote']['DaysLow'], info['query']['results']['quote']['DaysHigh'], info['query']['results']['quote']['Volume'], info['query']['results']['quote']['OneyrTargetPrice'], sentiment, float(info['query']['results']['quote']['DaysHigh'])-float(info['query']['results']['quote']['DaysLow']) ])
                else:
                    cwrite.writerow([ticker, sector,info['query']['results']['quote']['DaysLow'], info['query']['results']['quote']['DaysHigh'], info['query']['results']['quote']['Volume'], info['query']['results']['quote']['OneyrTargetPrice'],-2, float(info['query']['results']['quote']['DaysHigh'])-float(info['query']['results']['quote']['DaysLow'])])
            else:
                if(sentiment!=-2):
                    cwrite.writerow([ticker, sector,info['query']['results']['quote']['DaysLow'], info['query']['results']['quote']['DaysHigh'], info['query']['results']['quote']['Volume'], "-", sentiment, float(info['query']['results']['quote']['DaysHigh'])-float(info['query']['results']['quote']['DaysLow'])])
                else:
                    cwrite.writerow([ticker, sector,info['query']['results']['quote']['DaysLow'], info['query']['results']['quote']['DaysHigh'], info['query']['results']['quote']['Volume'], "-", -2, float(info['query']['results']['quote']['DaysHigh'])-float(info['query']['results']['quote']['DaysLow'])])
scrape_list(SITE)
b.close()

