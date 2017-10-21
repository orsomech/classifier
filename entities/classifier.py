import multiprocessing
import datetime
import numpy as np
import os
import entities.classification_request.ClassificationRequest
import entities.classification_response.ClassificationResponse


class Classifier(multiprocessing.Process):
    def __init__(self, model_provider, samples, client_socket):
        multiprocessing.Process.__init__(self)
        self.model_provider = model_provider
        self.samples = samples
        self.client_socket = client_socket

    def run(self):
        model = self.model_provider.load()
        i = 0

        while True:
            try:
                buffer = self.samples.get()
                if buffer == b'':
                    break

                buffer = np.ndarray(buffer=buffer, shape=(1, 2, 128, 1), dtype=np.float64)
                prediction = model.predict(buffer)

                self.client_socket.send(np.ndarray.max(prediction))
                i += 1
            except Exception as e:
                print(e)

        print(f'Process {os.getpid()} handled {i} requests {datetime.datetime.now().time()}')
