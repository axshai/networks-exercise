# Ex 4.4 - HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

# TO DO: import modules

# TO DO: set constants
import os
import socket
IP = "0.0.0.0"
PORT = 80
DEFAULT_URL = r"C:\Users\User\Desktop\forpy\webroot\index.html"
ROOT_DIR = r"C:\Users\User\Desktop\forpy\webroot"
SOCKET_TIMEOUT = 3
REDIRECTION_DICTIONARY = {r"imgs/abstract.jpg": r"uploads/abstract.jpg"}
FORBIDEN_LIST = [r"imgs/blocked_pic.jpg"]


def get_file_data(filename, filetype):
    if filetype == 'jpg' or "css":
        with open(filename, 'rb') as file_to_send:
            return file_to_send.read()
    else:
         with open(filename, "r", encoding='utf-8') as file_to_send:
            return file_to_send.read().encode(encoding='utf-8')


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response
    if resource == '':
        url = DEFAULT_URL
    else:
        url = ROOT_DIR + "\\" + resource
    if resource == "error":
        client_socket.send("HTTP/1.1 500 Internal Server Error\r\n\r\n".encode())
    elif resource in REDIRECTION_DICTIONARY:
        client_socket.send(("HTTP/1.1 302 Found\r\n" + "location: /" + REDIRECTION_DICTIONARY[resource] + "\r\n\r\n").encode())
    elif not os.path.isfile(url):
        client_socket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
    elif resource in FORBIDEN_LIST:
        client_socket.send("HTTP/1.1 403 Forbidden\r\n\r\n".encode())
    else:
        http_header = "HTTP/1.1 200 OK\r\n"
        filetype = url[url.rfind(".")+1:]
        if filetype == 'html':
            http_header += "Content-Type: text/html; charset=utf 8\r\n"
        elif filetype == 'jpg':
            http_header += "Content-Type: image/jpeg\r\n"
        elif filetype == 'js':
            http_header += "Content-Type: application/javascript\r\n"
        elif filetype == 'css':
            http_header += "Content-Type: text/css\r\n"
        http_header += "Content-Length: " + str(os.path.getsize(url)) + "\r\n\r\n"
        data = get_file_data(url, filetype)
        http_response = http_header.encode() + data
        client_socket.send(http_response)


def validate_http_request(request):
    """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """
    client_req = request.split("\n")
    first_line = client_req[0].split(" ")
    validation = len(first_line) == 3 and first_line[0] == "GET" and first_line[2] == "HTTP/1.1\r"
    if len(client_req) > 2:
        for line in client_req[1:-2]:
            splited_line = line.split(":")
            validation = validation and splited_line[-1][-1] == '\r'
        validation = validation and client_req[-2] == "\r" and client_req[-1] == ""
    else:
        validation = False
    url = first_line[1][1:] if validation else "error"
    return validation, url


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    while True:
        client_request = client_socket.recv(1024).decode()
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            print('Error: Not a valid HTTP request')
            handle_client_request(resource, client_socket)
    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        try:
            client_socket.settimeout(SOCKET_TIMEOUT)
            handle_client(client_socket)
        except:
            continue


if __name__ == "__main__":
    # Call the main handler function
    main()
