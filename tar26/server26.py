"""EX 2.6 server implementation
   Author:Shai Axelrod
   Date:22/10/2021
"""

import socket
import protocol


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    while True:
        # Get message from socket and check if it is according to protocol
        valid_msg, cmd = protocol.get_msg(client_socket)
        if valid_msg:
            print("your message was: " + cmd)
            valid_cmd = protocol.check_cmd(cmd)
            if valid_cmd:
                response = protocol.create_server_rsp(cmd)
            else:
                response = "Wrong command"
        else:
            response = "Wrong protocol"
            client_socket.recv(1024)  # Attempt to empty the socket from possible garbage
        if response == "":
            break
        client_socket.send(protocol.create_msg(response).encode())

    print("Closing\n")
    # Close sockets
    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    main()
