"""EX 2.6 client implementation
   Author:Shai Axelrod
   Date:23/10/2021
"""

import socket
import protocol


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))

    while True:
        user_input = input("Enter command\n")
        # Check if user entered a valid command as defined in protocol
        valid_cmd = protocol.check_cmd(user_input)

        if valid_cmd:
            cmd_to_send = protocol.create_msg(user_input)
            my_socket.send(cmd_to_send.encode())
            if user_input == "EXIT":
                break  # 3. If command is EXIT, break from while loop
            valid_msg, response = protocol.get_msg(my_socket)
            if valid_msg:
                print(response)
            else:
                print("Response not valid\n")
        else:
            print("Not a valid command")

    print("Closing\n")
    my_socket.close()


if __name__ == "__main__":
    main()
