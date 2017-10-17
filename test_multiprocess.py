import socket               # Import socket module
import numpy as np
from utils.timeit import timeit
from threading import _start_new_thread
import random


payload = np.ndarray(10)

@timeit
def send_requests(socket):
    pl = bytearray('test', encoding='utf-8')
    socket.sendall(pl)
    print(socket.recv(1024))


port = 9000                 # Reserve a port for your service.

try:
    for i in range(20):

        s = socket.socket()  # Create a socket object
        s.connect(("127.0.0.1", port))

        send_requests(s)
        #_start_new_thread(lambda x: send_requests(s), (payload.tobytes(),))

finally:
    s.shutdown(socket.SHUT_WR)
    s.close()

