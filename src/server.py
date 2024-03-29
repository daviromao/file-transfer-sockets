import threading
import sys
import os
import json

from socket import socket, AF_INET, SOCK_STREAM
from constants import FILE_LIST, SEND_FILE, DOWNLOAD_FILE

#constants
HOST = ''
PORT = 9999
current_directory = os.path.dirname(os.path.abspath(__file__))


def handle_send_file(connection : socket):
    get_filenamesize_byte = connection.recv(4)
    filenamesize = int().from_bytes(get_filenamesize_byte, byteorder='big')

    filename = connection.recv(filenamesize).decode("utf-8")
    directory = os.path.join(current_directory, "server_files")
    filepath = os.path.join(directory, filename)

    with open(filepath, 'wb') as file:
        buffer = connection.recv(1024)
        while buffer:
            file.write(buffer)
            buffer = connection.recv(1024)

    connection.close()

def handle_download_file(connection : socket): 
    filename = connection.recv(1024).decode("utf-8")
    path = os.path.join(current_directory, "server_files", filename)

    with open(path, 'rb') as file:
        buffer = file.read(1024)
        while(buffer):
            connection.send(buffer)
            buffer = file.read(1024)

    connection.close()

def handle_list_files(connection: socket):
    directory = os.path.join(current_directory, "server_files")
    filesname = os.listdir(directory)
    
    data = []
    
    for filename in filesname:
        data.append({
            "name": filename,
            "size": os.path.getsize(os.path.join(directory, filename))
        })

    data_json = json.dumps(data).encode("utf-8")
    print(data_json)
    connection.send(data_json)

def handle_request(connection: socket, client_address):
    print(f"Handle request from {client_address}.")
    
    request_type_byte = connection.recv(1)
    request_type = int().from_bytes(request_type_byte, byteorder='big')

    if request_type == FILE_LIST:
        handle_list_files(connection)
        
    elif request_type == DOWNLOAD_FILE :
        handle_download_file(connection)
        
    elif request_type == SEND_FILE :
        handle_send_file(connection)
            
    print(f"TCP tunnel with {client_address} closed.")
    connection.close()
    
def tcp_server():
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(10)
    
    while True:
        try:
            connection, client_address = server.accept()
            
            client_thread = threading.Thread(
                target=handle_request,
                args=(connection, client_address)
            )
            
            client_thread.start()
        except KeyboardInterrupt:
            print("Terminating server...")
            server.close()
            break


if __name__ == "__main__":
    tcp_server()
    
