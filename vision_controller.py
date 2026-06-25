# En este modulo se define el controlador de vision de R.E.D. optimizado para KDE Wayland

import subprocess
import os

def take_screenshot(filename="snapshot.png"):
    """
    Captura todas las pantallas activas usando el motor nativo de KDE (Spectacle) entornos Wayland.
    """
    print("[*] R.E.D. esta escaneando tus monitores...")
    
    try:
        #LLAMA A SPECTACULE Y TOMA UNA CAPTURA EN TODOS LOS MONITORES.
        # -b: Lanza en segundo plano (background)
        # -n: No abre la interfaz grafica de Spectacle
        # -o: Guarda directamente en la ruta especificada

        command = ["spectacle", "-b", "-n", "-o", filename]
        
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists(filename):
            print(f"[+] Captura de pantalla guardada {filename}")
            return True
        else:
            print("[-] Error: El archivo de imagen no fue generado.")
            return False
            
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"[-] Fallo en driver de vision: {e}")
        return False
