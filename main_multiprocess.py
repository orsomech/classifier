import multiprocessing
import socket
import os


def handle(connection, address):
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break

            connection.sendall(bytearray(f'{data} {os.getpid()}', encoding='utf-8'))
    except Exception as e:
        print(e)
    finally:
        connection.close()


class Server(object):
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        i = os.cpu_count()


        while True:
            conn, address = self.socket.accept()
            for i in range(os.cpu_count()):
                process = multiprocessing.Process(target=handle, args=(conn, address))
                process.daemon = True
                process.start()
                print(process.pid)

if __name__ == "__main__":
    server = Server("127.0.0.1", 9000)
    try:
        server.start()
    except Exception as e:
        print(e)
    finally:
        for process in multiprocessing.active_children():
            print(process.pid)
            process.terminate()
            process.join()
