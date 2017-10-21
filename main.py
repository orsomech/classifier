from providers import model_provider
from utils.timeit import timeit
import multiprocessing as mp
from multiprocessing import Process, Queue, JoinableQueue
from entities.classifier import Classifier
import os
import numpy as np
import socket
import datetime


samples = Queue()


def kill_all_classifiers(classifiers):
    for i in range(len(classifiers)):
        samples.put(None)


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
    classifiers = []
    server_socker = socket.socket()
    host = socket.gethostname()
    port = 12345
    server_socker.bind((host, port))
    server_socker.listen(5)
    client_socket, client_address = server_socker.accept()

    try:
        print('Parent id: ', os.getpid())

        for i in range(os.cpu_count()):
            classifier = Classifier(model_provider, samples, client_socket)
            classifier.daemon = True
            classifier.start()
            classifiers.append(classifier)

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
        kill_all_classifiers(classifiers)
        print('done')


if __name__ == '__main__':
    lister_to_incoming_requests()
