import socket
my_input=""
my_socket = socket.socket()
my_socket.connect(("127.0.0.1", 8820))

def find_len(message):
    length = str(len(message))
    zfill_length = length.zfill(2)
    message = zfill_length + message
    return message

while True:
    my_input=input("enter your request\n")

    my_socket.send(find_len(my_input).encode())
    length=my_socket.recv(2).decode()
    data = my_socket.recv(int(length)).decode()
    print("The server sent: " + "'"+data+"'")
    if my_input=="EXIT":
        break
my_socket.close()

