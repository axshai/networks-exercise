#   Ex. 2.7 template - client side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020


import socket
import protocol27

IP = "127.0.0.1"
PORT = 8820
SAVED_PHOTO_LOCATION = r"C:\clientsphotos\photo.jpg"  # The path + filename where the copy of the screenshot at


# the client should be saved


def handle_server_response(my_socket, cmd):
    validation, data = protocol27.get_msg(my_socket)
    if not validation:
        print("Response not valid\n")
        return
    if cmd != "SEND_PHOTO":
        print(data)
    else:
        photo = my_socket.recv(int(data))
        with open(SAVED_PHOTO_LOCATION, 'wb') as file:
            file.write(photo)


def main():
    my_socket = socket.socket()
    my_socket.connect((IP, PORT))

    # (2)

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    while True:
        cmd = input("Please enter command:\n")
        if protocol27.check_cmd(cmd):
            packet = protocol27.create_msg(cmd)
            my_socket.send(packet)
            if cmd == 'EXIT':
                break
            handle_server_response(my_socket, cmd)

        else:
            print("Not a valid command, or missing parameters\n")

    my_socket.close()


if __name__ == '__main__':
    main()
