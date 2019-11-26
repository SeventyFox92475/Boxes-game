##### CHANGE IP TO HOST IP #####

import socket

numOfClients = 0
MySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
MySocket.bind(('192.168.126.1', 10000))
print('Socket started')
MySocket.listen(5)
c, a = MySocket.accept()
print(a, 'has joined')
c1, a1 = MySocket.accept()
print(a1, 'has joined')
while True:
    msg = c.recv(1024)
    print('1', msg.decode())
    c1.send(msg)
    msg = c1.recv(1024)
    print('2', msg.decode())
    c.send(msg)
