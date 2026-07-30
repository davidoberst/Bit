# En este modulo se define el controlador de audio, como la IA escucha y procesa el audio 

import time
import os
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from faster_whisper import WhisperModel # TRANSCRIBIR AUDIO A TEXTO

# Variables de control para R.E.D.
is_muted = False
audio_frequency = 16000 #(Hz)
audio_buffer = []   

#cargar whisper al inicio. Para mas velocidad en el tiempo de respuesta, solo cargar una vez para no hacerlo en cada request
print("[*] Cargando Whisper...")
model = WhisperModel("small", device="cpu", compute_type="int8")
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
            segments, info = model.transcribe(
                filename, 
                language="es",
                temperature=0.0
            )
            transcripcion = " ".join(segment.text for segment in segments).strip()
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