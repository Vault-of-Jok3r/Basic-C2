import os
import win32com.client

def create_shortcut():
    # Récupère le chemin du dossier "Startup"
    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    
    # Spécifie le chemin vers l'image à ouvrir
    image_path = r"C:\Users\ldard\Bureau\Codes\Joker_Avatar.jpg"
    
    # Commande pour ouvrir l'image avec l'application Photos
    target_program = "cmd.exe"
    arguments = f'/c start "" "{image_path}"'

    # Crée un raccourci
    shortcut_name = "OuvrirImagePhotos.lnk"
    shell = win32com.client.Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(os.path.join(startup_folder, shortcut_name))
    shortcut.TargetPath = target_program
    shortcut.Arguments = arguments
    shortcut.WorkingDirectory = os.path.dirname(image_path)
    shortcut.IconLocation = image_path
    shortcut.save()

    print(f"Le raccourci pour ouvrir l'image avec Photos a été ajouté au démarrage sous : {startup_folder}")

if __name__ == "__main__":
    create_shortcut()