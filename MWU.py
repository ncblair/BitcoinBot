import numpy as np
import math
import utils
import price

def simulate_MWU(dates, prices, experts):
	"""
	DATES: List of dates (Nx1)
	PRICES: List of prices on each day (Nx1)
	EXPERTS: List of User objects (Mx1)
	"""
	dates, prices = price.fill_empty_dates(dates, prices)

	N = len(dates)
	M = len(experts)
	strategies = np.array([e.strategy(dates, prices) for e in experts]) #MxN
	weights = np.ones(shape=M)
	profits = np.empty(shape=M) #profits[i] is the profit for expert i
	eps = max(.01, min(math.sqrt(math.log(M) / N), .95)) 
	#epsilon in [.01, .95]
	delta = 1 - eps
	choices = np.empty(shape=N)
	my_profit = 0
	regret = 0
		
	normed_price_neg_deltas = utils.sigmoid((prices[:-1] - prices[1:]))

	for i in range(N - 1):
		weights = weights / sum(weights)
		costs = strategies[:, i] * normed_price_neg_deltas[i]
		profits += strategies[:, i] * (prices[i + 1] - prices[i])
		choices[i] = np.random.choice(strategies[:, i], p=weights)
		my_profit += choices[i] * (prices[i + 1] - prices[i])
		weights *= delta ** costs
	weights  = weights / sum(weights)
	choices[N-1] = np.random.choice(strategies[:, N-1], p=weights)

	regret = max(profits) - my_profit

	market_profit = prices[N - 1] - prices[0]

	for e, w in zip(experts, weights):
		e.weight = w

	print(f"weights: {[(e.get_name(), e.weight) for e in experts]}")
	return choices, my_profit, regret, market_profit











