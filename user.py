import numpy as np
import price

class User:

	def __init__(self, username):
		self.username = username
		self.weight = 1


	def get_name(self):
		return self.username

	def strategy(self):
		"""
		RETURNS:
			1 if user thinks it is a good idea to buy bitcoin
			0 if the user has no preference
			-1 if user thinks it is a bad idea to buy bitcoin
		"""
		raise NotImplementedError

class Random_user(User):
	def strategy(self):
		return np.random.choice([-1, 1])

class Two_day_trend_user(User):
	def strategy(self, day="Today"):
		if day == "Today":
			curr_price = price.get_price()
			prev_price = price.get_yesterday_price()
		else:
			return

		return 2 * (curr_price > prev_price) - 1
