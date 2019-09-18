import socket
import threading
from multiprocessing import Process
import time


class Server:
    def __init__(self, conn):
        self.conn = conn

    @staticmethod
    def hours():
        return time.strftime('Hour: %H', time.localtime())

    @staticmethod
    def minutes():
        return time.strftime('Minutes: %M', time.localtime())

    @staticmethod
    def seconds():
        return time.strftime('Seconds: %S', time.localtime())

    def time(self, word):
        if word == 'hour':
            self.conn.sendall(self.hours().encode())
        elif word == 'minute':
            self.conn.sendall(self.minutes().encode())
        elif word == 'second':
            self.conn.sendall(self.seconds().encode())
        else:
            self.conn.sendall('ERROR'.encode())

    def receiver(self):
        while True:
            try:
                word = self.conn.recv(1024).decode()
            except socket.timeout:
                print("close connection by timeout")
                break
            try:
                self.time(word)
            except socket.timeout:
                print("send data timeout")
            except socket.error as ex:
                print("send data error:", ex)
            if not word:
                break


def main_server():
    sock = socket.socket()  # создаем сокет

    sock.bind(("127.0.0.1", 9001))
    sock.listen(3)
    conn, addr = sock.accept()
    conn.settimeout(5.0)

    sockets = [conn]

    for i in sockets:
        Server(i).receiver()

    conn.close()
    sock.close()


def main_thread():
    t1 = threading.Thread(target=main_server())
    t2 = threading.Thread(target=main_server())
    t3 = threading.Thread(target=main_server())

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()


def main():
    p_one = Process(target=main_thread())
    p_two = Process(target=main_thread())

    p_one.start()
    p_two.start()

    p_one.join()
    p_two.join()


if __name__ == '__main__':
    main()
