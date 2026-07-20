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
    
    # Configuración de voz táctica:
    # es-MX-DaliaNeural (Voz femenina de México, ultra fluida y rápida)
    # es-CO-GonzaloNeural (Voz masculina de Colombia, excelente entonación)
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
            ["mpv", "--no-video", "--speed=1.5", filename], # 1.4x suele ser perfecto para Edge-TTS ya que habla rápido
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
        "Hola Juan, mi voz funciona perfectamente, la prueba fue exitosa"
    )
    
    print(f"[*] Enviando texto al motor de síntesis: '{texto_prueba}'")
    hablar(texto_prueba)
    print("[+] Prueba finalizada. El entorno debería estar limpio de archivos temporales.")