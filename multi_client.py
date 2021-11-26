import socket

my_socket = socket.socket()
my_socket.connect(("127.0.0.1", 5555))
while True:
    message=input("enter your message\n")
    if message == '':
        break
    my_socket.send(message.encode())
    data = my_socket.recv(1024).decode()
    print(data)
my_socket.close()