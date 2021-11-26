#   Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020
import os
import shutil
import socket
import subprocess
import pyautogui
import protocol27

IP = "0.0.0.0"
PORT = 8820
PHOTO_PATH = r"C:\sphoto.jpg"  # The path + filename where the screenshot at the server should be saved


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.
    For example, the filename to be copied actually exists
    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """

    # Use protocol.check_cmd first
    splited_cmd = cmd.split()
    if not protocol27.check_cmd(cmd):
        return False, splited_cmd[0], splited_cmd[1:]
    if splited_cmd[0] == "DIR":
        return os.path.isdir(splited_cmd[1]), "DIR", splited_cmd[1:]
    elif splited_cmd[0] == "DELETE" or splited_cmd[0] == "EXECUTE":
        valid_parm = os.path.isfile(splited_cmd[1])
        return valid_parm, splited_cmd[0], splited_cmd[1:]
    elif splited_cmd[0] == "COPY":
        valid_parm1 = os.path.isfile(splited_cmd[1])
        if "\\" in splited_cmd[2]:
            valid_parm2 = os.path.isdir(splited_cmd[2][:splited_cmd[2].rindex("\\")])
        else:
            valid_parm2 = False
        return valid_parm1 and valid_parm2, splited_cmd[0], splited_cmd[1:]
    else:
        return True, splited_cmd[0], splited_cmd[1:]


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data

    """
    if command == "DIR":
        if "\n".join(os.listdir(params[0])).isascii():
            return "\n".join(os.listdir(params[0]))
        else:
            return "Did not succeed"
    elif command == "DELETE":
        try:
            os.remove(params[0])
            return "Succeeded"
        except Exception as e:
            return "Did not succeed: ".format(e)
    elif command == "COPY":
        try:
            shutil.copy(params[0], params[1])
            return "Succeeded"
        except Exception as e:
            return "Did not succeed: ".format(e)
    elif command == "EXECUTE":
        try:
            subprocess.call(params[0])
            return "Succeeded"
        except Exception as e:
            return "Did not succeed: ".format(e)
    elif command == "TAKE_SCREENSHOT":
        try:
            image = pyautogui.screenshot()
            image.save(PHOTO_PATH)
            return "Succeeded"
        except Exception as e:
            return "Did not succeed: ".format(e)
    elif command == "EXIT":
        return ""
    else:
        return os.path.getsize(r"C:\sphoto.jpg")

    # (7)


def main():
    # open socket with client
    server_socket = socket.socket()
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")
    # (1)

    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol27.get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:
                if command != 'SEND_PHOTO':
                    response = handle_client_request(command,
                                                     params)  # prepare a response using "handle_client_request"
                    msg = protocol27.create_msg(response)
                else:
                    if not os.path.isfile(PHOTO_PATH):
                        response = "you didn't take screenshot yet"
                        msg = protocol27.create_msg(response)
                    else:
                        size = handle_client_request(command, params)
                        response = protocol27.create_msg(str(size))
                        with open(PHOTO_PATH, 'rb') as input_file:
                            msg = response + input_file.read()
                if command == 'EXIT':
                    break
            else:
                # prepare proper error to client
                response = 'Bad command or parameters'
                msg = protocol27.create_msg(response)
            client_socket.send(msg)

        else:
            # prepare proper error to client
            response = 'Packet not according to protocol'
            msg = protocol27.create_msg(response)
            client_socket.send(msg)

            # Attempt to clean garbage from socket
            client_socket.recv(1024)

    client_socket.close()
    server_socket.close()
    print("Closing connection")


if __name__ == '__main__':
    main()
