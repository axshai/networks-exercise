"""EX 2.6 protocol implementation
   Author:Shai Axelrod
   Date:23/10/2021
"""
import datetime
import random

LENGTH_FIELD_SIZE = 2
PORT = 8820


def check_cmd(data):
    """
    Check if the command is defined in the protocol (e.g RAND, NAME, TIME, EXIT)
    :param data: the command
    :return: true if the command is defined in the protocol, false otherwise
    """
    return data in ('RAND', 'WHORU', 'TIME', 'EXIT')


def create_msg(data):
    """
    Create a valid protocol message, with length field
    :param data: the raw message
    :return:valid protocol message, with length field
    """
    length = str(len(data))
    zfill_length = length.zfill(2)
    data = zfill_length + data
    return data


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    :param my_socket: the socket with the data
    :return: the message from protocol, without the length field and true, or False,
    "Error" if length field does not include a number
    """
    length = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    if not length.isdigit():
        return False, "Error"
    data = my_socket.recv(int(length)).decode()
    return True, data


def create_server_rsp(command):
    """
    Based on the command, create a proper response
    :param command: the command from the client
    :return:the proper response
    """
    if command == "EXIT":
        return ""
    elif command == "TIME":
        return datetime.datetime.now().time().__str__()
    elif command == "WHORU":
        return "shai's server"
    else:
        return str(random.randint(0, 10))
