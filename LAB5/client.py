import socket
import threading
import json
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

# Send the message to the server
data = json.dumps(client_server_json)
client_socket.send(data.encode())

while True:
 
    input_message = input("Enter 'message' to write a message or 'exit' to quit): ")
    if input_message == 'message':        
        message_json["payload"]["message"] = input("Enter a message: ")
        data = json.dumps(message_json)
        client_socket.send(data.encode())
        
    if input_message == 'exit':
        data = json.dumps(exit_json)
        client_socket.send(data.encode())
        break

    

# Close the client socket when done
client_socket.close()