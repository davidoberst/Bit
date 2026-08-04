import os
import subprocess
from gtts import gTTS #ai voice
import time

def hablar(texto):
    """
    Convierte el texto recibido en voz humana y la reproduce mostrando el texto a la par.
    """
    if not texto:
        return
        
    filename = "voice_response.mp3"
    
    try:
        # 1. Pasar el texto a gTTS
        tts = gTTS(text=texto, 
        lang='es',
        tld='com.co',
         slow=False)
        
        # 2. Guardar el archivo de audio temporal
        tts.save(filename)
        
        # 3. Lanzar mpv en un proceso asíncrono controlado
        proceso_audio = subprocess.Popen(
            ["mpv", "--no-video", "--speed=1.8", filename], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        
        # 4. El Vigilante Táctico: Mantiene vivo a Python mientras mpv suena,
        # pero con pausas imperceptibles para no congelar los hilos del sistema.
        while proceso_audio.poll() is None:
            time.sleep(0.05)
            
        # 5. Limpieza segura: Una vez que poll() detecta que mpv terminó, borramos el mp3
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        print(f"[-] Error en el controlador de voz: {e}")