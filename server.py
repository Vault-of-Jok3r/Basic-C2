import socket
import subprocess

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9999

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(10)
    print(f"Serveur démarré sur {SERVER_HOST}:{SERVER_PORT}...")

    while True:
        try:
            client_socket, client_addr = server_socket.accept()
            print(f"Connexion de {client_addr}")
            handle_client(client_socket)
        except KeyboardInterrupt:
            print("\nServeur interrompu.")
            break
        except Exception as e:
            print(f"Erreur serveur: {e}")
            break

def handle_client(client_socket):
    while True:
        command = input("Entrez une commande ('screenshot', 'portscan', 'exit') : ").strip()
        
        if command.lower() == 'exit':
            client_socket.send("exit".encode())
            break

        elif command.lower() == "screenshot":
            client_socket.send("screenshot".encode())  # Envoi de la commande pour capture d'écran
            # Traitement de la capture d'écran
            response = client_socket.recv(1024).decode()
            if response == "screenshot":
                # Réception de la taille de l'image (4 octets)
                img_size = int.from_bytes(client_socket.recv(4), 'big')
                # Réception de l'image elle-même
                img_data = b""
                while len(img_data) < img_size:
                    img_data += client_socket.recv(4096)
                
                # Sauvegarder l'image reçue
                with open("screenshot.png", "wb") as img_file:
                    img_file.write(img_data)
                print("Capture d'écran reçue et sauvegardée sous 'screenshot.png'.")
        
        elif command.lower() == "portscan":
            client_socket.send("portscan".encode())  # Envoi de la commande pour scan de ports
            # Attente de la réponse du scan de ports
            response = b""
            while True:
                data = client_socket.recv(4096)
                if b"done" in data:
                    response += data.split(b"done")[0]
                    break
                response += data
            print(f"Résultats du port scan :\n{response.decode()}")
        else:
            subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    
    client_socket.close()

if __name__ == "__main__":
    start_server()
