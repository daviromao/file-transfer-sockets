import os
from socket import socket, AF_INET, SOCK_STREAM
from constants import *

# HOST = '172.20.8.236'
# PORT = 9999
user_folder = os.path.expanduser("~")


def get_file_list(HOST: str, PORT: int):
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((HOST, PORT))

    request_type = FILE_LIST.to_bytes(1, byteorder='big')
    client.send(request_type)

    data = b""

    while buffer := client.recv(1024):
        data += buffer
    files = data.decode("utf-8")
    return files


def download_file(filename, HOST: str, PORT: int):
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((HOST, PORT))

    request_type = DOWNLOAD_FILE.to_bytes(1, byteorder='big')
    client.send(request_type)

    client.send(filename.encode("utf-8"))

    download_folder = os.path.join(user_folder, "Downloads")
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    filepath = os.path.join(download_folder, filename)

    with open(filepath, 'wb') as file:
        buffer = client.recv(1024)
        while buffer:
            file.write(buffer)
            buffer = client.recv(1024)

    client.close()


def send_file(filepath, HOST: str, PORT: int):
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((HOST, PORT))

    request_type = SEND_FILE.to_bytes(1, byteorder='big')
    client.send(request_type)

    filename = filepath.split("/")[-1]
    filename_size = len(filename).to_bytes(length=4, byteorder='big')

    client.send(filename_size)
    client.send(filename.encode("utf-8"))

    with open(filepath, "rb") as file:
        buffer = file.read(1024)
        while (buffer):
            client.send(buffer)
            buffer = file.read(1024)

    client.close()
