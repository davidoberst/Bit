# =====================================================================
# R.E.D. - ARCHIVO MAESTRO DE CONTROL (main.py)
# =====================================================================

import time
import keyboard
import sounddevice as sd
import audio_controller       
import vision_controller      
import brain      
import traceback
import sys            
import speaker_controller
from delete_temp_files import delete_temp_files

def ejecutar_ciclo_asistencia():
    print("\n" + "="*50)
    print("R.E.D INICIADO")
    print("="*50)
    
    # 1. Limpiar el buffer usando el nombre correcto del módulo
    audio_controller.audio_buffer = []
    audio_controller.is_muted = False
    
    # 2. Iniciar la escucha activa por el micrófono
    print("\n Escuchando... Habla ahora (Tienes 1 minuto de grabación, presiona x para pararla.)")
    stream = sd.InputStream(
        samplerate=audio_controller.audio_frequency, 
        channels=1, 
        callback=audio_controller.audio_callback
    )
    
    with stream:
     input(" Presiona ENTER para detener la grabación y enviar a R.E.D... ")
     print("\n[+] Grabación finalizada por el usuario.")
        
    print("[*] Procesando muestras de voz locales...")
    audio_controller.save_audio_output() # Guarda 'audio_output.wav'
    
    # 3. Disparar el ojo táctico usando el nombre correcto del módulo
    print("\n Activando visión periférica...")
    captura_exitosa = vision_controller.take_screenshot()
    
    if not captura_exitosa:
        print("[-] Cancelando secuencia: El módulo de visión falló.")
        return

    # 4. Enviar payload multimodal al cerebro conectado con Gemini
    print("\n Sincronizando datos con el núcleo de R.E.D...")
    respuesta_ia = brain.consultar_modelo_IA()
    
    if respuesta_ia:
        print("\n" + "═"*50)
        print("R.E.D. RESPONSE:")
        print("═"*50)
        print(respuesta_ia)
        print("═"*50 + "\n")

        speaker_controller.hablar(respuesta_ia) #respuesta por voz
        delete_temp_files()


    else:
        print("[-] No se pudo obtener respuesta de la API.")

if __name__ == "__main__":
    print("[*] Inicializando RED")
    print("[+] Servidor gráfico KDE Wayland detectado a través de Spectacle.")
    print("[+] Frecuencia de audio optimizada a 16kHz.")
    
    try:
        ejecutar_ciclo_asistencia()
    except KeyboardInterrupt:
        print("\n[-] Sistema apagado de forma manual por el usuario.")
    except Exception as e:
        tb = e.__traceback__
        linea = traceback.extract_tb(tb)[-1].lineno
        print(f"\n[-] Error inesperado en RED: {e} Linea :{linea}")
    
