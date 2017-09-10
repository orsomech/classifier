import socket               # Import socket module
import numpy as np
import scipy.io as sio
from utils.timeit import timeit

x_test = sio.loadmat('data/X_test_4D_for_keras.mat')
x_test = x_test['X_test']
x_test = np.swapaxes(x_test, 2, 3)
x_test = np.swapaxes(x_test, 1, 2)
x_test = np.swapaxes(x_test, 0, 1)


@timeit
def send_requests(socket, count, sample):
    bytes_sample = np.ndarray.tobytes(sample)
    for i in range(count):
        socket.sendall(bytes_sample)

# Select specific sample
index = 0  # index can be in a range: [0 --- len(x_test)-1]
samples_to_classify = x_test[index:index + 1, :, :, :]


s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                 # Reserve a port for your service.

s.connect((host, port))

send_requests(s, 1000, samples_to_classify)

s.shutdown(socket.SHUT_WR)
s.close()
