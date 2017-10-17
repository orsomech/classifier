import multiprocessing
import numpy as np
from utils.fileit import write_to_file


class Consumer(multiprocessing.Process):
    def __init__(self, model, samples, predictions):
        multiprocessing.Process.__init__(self)
        self.model = model
        self.samples = samples
        self.predictions = predictions

    def run(self):
        proc_name = self.name
        while True:
            buffer = self.samples.get()
            if buffer is None:
                #self.samples.task_done()
                break

            sample = np.ndarray(buffer=buffer, shape=(1, 2, 128, 1), dtype=np.float64)
            prediction = self.model.predict(sample)
            #write_to_file(str(self.getpid()), str(prediction))
            #self.samples.task_done()
            self.predictions.put(prediction)
        return


