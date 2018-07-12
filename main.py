import numpy as np
import price
import user
import os
import sqlite3
import datetime
import MWU

def main():
	# conn = sqlite3.connect('user.db')
	# c = conn.cursor()

	# users = [user.Random_user("random1"), user.Random_user("random2"), user.Two_day_trend_user("two_day")]
	# strategies = [user.strategy() for user in users]

	price_history = price.get_historical_data()

	#price.plot_historical_data(price_history)

	prices, dates = price.get_daily_average_from_data(price_history)

	experts = [user.Random_user("bob")]
	experts += [user.N_day_trend_user(f"{n}day", n) for n in range(1, 100, 5)]
	# experts += [user.Genie("genie")]

	results = MWU.simulate_MWU(dates, prices, experts)
	choices, profit, regret, market_profit = results

	print(f"choices: {choices}")
	print(f"profit: {profit}")
	print(f"regret: {regret}")
	print(f"market_profit: {market_profit}")








if __name__ == "__main__":
	main()