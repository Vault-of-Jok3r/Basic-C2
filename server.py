#Coté server / besoin de socket uniquement - regarder librairie socket y'a un mot clé

import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9999


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(10)
    print(f"Serveur démarré sur {SERVER_HOST}:{SERVER_PORT}...")

    while True:
        client_socket, client_addr = server_socket.accept()
        print(f"Connexion de {client_addr}")
        handle_client(client_socket)

def handle_client(client_socket):
    while True:
        command = input(f"client_socket {client_socket.getpeername()} > ")
        client_socket.send(command.encode())
        if command.lower() == 'exit':
            break
        print(client_socket.recv(4096).decode())
        
    client_socket.close()

if __name__ == "__main__":
    start_server()
