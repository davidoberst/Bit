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
import pygame
from delete_temp_files import delete_temp_files


#CONFIGURACION DE VENTANA DE PYGAME

#inicializar pygame 

pygame.init()

ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))

#titulo de la ventana 

pygame.display.set_caption("Bit")

#definir colores para la ventana 

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Bucle principal
ejecutando = True
while ejecutando:
    
    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # --- Renderizado ---
    
    # 1. Pintar el fondo de negro absoluto
    pantalla.fill(NEGRO)
    
    # 2. Dibujar el borde blanco de 1 px
    # pygame.draw.rect(superficie, color, (x, y, ancho, alto), grosor)
    pygame.draw.rect(pantalla, BLANCO, (0, 0, ANCHO, ALTO), 1)

    # Actualizar la pantalla
    pygame.display.flip()

def ejecutar_ciclo_asistencia():
    delete_temp_files()

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
    
