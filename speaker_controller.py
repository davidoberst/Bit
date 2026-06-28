import os
import subprocess
from gtts import gTTS #ai voice
import time

def hablar(texto):
    """
    Convierte el texto recibido en voz humana (femenina) y la reproduce en Arch.
    """
    if not texto:
        return
        
    filename = "voice_response.mp3"
    print("[*] R.E.D. está vocalizando la respuesta...")
    
    try:
        # 1. Pasar el texto a gTTS. El lenguaje 'es' usa por defecto la voz femenina.

        tts = gTTS(text=texto, lang='es', slow=False) #idioma español latino
        
        # 2. Guardar el archivo de audio temporal
        tts.save(filename)
        
        # 3. Reproducir el audio usando mpv de forma silenciosa en la terminal
        # --no-video: Asegura que no intente abrir ventanas flotantes
        # check=True: Espera a que termine de hablar antes de seguir
        subprocess.run(
            ["mpv", "--no-video","--speed=1.8", filename], 
            check=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        
        # 4. Limpieza: Borrar el archivo mpv temporal para no dejar basura en el proyecto
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        print(f"[-] Error en el controlador de voz: {e}")

# Banco de pruebas local rápido
if __name__ == "__main__":
    hablar("Hola Juan. Conexión de audio establecida con éxito. Estoy lista para operar.")