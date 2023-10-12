import socket
import threading
import json
import os
import base64

# Server configuration
HOST = '127.0.0.1' # Loopback address for localhost
PORT = 12345 # Port to listen on
# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the specified address and port
server_socket.bind((HOST, PORT))
# Listen for incoming connections
server_socket.listen()
print(f"Server is listening on {HOST}:{PORT}")


def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    while True:
        try:
            message = json.loads(client_socket.recv(100000).decode())
        except:
            break # Exit the loop when the client disconnects
        print("from " + str(client_address) + " message type: " + message["type"])
        # Broadcast the message to all clients
        for client in clients:
            if client != client_socket and message["type"] == "message": # find alternative to this IF
                data = json.dumps(message)
                client.send(data.encode())
            
            # client uploads a file
            elif message["type"] == 'upload':
                save_path = './server_media/'

                # upload txt file
                if message["payload"]["extension_type"] == 'txt':
                    complete_name = os.path.join(save_path, message["payload"]["file_name"])
                    with open(complete_name, "w") as f:
                        f.write(message["payload"]["contents"])

                # upload image
                elif message["payload"]["extension_type"] == 'jpg':
                    complete_name = os.path.join(save_path, message["payload"]["file_name"])
                    with open(complete_name, "wb") as f:
                        f.write(base64.b64decode(message["payload"]["contents"]))

            # handle download
            elif message["type"] == 'download':
                file_path = './server_media/'
                complete_name = os.path.join(file_path, message["payload"]["file_name"])

                file_json = message
                if os.path.isfile(complete_name):
                    if complete_name.endswith('.txt'):
                        with open(complete_name, 'r') as file:
                            file_json["payload"]['contents'] = file.read()
                    elif complete_name.endswith('.jpg'):
                        with open(complete_name, 'rb') as file:
                            file_json["payload"]['contents'] = base64.b64encode(file.read()).decode("utf-8")

                else:
                    message["payload"]["file_name"] = 'n/a'
                

                data = json.dumps(file_json)
                client.send(data.encode())
                


    # Remove the client from the list
    clients.remove(client_socket)
    client_socket.close()

clients = []

while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    # Start a thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()