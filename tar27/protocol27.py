#   Ex. 2.7 template - protocol


LENGTH_FIELD_SIZE = 4
PORT = 8820


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE C:\work\file.txt is good, but DELETE alone is not
    """
    if data == "":
        return False
    splited_data = data.split()
    dir_del_exe_valid = splited_data[0] in ["DIR", "DELETE", "EXECUTE"] and len(splited_data) == 2
    dir_del_exe_valid = dir_del_exe_valid and splited_data[1].isascii()
    copy_valid = splited_data[0] == "COPY" and len(splited_data) == 3 and splited_data[1].isascii()
    copy_valid = copy_valid and splited_data[2].isascii()
    shot_exit_valid = data in ["TAKE_SCREENSHOT", "EXIT", "SEND_PHOTO"]
    return dir_del_exe_valid or shot_exit_valid or copy_valid


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """
    length = str(len(data))
    zfill_length = length.zfill(LENGTH_FIELD_SIZE)
    data = zfill_length + data
    return data.encode()
    # (4)


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    length = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    if not length.isdigit():
        return False, "Error"
    data = my_socket.recv(int(length)).decode()
    return True, data
