# =====================================================================
# R.E.D. - ARCHIVO MAESTRO DE CONTROL (main.py)
# =====================================================================

import time
import math
import numpy as np
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

# Evitar banners de Pygame
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Inicialización de la ventana de pygame
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
esta_hablando = False  # Estado para saber cuándo Bit está usando su voz
stream_audio = None

# Buffer para capturar las ondas de voz del usuario en tiempo real
muestras_mic = np.zeros(400)

def callback_mic_visual(indata, frames, time_info, status):
    """Callback que graba el audio para el backend y guarda una copia para la onda visual."""
    global muestras_mic
    audio_controller.audio_callback(indata, frames, time_info, status)
    if len(indata) > 0:
        muestras_mic = indata[:, 0].copy()

def iniciar_grabacion():
    """Inicia la escucha activa del micrófono en segundo plano."""
    global esta_grabando, stream_audio, muestras_mic
    delete_temp_files()
    
    audio_controller.audio_buffer = []
    audio_controller.is_muted = False
    muestras_mic = np.zeros(400)
    
    # Iniciar el stream de audio apuntando a nuestro callback visualizador
    stream_audio = sd.InputStream(
        samplerate=audio_controller.audio_frequency, 
        channels=1, 
        callback=callback_mic_visual
    )
    stream_audio.start()
    esta_grabando = True
    print("[*] Grabando... Presiona ENTER de nuevo en la ventana para detener.")

def hablar_sincronizado(texto):
    """Ejecuta el TTS y marca el estado de habla de Bit para activar la física del círculo."""
    global esta_hablando
    esta_hablando = True
    speaker_controller.hablar(texto)
    esta_hablando = False

def decir_frase_carga_async():
    """Lanza la voz de carga en segundo plano para no ralentizar el análisis táctico."""
    hablar_sincronizado("Claro, procesando datos multimedia, un momento Juan.")

def procesar_y_responder():
    """Hilo secundario: Detiene grabación, toma captura, consulta a Gemini y habla."""
    global esta_grabando, esta_procesando, stream_audio
    esta_procesando = True
    
    # 1. Detener micrófono de forma segura
    if stream_audio:
        stream_audio.stop()
        stream_audio.close()

    # Lanzar aviso de carga por voz de forma asíncrona inmediatamente
    hilo_voz_carga = threading.Thread(target=decir_frase_carga_async)
    hilo_voz_carga.start()
    
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
    
    # Esperar a que termine de decir la frase de carga antes de que hable la respuesta final
    hilo_voz_carga.join()
    
    if respuesta_ia:
        print("\n" + "═"*50)
        print("R.E.D. RESPONSE:")
        print("═"*50)
        print(respuesta_ia)
        print("═"*50 + "\n")
        
        # 4. Hablar (Corre sincronizado con la animación circular de Bit)
        hablar_sincronizado(respuesta_ia)
    else:
        print("[-] No se pudo obtener respuesta de la API.")
        
    esta_procesando = False


# BUCLE PRINCIPAL DE PYGAME (Game Loop)
print("[*] Inicializando RED en entorno gráfico...")

clock = pygame.time.Clock()
ejecutando = True

while ejecutando:
    clock.tick(60)  # Mantener ciclo estable a 60 FPS
    
    # --- 1. Manejo de Eventos (Teclado y Ventana) ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                # Estado 1: Inactivo -> Empezar a grabar
                if not esta_grabando and not esta_procesando:
                    iniciar_grabacion()
                
                # Estado 2: Grabando -> Detener e iniciar procesamiento
                elif esta_grabando and not esta_procesando:
                    esta_grabando = False
                    hilo_procesamiento = threading.Thread(target=procesar_y_responder)
                    hilo_procesamiento.start()

    # --- 2. Renderizado de Gráficos (Todo Blanco y Negro) ---
    pantalla.fill(NEGRO)
    
    # Dibujar borde blanco minimalista y fijo
    pygame.draw.rect(pantalla, BLANCO, (0, 0, ANCHO, ALTO), 1)
    
    centro_x = ANCHO // 2
    centro_y = ALTO // 2
    radio_base = 150

    if esta_grabando:
        # 🎙️ EL USUARIO HABLA: El círculo desaparece y se dibuja la onda de sonido horizontal
        puntos_onda = []
        paso_x = ANCHO / len(muestras_mic)
        for i, amp in enumerate(muestras_mic):
            x = int(i * paso_x)
            # Escalamos la amplitud del micrófono
            desplazamiento_y = int(amp * 250)
            # Limitar la deformación para que sea limpia
            desplazamiento_y = max(-200, min(200, desplazamiento_y))
            y = centro_y + desplazamiento_y
            puntos_onda.append((x, y))
            
        if len(puntos_onda) > 1:
            pygame.draw.lines(pantalla, BLANCO, False, puntos_onda, 2)

    elif esta_hablando:
        # 🤖 BIT HABLA: Círculo deformándose rápidamente (Osciloscopio circular reactivo)
        puntos_circulo_mutante = []
        t = time.time() * 25  # Velocidad de oscilación de la voz de Bit
        
        # Generar un círculo deformado usando funciones senoidales complejas de alta frecuencia
        for i in range(361):
            angulo = math.radians(i)
            # Modulación compleja para simular ondas de voz artificiales sobre el radio base
            deformacion = (
                math.sin(angulo * 8 + t) * 12 + 
                math.sin(angulo * 3 - t * 1.5) * 8 + 
                math.cos(angulo * 12 + t * 2) * 4
            )
            radio_dinamico = radio_base + deformacion
            x = int(centro_x + radio_dinamico * math.cos(angulo))
            y = int(centro_y + radio_dinamico * math.sin(angulo))
            puntos_circulo_mutante.append((x, y))
            
        pygame.draw.polygon(pantalla, NEGRO, puntos_circulo_mutante, 0)  # Relleno negro
        pygame.draw.lines(pantalla, BLANCO, True, puntos_circulo_mutante, 2)  # Línea blanca

    elif esta_procesando:
        # 🧠 PROCESANDO: Círculo con una pulsación senoidal lenta y elegante
        puntos_procesando = []
        t = time.time() * 8
        for i in range(361):
            angulo = math.radians(i)
            # Una onda más armónica y controlada mientras piensa
            deformacion = math.sin(angulo * 10 + t) * 5
            radio_dinamico = radio_base + deformacion
            x = int(centro_x + radio_dinamico * math.cos(angulo))
            y = int(centro_y + radio_dinamico * math.sin(angulo))
            puntos_procesando.append((x, y))
            
        pygame.draw.lines(pantalla, BLANCO, True, puntos_procesando, 2)

    else:
        # 💤 REPOSO: Círculo blanco minimalista y perfecto
        pygame.draw.circle(pantalla, BLANCO, (centro_x, centro_y), radio_base, 2)

    # Actualizar la pantalla
    pygame.display.flip()

# Al cerrar la ventana, liberar recursos
if stream_audio:
    stream_audio.stop()
    stream_audio.close()
pygame.quit()
sys.exit()