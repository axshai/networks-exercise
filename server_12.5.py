import socket
import select
MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = "0.0.0.0"
print("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("Listening for clients...")
client_sockets = []
messages_to_send = []
listeners=[]
while True:
    rlist, wlist, xlist = select.select([server_socket] + client_sockets,  client_sockets, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)
        else:
            data = current_socket.recv(MAX_MSG_LENGTH).decode()
            if data == "":
                print("Connection closed", )
                client_sockets.remove(current_socket)
                current_socket.close()
            else:
                print("i recived "+data)
                messages_to_send.append((current_socket, data,[i for i in client_sockets if not (i is current_socket)]))

    for message in messages_to_send:
        current_socket, data ,listeners= message
        for sock in listeners:
            if sock in wlist:
                sock.send(("someone sent "+data).encode())
                listeners.remove(sock)
        if listeners == []:
            messages_to_send.remove(message)