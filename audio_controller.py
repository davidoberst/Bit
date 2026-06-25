#En este modulo se define el controlador de audio, como la IA escucha y procesa el audio 

import time
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

# Variables de control para R.E.D.
is_muted = False
audio_frequency = 16000 #(Hz)
audio_buffer = []   

def audio_callback(indata, frames, time, status):
    global is_muted
    global audio_buffer 
    if status:
        print(f"hardware status : {status}") 
        
    if is_muted: 
        return  #si el microfono esta muteado, que ignore el bloque.
    #else
    audio_buffer.append(indata.copy())

def save_audio_output(filename="audio_output.wav"):
    if not audio_buffer:
        print("no hay audio grabado para guardar.")
        return
    #else

    #juntar audio completo :
    full_audio = np.concatenate(audio_buffer, axis=0)
    
    #escrbir datos en un wav 
    write(filename, audio_frequency, full_audio)
    print(f"[audio guardado con éxito en: {filename}")
