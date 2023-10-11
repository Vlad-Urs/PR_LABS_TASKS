import socket
import threading
import json
import base64
import os
from PIL import Image


# Server configuration
HOST = '127.0.0.1' # Server's IP address
PORT = 12345 # Server's port
# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

client_socket.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")
# Function to receive and display messages
def receive_messages():
    while True:
        message = json.loads(client_socket.recv(1024).decode('utf-8'))
        if not message:
            break # Exit the loop when the server disconnects
        if message["type"] == 'message':
            print('got here')
            print(f"{message['payload']['name']} : {message['payload']['message']}")


receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True # Thread will exit when the main program exits
receive_thread.start()

name = input("enter a client's name: ")
room = input("enter a clients's room: ")

client_server_json = {
    "type" : "connect",
    "payload" : {
        "name" : name,
        "room" : room
    }
}

message_json ={
    "type" : "message",
    "payload" : {
        "name" : name,
        "message" : ''
    }
}

exit_json = {
    "type" : "exit",
    "payload" : {
        "name" : name,
        "message" : ''
    }
}

file_json = {
    "type" : "upload",
    "payload" : {
        "user_name" : name,
        "file_name" : '',
        "extension_type" : '',
        "contents" : None
    }
}

# Send the message to the server
data = json.dumps(client_server_json)
client_socket.send(data.encode())

while True:
 
    input_message = input("Enter 'message' for message, 'upl' for upload, 'dwn' for download, 'exit' to quit): ")
    if input_message == 'message':        
        message_json["payload"]["message"] = input("Enter a message: ")
        data = json.dumps(message_json)
        client_socket.send(data.encode())
    
    elif input_message == 'upl':
        path = input('Provide path for file: ')
        file_name = input('Provide file name: ')
        complete_name = os.path.join(path, file_name)
        if os.path.isfile(complete_name):
            
            # upload txt file
            if complete_name.lower().endswith('.txt'):

                f = open(complete_name, 'r')
                file_json["payload"]["extension_type"] = 'txt'
                file_json["payload"]["contents"] = f.read()
                file_json["payload"]["file_name"] = file_name
                f.close()
                data = json.dumps(file_json)
                client_socket.send(data.encode())


            # upload image
            if complete_name.lower().endswith('.jpg'):

                
                with open(complete_name, "rb") as image_file:
                    image_bytes = base64.b64encode(image_file.read()).decode("utf-8")

                file_json["payload"]["extension_type"] = 'txt'
                file_json["payload"]["contents"] = image_bytes
                file_json["payload"]["file_name"] = file_name

                data = json.dumps(file_json)
                client_socket.send(data.encode())

        else:
            print('The path provided is incorrect or the file does not exist')
        
    elif input_message == 'exit':
        data = json.dumps(exit_json)
        client_socket.send(data.encode())
        break

    

# Close the client socket when done
client_socket.close()