from providers import model_provider
from utils.timeit import timeit
import numpy as np
import socket

model = model_provider.load()


@timeit
def precess_request(buffer):
    sample = np.ndarray(buffer=buffer, shape=(1, 2, 128, 1), dtype=np.float64)
    return model.predict(sample)


def start_server():
    sckt = socket.socket()
    host = socket.gethostname()
    port = 12345
    sckt.bind((host, port))
    sckt.listen(5)
    client_socket, client_address = sckt.accept()
    print('classifier ready')

    while True:
        receiving_buffer = client_socket.recv(2048)
        if not receiving_buffer:
            break

        prediction = precess_request(receiving_buffer)
        client_socket.send(prediction)

    client_socket.close()


if __name__ == '__main__':
    start_server()
