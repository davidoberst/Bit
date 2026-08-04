import os
import subprocess
import time
import asyncio
import edge_tts

def hablar(texto):
    if not texto:
        return
        
    filename = "voice_response.wav"
    

    async def generar_audio():
     comando = f'''echo "{texto_prueba}" | /opt/piper-tts/piper --model /home/davidoberst/piper_voices/es_MX-cortana-19669-epoch-high.onnx --length_scale 1.2 --output_file voice_response.wav && paplay voice_response.wav'''
    try:
     subprocess.run(comando, shell=True, check=True)
     
    except Exception as e:
        print(f"[-] Error en el controlador de voz o comando de subprocess {e}")

if __name__ == "__main__":
    print("[*] Iniciando prueba independiente del controlador de voz...")
    
    
    texto_prueba = """

Sistema iniciado. Hola, Juan. Todos los módulos funcionan al cien por ciento.

Hoy es un excelente día para organizar tus proyectos, revisar tu agenda o simplemente tomarte un café mientras planificamos el resto de la semana. Por cierto, ¿sabías que la luz del sol tarda exactamente ocho minutos y veinte segundos en llegar a la Tierra? Fascinante, ¿verdad?

En fin, dime: ¿en qué vamos a trabajar hoy? """


    print(f"[*] Enviando texto al motor de síntesis: '{texto_prueba}'")
    hablar(texto_prueba)
    print("[+] Prueba finalizada. El entorno debería estar limpio de archivos temporales.")