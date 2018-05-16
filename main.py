import numpy as np
import price
import user
import os
import sqlite3
import datetime

def main():
	# conn = sqlite3.connect('user.db')
	# c = conn.cursor()

	# users = [user.Random_user("random1"), user.Random_user("random2"), user.Two_day_trend_user("two_day")]
	# strategies = [user.strategy() for user in users]

	price_history = price.get_historical_data()

	price.plot_historical_data(price_history)






if __name__ == "__main__":
	main()