import socket
my_input=""
my_socket = socket.socket()
my_socket.connect(("127.0.0.1", 8820))

while True:
    my_input=input("enter your request\n")
    my_socket.send(my_input.encode())
    length=my_socket.recv(2).decode()
    data = my_socket.recv(int(length)).decode()
    print("The server sent: " + "'"+data+"'")
    if my_input=="EXIT":
        break
my_socket.close()

