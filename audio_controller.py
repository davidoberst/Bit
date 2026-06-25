#En este modulo se define el controlador de audio, como la IA escucha y procesa el audio 

import sounddevice as sd
import numpy as np

# Variables de control para R.E.D.
is_muted = False
audio_frequency = 44100 #(Hz)
audio_buffer = [] 

def audio_callback(indata, frames, time, status):
    if status:
        print(status) 
        
    if is_muted:
        return 
    #else
    audio_buffer.append(indata.copy())