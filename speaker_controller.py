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
    #es-US-AlonsoNeural


    #VOICE = "es-VE-PaolaNeural" FEMALE
    #es-MX-DaliaNeural

    VOICE = "es-US-AlonsoNeural"

    async def generar_audio():
       
        communicate = edge_tts.Communicate(texto, VOICE, rate="+0%", volume="+20%", pitch="-15Hz") #15
        await communicate.save(filename)

    try:
        # 1. Ejecutar la subtarea asíncrona para guardar el mp3 de alta fidelidad
        asyncio.run(generar_audio())
        
        # 2. Lanzar mpv en un proceso asíncrono controlado (Tu código intacto)
        proceso_audio = subprocess.Popen(
            ["mpv", "--no-video", "--speed=1.5", filename], # 1.4x
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
    
    
    texto_prueba = """

Señor, la Toxicidad en la sangre, 24%. Parece que el uso continuado del traje de Iron Man está acelerando su condición. Otro núcleo se ha agotado.

He ejecutado simulaciones en todos los elementos conocidos, y ninguno puede servir como un reemplazo viable para el núcleo de paladio.

Se le está acabando tanto el tiempo como las opciones. Desafortunadamente, el dispositivo que lo mantiene con vida también lo está matando."""


    print(f"[*] Enviando texto al motor de síntesis: '{texto_prueba}'")
    hablar(texto_prueba)
    print("[+] Prueba finalizada. El entorno debería estar limpio de archivos temporales.")