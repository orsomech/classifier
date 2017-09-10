import numpy as np
import scipy.io as sio
import requests
from utils.timeit import timeit
from io import StringIO, BytesIO
from providers.model_provider import load

x_test = sio.loadmat('data/X_test_4D_for_keras.mat')
x_test = x_test['X_test']
x_test = np.swapaxes(x_test, 2, 3)
x_test = np.swapaxes(x_test, 1, 2)
x_test = np.swapaxes(x_test, 0, 1)


# Select specific sample
index = 0  # index can be in a range: [0 --- len(x_test)-1]
samples_to_classify = x_test[index:index + 1, :, :, :]
#print(type(samples_to_classify))

@timeit
def test():
    payload = {'sample': samples_to_classify.tostring()}

    for i in range(1, 2):
        print(requests.get('http://localhost:5000/classify', data=payload))


if __name__ == '__main__':
    model = load()
    print(model.predict(samples_to_classify))
    test()
    #print(samples_to_classify)
    #test()
    #print(samples_to_classify.dtype)
    #print(samples_to_classify.shape)
    #print(type(samples_to_classify.dtype))
    #print(type(samples_to_classify.shape))

    '''
    from tempfile import TemporaryFile

    f = TemporaryFile()
    np.savez(f, x=samples_to_classify)
    f.seek(0)
    npz = np.load(f)
    
    print(npz['x'])
    print(samples_to_classify)
    '''

