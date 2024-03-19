from socket import socket, AF_INET, SOCK_STREAM
from constants import *

HOST = ''
PORT = 9999

def get_file_list():
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((HOST, PORT))
    request_type = FILE_LIST.to_bytes(1, byteorder='big')
    client.send(request_type)
    
    data = b""
    
    while buffer := client.recv(1024):
        data += buffer
    files = data.decode("utf-8")
    return files
