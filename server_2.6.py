import socket
import datetime
import random
#import datetime.datetime.now().time()

def find_len(message):
    length = str(len(message))
    zfill_length = length.zfill(2)
    message = zfill_length + message
    return message

server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 8820))
server_socket.listen()
print("Server is up and running")
(client_socket, client_address) = server_socket.accept()
print("Client connected")
while True:
    data = client_socket.recv(4).decode()
    if data == "EXIT":
        client_socket.send(find_len("bye").encode())
        break
    elif data == "TIME":
        client_socket.send(find_len(datetime.datetime.now().time().__str__()).encode())
    elif data == "WHOR":
        client_socket.send(find_len("shai's server").encode())
    elif data == "RAND":
        client_socket.send(find_len(str(random.randint(0,10))).encode())
    else:
        client_socket.send(find_len("wromg protocol").encode())
client_socket.close()
server_socket.close()
