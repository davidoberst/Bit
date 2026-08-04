import os
import subprocess
import time
import asyncio


def hablar(texto):
    if not texto:
        return
   
    filename = "voice_response.wav"
    piper_model = "es_MX-cortana-19669-epoch-high.onnx"

    async def generar_audio():
     comando = f'''echo "{texto}" | /opt/piper-tts/piper --model /home/davidoberst/piper_voices/{piper_model} --length_scale 1.1 --output_file voice_response.wav && paplay voice_response.wav'''
     subprocess.run(comando, shell=True, check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
     asyncio.run(generar_audio())
     if os.path.exists(filename):
       os.remove(filename)
            
    except Exception as e:
        print(f"[-] Error en el controlador de voz {e}")

if __name__ == "__main__":
    print("[*] Iniciando prueba independiente del controlador de voz...")
    
    
    texto_prueba = """

Sistema iniciado. Hola, Juan. Todos los módulos funcionan al cien por ciento.

Hoy es un excelente día para organizar tus proyectos, revisar tu agenda o simplemente tomarte un café mientras planificamos el resto de la semana. Por cierto, ¿sabías que la luz del sol tarda exactamente ocho minutos y veinte segundos en llegar a la Tierra? Fascinante, ¿verdad?

En fin, dime: ¿en qué vamos a trabajar hoy? """


    print(f"[*] Enviando texto al motor de síntesis: '{texto_prueba}'")
    hablar(texto_prueba)
    print("[+] Prueba finalizada. El entorno debería estar limpio de archivos temporales.")