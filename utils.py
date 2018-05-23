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

def sigmoid(x):
	return 1 / (1 + np.exp(-x))

def squisher(x):
	def squisher_help(single):
		if single >= 0:
			return 1.5 - ((1 / (1 + single)) + 1) / 2
		else:
			return (1 / (1 - single)) / 2
	return np.vectorize(squisher_help)(x)


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

def spawn(f):
    def help_spawn(q,x):
        y = f(x)
        q.put(y)
    return help_spawn

#multiprocessing map for nested functions
def parmap(f,X):
    queue=[Manager().Queue() for x in X]
    proc=[Process(target=spawn(f),args=(q,x)) for x,q in zip(X,queue)]
    [p.start() for p in proc]
    [p.join() for p in proc]
    return [q.get() for q in queue]