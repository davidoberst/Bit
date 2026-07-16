# =====================================================================
# R.E.D. - ARCHIVO MAESTRO DE CONTROL (main.py)
# =====================================================================

import time
import sounddevice as sd
import audio_controller       
import vision_controller      
import brain      
import traceback
import sys            
import speaker_controller
import pygame
import threading 
from delete_temp_files import delete_temp_files

#ventana de pygame
pygame.init()

ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Bit")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)


# LÓGICA DE CONTROL Y ESTADOS DE R.E.D.

esta_grabando = False
esta_procesando = False
stream_audio = None

def iniciar_grabacion():
    """Inicia la escucha activa del micrófono en segundo plano."""
    global esta_grabando, stream_audio
    delete_temp_files()
    
    audio_controller.audio_buffer = []
    audio_controller.is_muted = False
    
    # Iniciar el stream de audio
    stream_audio = sd.InputStream(
        samplerate=audio_controller.audio_frequency, 
        channels=1, 
        callback=audio_controller.audio_callback
    )
    stream_audio.start()
    esta_grabando = True
    print("[*] Grabando... Presiona ENTER de nuevo en la ventana para detener.")

def procesar_y_responder():
    """Hilo secundario: Detiene grabación, toma captura, consulta a Gemini y habla."""
    global esta_grabando, esta_procesando, stream_audio
    esta_procesando = True
    
    # 1. Detener micrófono de forma segura
    if stream_audio:
        stream_audio.stop()
        stream_audio.close()
    
    print("[*] Procesando muestras de voz locales...")
    audio_controller.save_audio_output()
    
    # 2. Visión periférica
    print("[*] Activando visión periférica...")
    captura_exitosa = vision_controller.take_screenshot()
    
    if not captura_exitosa:
        print("[-] Cancelando secuencia: El módulo de visión falló.")
        esta_procesando = False
        return

    # 3. Consultar Cerebro (Gemini)
    print("[*] Sincronizando datos con el núcleo de R.E.D...")
    respuesta_ia = brain.consultar_modelo_IA()
    
    if respuesta_ia:
        print("\n" + "═"*50)
        print("R.E.D. RESPONSE:")
        print("═"*50)
        print(respuesta_ia)
        print("═"*50 + "\n")
        
        # 4. Hablar (Esta función suele ser bloqueante, por eso corre en este hilo)
        speaker_controller.hablar(respuesta_ia)
    else:
        print("[-] No se pudo obtener respuesta de la API.")
        
    esta_procesando = False


# BUCLE PRINCIPAL DE PYGAME (Game Loop)

print("[*] Inicializando RED en entorno gráfico...")

ejecutando = True
while ejecutando:
    
    # --- 1. Manejo de Eventos (Teclado y Ventana) ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        elif evento.type == pygame.KEYDOWN:
            # Si se presiona ENTER dentro de la ventana de Pygame
            if evento.key == pygame.K_RETURN:
                
                # Estado 1: No está haciendo nada -> Empezar a grabar
                if not esta_grabando and not esta_procesando:
                    iniciar_grabacion()
                
                # Estado 2: Está grabando -> Detener y empezar a procesar en un hilo
                elif esta_grabando and not esta_procesando:
                    esta_grabando = False
                    
                    hilo_procesamiento = threading.Thread(target=procesar_y_responder)
                    hilo_procesamiento.start()


    pantalla.fill(NEGRO)
    
    # Dibujar borde blanco
    pygame.draw.rect(pantalla, BLANCO, (0, 0, ANCHO, ALTO), 1)
    
    # Opcional: Cambiar el borde de color según el estado para feedback visual
    if esta_grabando:
        # Borde rojo si graba
        pygame.draw.rect(pantalla, (255, 0, 0), (0, 0, ANCHO, ALTO), 2)
    elif esta_procesando:
        # Borde azul/celeste si procesa
        pygame.draw.rect(pantalla, (0, 150, 255), (0, 0, ANCHO, ALTO), 2)

    # Actualizar los gráficos en la ventana
    pygame.display.flip()

# Al cerrar la ventana, nos aseguramos de apagar todo
if stream_audio:
    stream_audio.stop()
    stream_audio.close()
pygame.quit()
sys.exit()