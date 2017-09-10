import numpy as np
from flask import Flask, request
from utils.timeit import timeit
from providers import model_provider
import io

model = model_provider.load()
app = Flask('Classifier')

print('classifier ready')


@app.route('/classify')
@timeit
def classify():
    print('classify')
    #sample = np.fromstring(request.form['sample'])
    #print(request.form['sample'])
    #f = io.StringIO(request.form['sample'])
    #f.seek(0)
    #sample = np.load(f)
    #print('before {0}'.format(sample))
    p = request.form['sample']
    print(p)
    sample = np.fromstring(request.form['sample'], dtype=np.float64).reshape((1, 2, 128, 1))

    #sample = np.swapaxes(sample, 2, 3)
    #sample = np.swapaxes(sample, 1, 2)
    #sample = np.swapaxes(sample, 0, 1)

    return model.predict(sample)


if __name__ == '__main__':
    i = 0
