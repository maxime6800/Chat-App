import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 12345

# List to keep track of connected clients
clients = []

# File to save chat messages
CHAT_LOG_FILE = "chat_log.txt"

# Function to handle individual client connections
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received message: {message}")
                save_message(message)
                broadcast(message, client_socket)
            else:
                remove(client_socket)
        except:
            continue

# Function to broadcast messages to all clients
def broadcast(message, connection):
    for client in clients:
        if client != connection:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove(client)

# Function to remove clients
def remove(connection):
    if connection in clients:
        clients.remove(connection)

# Function to save message to a file
def save_message(message):
    with open(CHAT_LOG_FILE, 'a') as f:
        f.write(message + '\n')

# Main function to start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(100)
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        clients.append(client_socket)
        print(f"Connection established with {client_address}")

        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
