# En este modulo se define el controlador de audio, como la IA escucha y procesa el audio 

import time
import os
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import whisper # TRANSCRIBIR AUDIO A TEXTO ()

# Variables de control para R.E.D.
is_muted = False
audio_frequency = 16000 #(Hz)
audio_buffer = []   

#cargar whisper, modelo de transcripcion al inicio. Para mas velocidad en el tiempo de respuesta, solo cargar una vez para no hacerlo en cada request
print("[*] Cargando Whisper...")
model = whisper.load_model("small")
print("[*] Whisper cargado..")

def audio_callback(indata, frames, time, status):
    global is_muted
    global audio_buffer 
    if status:
        print(f"hardware status : {status}") 
        
    if is_muted: 
        return # si el microfono esta muteado, que ignore el bloque.
    
    audio_buffer.append(indata.copy())

def save_audio_output(filename="audio_output.wav"):
    if not audio_buffer:
        print("No hay audio grabado para guardar.")
        return "[Audio no grabado]"

    # Juntar audio completo:
    full_audio = np.concatenate(audio_buffer, axis=0)
    
    # Escribir datos en un wav 
    write(filename, audio_frequency, full_audio)
    print(f"[*] Audio guardado con éxito en: {filename}")

    # -------------------------------------------------------------
    # Transcribir wav a texto usando Whisper para la memoria (memory.json)

    print("[*] Transcribiendo audio localmente con Whisper...")
    try:       
        if os.path.isfile(filename): 
            resultado = model.transcribe(
                filename, 
                language="es",
                fp16=False,
                temperature=0.0
            )
            transcripcion = resultado.get("text", "").strip()
            
            if transcripcion:
                print(f"[+] Transcripción exitosa: \"{transcripcion}\"")
                return transcripcion
            else:
                return "[Audio sin voz detectable]"
        else:
            return "[Archivo de audio no encontrado]"

    except Exception as e:
        print(f"[-] Error al ejecutar Whisper: {e}")
        return "[Error al leer archivo de audio]"