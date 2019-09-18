import socket

sock = socket.socket()
sock.connect(('127.0.0.1', 9001))

word = str(input())
if word == 'stop':
    sock.close()
sock.send(word.encode())

time = sock.recv(1024).decode()
sock.close()

print(time)






