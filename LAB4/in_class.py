import socket
import signal
import sys
import threading
from time import sleep
import json


# Define the server's IP address and port
HOST = '127.0.0.1' # IP address to bind to (localhost)
PORT = 8080 # Port to listen on
# Create a socket that uses IPv4 and TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the address and port
server_socket.bind((HOST, PORT))
# Listen for incoming connections
server_socket.listen(5) # Increased backlog for multiple simultaneous connections
print(f"Server is listening on {HOST}:{PORT}")
# Function to handle client requests


def handle_request(client_socket):
# Receive and print the client's request data
    request_data = client_socket.recv(1024).decode('utf-8')
    print(f"Received Request:\n{request_data}")
    # Parse the request to get the HTTP method and path
    request_lines = request_data.split('\n')
    request_line = request_lines[0].strip().split()
    method = request_line[0]
    path = request_line[1]
    # Initialize the response content and status code
    response_content = ''
    status_code = 200

    with open('products.json', 'r') as json_file:
        json_load = json.load(json_file)

    # Define a simple routing mechanism
    if path == '/':
        response_content = '''<h1>Home</h1>
        <a href = /products><br><br>Products</a>
        <a href = /about><br><br>About us</a>
        <a href = /contacts><br><br>Contacts</a>
        '''
    elif path == '/products':
        response_content = '<h1>Products:</h1>'
        page = 1
        for product in json_load:
            pr_name = product['name']
            response_content += f'<a href = /prod{page}>{pr_name}</a><br>'
            page += 1
        response_content += '<a href = /><br><br>Home</a>'
    elif path == '/prod1':
        for key in json_load[0]:
            response_content += key + ' : ' + str(json_load[0][key]) + '<br>'
        response_content += '<a href = /products><br><br>Products</a>'
    elif path == '/prod2':
        for key in json_load[1]:
            response_content += key + ' : ' + str(json_load[1][key]) + '<br>'
        response_content += '<a href = /products><br><br>Products</a>'
    elif path == '/about':
        response_content = '''This is the About page.
        <br>
        <a href = /><br><br>Home</a>
        '''
    elif path == '/contacts':
        response_content = '''Contacts:
        <br>
        tel: 0953087890 <br>
        email: something@gmail.com
        <a href = /><br><br>Home</a>
        '''
    else:
        response_content = '404 Not Found'
        status_code = 404
    # Prepare the HTTP response
    response = f'HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_content}'
    client_socket.send(response.encode('utf-8'))
    # Close the client socket
    client_socket.close()


def signal_handler(sig, frame):
    print("\nShutting down the server...")
    server_socket.close()
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)
while True:
    # Accept incoming client connections
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    # Create a thread to handle the client's request
    client_handler = threading.Thread(target=handle_request, args=(client_socket,))
    client_handler.start()