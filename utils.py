import numpy as np
import time
from multiprocessing import Process, Manager

def moving_average(a, n=3):
    cum = np.cumsum(a, dtype=float)
    ret = np.empty(shape=len(a))
    for i in range(1, n):
    	ret[i] = cum[i] / (i + 1)
    ret[n:] = (cum[n:] - cum[:-n]) / n

    return ret


def get_average_value_per_day(array, timestamps):
	"""
	ARRAY: array of values
	TIMESTAMPS: array of datetime objects that correspond to values

	RETURN: average value per day, list of days
	"""
	num_data_on_day = 0
	ret = [0]
	days = [get_day(timestamps[0])]
	for value, time in zip(array, timestamps):
		if get_day(time)[0] == days[-1][0]:
			num_data_on_day += 1
			ret[-1] += value
		else:
			days.append(get_day(time))
			ret[-1] = ret[-1] / num_data_on_day
			num_data_on_day = 1
			ret.append(value)
	ret[-1] = ret[-1] / num_data_on_day
	days = [day[1] for day in days]
	return np.array(ret), np.array(days)




def get_day(timestamp):
	return ((timestamp.month, timestamp.day, timestamp.year), timestamp)


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print(f"{method.__name__} {(te-ts) * 1000:.2f} ms")
        return result
    return timed

#modified two functions from:
#https://stackoverflow.com/questions/3288595/multiprocessing-how-to-use-pool-map-on-a-function-defined-in-a-class/21345308
def spawn(f):
    def fun(q,x):
        y = f(x)
        q.put(y)
    return fun

#multiprocessing map for nested functions
def parmap(f,X):
    queue=[Manager().Queue() for x in X]
    proc=[Process(target=spawn(f),args=(q,x)) for x,q in zip(X,queue)]
    [p.start() for p in proc]
    [p.join() for p in proc]
    return [q.get() for q in queue]