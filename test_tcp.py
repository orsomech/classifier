from multiprocessing import Process
import socket  # Import socket module
import struct
import sys
import numpy as np
import scipy.io as sio
from utils.timeit import timeit
import datetime
import time

response_count = 0
x_test = sio.loadmat('data/X_test_4D_for_keras.mat')
x_test = x_test['X_test']
x_test = np.swapaxes(x_test, 2, 3)
x_test = np.swapaxes(x_test, 1, 2)
x_test = np.swapaxes(x_test, 0, 1)


@timeit
def send_requests(socket, count, sample=None):
    bytes_sample = np.ndarray.tobytes(sample)
    for i in range(count):
        for j in range(1000):
            socket.sendall(bytes_sample)
        #time.sleep(1)
    #socket.sendall(None)


@timeit
def receive_response(socket, count):
    response_count = 0
    print(f'Expected responses {count}')

    try:
        while response_count < count:
            #print('recv ', response_count)
            response_count += 1
            socket.recv(1024)
            #print(response_count, end=' ')
    finally:
        print()
        print(f'{response_count} responses')


def send_requests_continually(scket, sample):
    try:
        bytes_sample = np.ndarray.tobytes(sample)
        while True:
            scket.sendall(bytes_sample)
    except Exception as e:
        x = 0
        #print(e)


def receive_response_time(scket, seconds):
    print(f'Running for {seconds} seconds')
    response_count = 0
    time_start = time.time()

    try:
        while (time.time() - time_start) < seconds:
            response_count += 1
            scket.recv(1024)
        scket.sendall(None)
    #except Exception as e:
    #    print(e)
    finally:
        print(f'{response_count} responses')


if __name__ == '__main__':
    try:
        # Select specific sample
        index = 0  # index can be in a range: [0 --- len(x_test)-1]
        samples_to_classify = x_test[index:index + 1, :, :, :]

        s = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 12345             # Reserve a port for your service.

        s.connect((host, port))

        #send_requests(s, 40)
        test_count = 10
        print('sending requests')
        #process = Process(target=send_requests, args=(s, test_count, samples_to_classify))
        process = Process(target=send_requests_continually, args=(s, samples_to_classify))
        process.start()
        #print('sending requests done')

        '''
        for i in range(test_count):
            buffer = s.recv(1024)
            #buffer = np.ndarray(buffer=buffer, shape=(1, 2, 128, 1), dtype=np.float64)
            print(i, ': ', struct.unpack('f', buffer))
        '''

        s.recv(1024)

        #print('Samples count: ', test_count)
        #receive_response(s, (test_count*1000)-2)
        receive_response_time(s, 30)

        '''
        for i in range(test_count-1):
            # print('Receive: ', i)
            response_count += 1
            s.recv(1024)
        '''
        #time.sleep(10)

        s.shutdown(socket.SHUT_WR)
        s.close()
    except Exception as e:
        x = 0
        #print(e)
    #finally:
    #    print(f'{response_count} responses received {datetime.datetime.now().time()}')
