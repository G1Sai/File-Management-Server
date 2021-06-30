import socket
import threading

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 8088



def receiver():
    while True:   
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))

def server():
    while True:
        ClientSocket.send(str.encode(input()))

try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

t = threading.Thread(target=receiver)

t.start()

server()

ClientSocket.close()