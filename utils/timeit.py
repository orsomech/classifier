from time import time


def timeit(method):
    def timed(*args, **kw):
        ts = time()
        result = method(*args, **kw)
        te = time()
        print('{0}: {1:.6f}'.format(method.__name__, te - ts))

        return result
    return timed
