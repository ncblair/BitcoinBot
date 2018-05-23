import urllib3
import json
from bs4 import BeautifulSoup
import get_historical_data
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime
import utils
import os

def get_price():
	"""
	RETURN: The price of Bitcoin in USD
	"""
	urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
	url = "https://api.coindesk.com/v1/bpi/currentprice.json"
	http = urllib3.PoolManager()
	response = http.request('GET', url)
	data = json.loads(response.data)
	conversion = data['bpi']['USD']['rate_float']
	return conversion

def get_yesterday_price():
	"""
	RETURN: The price of Bitcoin in USD yesterday
	"""
	urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
	url = "https://api.coindesk.com/v1/bpi/historical/close.json?for=yesterday"
	http = urllib3.PoolManager()
	response = http.request('GET', url)
	data = json.loads(response.data)
	conversion = data['bpi']['USD']['rate_float']
	return conversion

@utils.timeit
def get_historical_data():
	"""
	RETURN: the price of Bitcoin in USD historically as a pandas DF
	"""
	#get_historical_data.main()
	return np.load("kraken.npy")


def generator_historical_data():
	"""
	Yields historical data one line at a time
	"""
	with open("kraken.csv") as infile:
	    for line in infile:
	        yield np.array(line.split(",")).astype(float)

@utils.timeit
def get_daily_average_from_data(data):
	"""
	historical data input

	RETURN: average value per day, list of days
	"""
	prices = data[:, 0]
	ts = np.vectorize(datetime.date.fromtimestamp)(data[:, 2])
	num_datapoints = len(ts)

	dates = [ts[0]]
	daily_prices = [prices[0]]
	i = 1
	for date, price in zip(ts[1:], prices[1:]):
		if date == dates[-1]:
			daily_prices[-1] += price
			i += 1
		else:
			daily_prices[-1] /= i
			daily_prices.append(price)
			dates.append(date)
			i = 1
	daily_prices[-1] /= i

	return np.array([daily_prices, dates])

def fill_empty_dates(dates, prices):
	new_dates = []
	new_prices = []

	for i in range(len(dates) - 1):
		date = dates[i]
		next_date = dates[i + 1]
		days_between = (next_date - date).days

		price = prices[i]
		next_price = prices[i + 1]
		price_delta = next_price - price

		slope = price_delta / (days_between)
		new_dates.append(date)
		new_prices.append(price)
		for j in range(1, days_between):
			new_dates.append(date + datetime.timedelta(days=j))
			new_prices.append(price + j * slope)

	new_dates.append(dates[-1])
	new_prices.append(prices[-1])

	return np.array(new_dates), np.array(new_prices)





@utils.timeit
def plot_historical_data(historical_data):
	"""
	HISTORICAL_DATA: np array (num_points, 3) [price, volume, utc_timestamp]

	Plot historical bitcoin price data
	"""
	fig, ax = plt.subplots(figsize=(10, 6))

	prices = historical_data[:, 0].T

	volume = historical_data[:, 1].T
	timestamps = historical_data[:, 2].T
	timestamps = np.vectorize(datetime.datetime.fromtimestamp)(timestamps)

	daily, days = get_daily_average_from_data(historical_data)

	hunnit_day_moving = utils.moving_average(daily, n=100)

	ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))

	plt.title("Bitcoin Price in USD")

	ax.plot(timestamps, prices, label = "price")
	ax.plot(days, hunnit_day_moving, label = "100-day moving average")
	ax.plot(timestamps, volume, label = "volume")

	ax.legend()

	plt.show()