from providers import model_provider
from utils.timeit import timeit
import multiprocessing as mp
from multiprocessing import Process, Queue, JoinableQueue
from entities.classifier import Classifier
import os
import numpy as np
import socket
import datetime

processes_count = os.cpu_count()

samples = Queue()
predictions = Queue()


#@timeit
def process_requests(samples, client):
    print(f'Starting process {os.getpid()}')

    i = 0
    try:
        model = model_provider.load()

        while True:
            #print('get ', i)
            buffer = samples.get()

            if buffer == b'':
                break

            buffer = np.ndarray(buffer=buffer, shape=(1, 2, 128, 1), dtype=np.float64)
            prediction = model.predict(buffer)

            l = client.send(np.ndarray.max(prediction))
            #print(f'send {np.ndarray.max(prediction)}, {i}, {l}')
            i += 1
    except Exception as e:
        print(e)
    finally:
        print(f'Process {os.getpid()} handled {i} requests {datetime.datetime.now().time()}')

    print(f'Shutting down process {os.getpid()}')


def start_server(samples, client_socket):
    for i in range(processes_count):
        c = Classifier(samples, client_socket)
        c.start()
        '''
        process = Process(target=process_requests, args=(samples, predictions))
        process.daemon = True
        process.start()
        '''


def kill_all_processes():
    for i in range(processes_count):
        samples.put(None)
    predictions.put(None)


def report_predictions(predictions, client):
    while True:
        try:
            prediction = predictions.get()

            if prediction is None:
                break

            client.sendall(prediction)
        except Exception as e:
            print(e)


def lister_to_incoming_requests():
    sckt = socket.socket()
    host = socket.gethostname()
    port = 12345
    sckt.bind((host, port))
    sckt.listen(5)
    client_socket, client_address = sckt.accept()

    try:
        print('Parent id: ', os.getpid())
        for i in range(10):
            process = Process(target=process_requests, args=(samples, client_socket))
            process.daemon = True
            process.start()

        print('Ready')
        while True:
            receiving_buffer = client_socket.recv(2048)
            if receiving_buffer == b'':
                break

            samples.put(receiving_buffer)
    except Exception as e:
        print(e)
    finally:
        print('close socket ', datetime.datetime.now().time())
        client_socket.close()
        #kill_all_processes()
        print('done')


if __name__ == '__main__':
    #start_server()
    lister_to_incoming_requests()
