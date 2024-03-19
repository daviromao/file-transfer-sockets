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


def handle_send_file():
    pass

def handle_download_file():
    pass


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
        handle_download_file()
        
    elif request_type == SEND_FILE :
        handle_send_file()
            
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
    
