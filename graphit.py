import numpy as np
import matplotlib.pyplot as plt
import csv
b=open("tickers.csv", "rb")
cread = csv.reader(b)
pricechange=[]
sentiment=[]
for row in cread:
	if(row[6]!='Sentiment'):
		pricechange=pricechange+[float(row[6])]
		sentiment=sentiment+[float(row[7])]
plt.scatter(pricechange, sentiment)
plt.show()