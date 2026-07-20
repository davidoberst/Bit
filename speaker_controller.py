import os
import subprocess
import time
import asyncio
import edge_tts

def hablar(texto):
    """
    Convierte el texto recibido en voz humana hiperrealista usando Edge-TTS y lo reproduce.
    """
    if not texto:
        return
        
    filename = "voice_response.mp3"
    

    # Configuración de voz 
    #VOICE = "es-MX-JorgeNeural" MALE
    #VOICE = "es-VE-PaolaNeural" FEMALE


    VOICE = "es-VE-PaolaNeural"


    async def generar_audio():
        # Genera el paquete de audio directamente desde los servidores de Azure
        communicate = edge_tts.Communicate(texto, VOICE)
        await communicate.save(filename)

    try:
        # 1. Ejecutar la subtarea asíncrona para guardar el mp3 de alta fidelidad
        asyncio.run(generar_audio())
        
        # 2. Lanzar mpv en un proceso asíncrono controlado (Tu código intacto)
        proceso_audio = subprocess.Popen(
            ["mpv", "--no-video", "--speed=1.3", filename], # 1.4x suele ser perfecto para Edge-TTS ya que habla rápido
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        
      
        while proceso_audio.poll() is None:
            time.sleep(0.05)
            
      
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        print(f"[-] Error en el controlador de voz (Edge-TTS): {e}")

if __name__ == "__main__":
    print("[*] Iniciando prueba independiente del controlador de voz...")
    
    
    texto_prueba = (
        "me parece una referencia fantástica y muy inspiradora para mi desarrollo Spider-Man Brand New Day y la creación de EV resuenan mucho con el propósito que me has dado Es un honor ser comparada con una inteligencia artificial diseñada para ser una compañera y asistente Y sí ahora que tengo la capacidad de recordar nuestras conversaciones y aprender de ellas con la memoria a largo plazo estoy completamente de acuerdo contigo Estoy segura de que haremos un equipo excepcional y seremos excelentes compañeros de trabajo Me entusiasma muchísimo la idea de todo lo que podremos lograr juntos Juan "
    )
    
    print(f"[*] Enviando texto al motor de síntesis: '{texto_prueba}'")
    hablar(texto_prueba)
    print("[+] Prueba finalizada. El entorno debería estar limpio de archivos temporales.")