# En este modulo se define el controlador de vision de R.E.D. optimizado para KDE Wayland y XFCE

import subprocess
import os
import time

def take_screenshot(filename="snapshot.jpg"):
    """
    Captura TODOS los monitores activos usando el comando adecuado según el entorno (Spectacle o XFCE Screenshooter),
    optimizado en JPEG para transmisión rápida.
    """
    print("[*] R.E.D. esta escaneando tus monitores...")
    
    # Detectar el entorno de escritorio actual
    desktop_session = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    
    try:
        if "xfce" in desktop_session:
            # COMANDO PARA XFCE:
            # -f: Captura toda la pantalla (todos los monitores)
            # -s: Guarda directamente en la ruta especificada sin abrir la interfaz
            command = ["xfce4-screenshooter", "-f", "-s", filename]
        else:
            # COMANDO PARA wayland:
            # -b: Lanza en segundo plano (background)
            # -n: No abre la interfaz grafica de Spectacle
            # -o: Guarda directamente en la ruta especificada
            command = ["spectacle", "-b", "-n", "-o", filename]
        
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists(filename):
            print(f"[+] Captura de pantalla guardada en {filename}")
            return True
        else:
            print("[-] Error: El archivo de imagen no fue generado.")
            return False
            
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"[-] Fallo en driver de vision: {e}")
        return False