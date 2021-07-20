import socket
import select
import msvcrt

my_socket = socket.socket()
my_socket.connect(("127.0.0.1", 5555))
message=""
key=""
print("enter your messages")
while True:
    if msvcrt.kbhit():
        key = msvcrt.getch().decode()
        if key!="\r":
            print(key,end="")
            message += key
        else:
            if message=="exit":
                break
            my_socket.send(message.encode())
            message = ""
            key = ""
            print("\nenter your messages")
    rlist, wlist, xlist = select.select([my_socket] ,[], [],0)
    if len(rlist) != 0:
        data = my_socket.recv(1024).decode()
        print(data)

my_socket.close()