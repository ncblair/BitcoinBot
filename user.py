import numpy as np
import price
import utils

class User:

	def __init__(self, username):
		self.username = username
		self.weight = 1


	def get_name(self):
		return self.username

	def strategy(self, dates, prices):
		"""
		RETURNS:
			1 if user thinks it is a good idea to own bitcoin
			0 if the user thinks it is a bad idea to own bitcoin
		"""
		raise NotImplementedError

class Random_user(User):
	"""
	Toy user, uses the least information and is expected to perform as the market does
	"""
	def strategy(self, dates, prices):
		return np.random.choice([0, 1], size=len(dates))

class N_day_trend_user(User):
	"""
	Owns bitcoin if n_day moving average is positively sloping
	"""
	def __init__(self, username, n):
		super().__init__(username)
		self.n = n

	def strategy(self, dates, prices):
		T = len(dates)
		strategies = np.empty(shape=T)
		strategies[0] = np.random.choice([0, 1])
		movavg = utils.moving_average(prices, self.n)
		strategies[1:] = [movavg[i] > movavg[i - 1] for i in range(1, T)]
		return strategies

# class RNN_user(User):
# 	def __init__(self, username, args):
# 		super().__init__(username)
# 		raise NotImplementedError
# 		self.nn = get_RNN(args)

# 	def strategy(self, dates, prices):
# 		T = len(dates)
# 		strategies = np.empty(shape=T)
# 		predictions = np.empty(shape=T)
# 		for d in dates:
			

class Genie(User):
	"""
	Knows the future
	"""
	def strategy(self, dates, prices):
		T = len(dates)
		strategies = np.empty(shape = T)
		strategies[-1] = np.random.choice([0, 1])
		strategies[:-1] = [prices[i] > prices[i - 1] for i in range(1, T)]
		return strategies