# =====================================================================
# (main.py) — Versión terminal, sin interfaz gráfica
# =====================================================================

import sounddevice as sd
import numpy as np
import audio_controller
import vision_controller
import brain
import speaker_controller
import threading
import concurrent.futures
from delete_temp_files import delete_temp_files
import subprocess

# LÓGICA DE CONTROL Y ESTADOS
esta_grabando = False
stream_audio = None


def iniciar_grabacion():
    """Inicia la escucha activa del micrófono en segundo plano."""
    global esta_grabando, stream_audio
    delete_temp_files()

    audio_controller.audio_buffer = []
    audio_controller.is_muted = False

    stream_audio = sd.InputStream(
        samplerate=audio_controller.audio_frequency,
        channels=1,
        callback=audio_controller.audio_callback
    )
    stream_audio.start()
    esta_grabando = True
    print("\n[●] Grabando... presione ENTER de nuevo para detener.\n")


def decir_frase_carga_async():
    """Lanza la voz de carga en segundo plano para no ralentizar el análisis."""
    speaker_controller.hablar("Procesando entrada y datos multimedia.")


def procesar_y_responder():
    """Detiene grabación, toma captura, consulta al modelo y habla."""
    global stream_audio
    print("[*] Procesando...")

    # 1. Detener micrófono de forma segura
    if stream_audio:
        stream_audio.stop()
        stream_audio.close()

    # Lanzar aviso de carga por voz de forma asíncrona
    hilo_voz_carga = threading.Thread(target=decir_frase_carga_async)
    hilo_voz_carga.start()

    # 2. Transcripción y captura en paralelo
    print("[*] Procesando voz y visión en paralelo...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futuro_transcripcion = executor.submit(audio_controller.save_audio_output)
        futuro_captura = executor.submit(vision_controller.take_screenshot)
        texto_transcrito_usuario = futuro_transcripcion.result()
        captura_exitosa = futuro_captura.result()

    if not captura_exitosa:
        print("[-] Cancelando secuencia: El módulo de visión falló.")
        return

    # 3. Consultar modelo
    print("[*] Sincronizando datos con brain.py...")
    respuesta_ia = brain.consultar_modelo_IA(texto_usuario_previo=texto_transcrito_usuario)

    # Esperar a que termine la frase de carga antes de hablar la respuesta final
    hilo_voz_carga.join()

    if respuesta_ia:
        print("\n" + "═" * 50)
        print("RESPONSE:")
        print("═" * 50)
        print(respuesta_ia)
        print("═" * 50 + "\n")

        speaker_controller.hablar(respuesta_ia)
    else:
        speaker_controller.hablar("Lo siento señor, No se pudo obtener una respuesta de la API, revise los logs.")
        print("[-] No se pudo obtener respuesta de la API.")


# BUCLE PRINCIPAL EN TERMINAL
print("")

print("┌" + "─" * 46 + "┐")
print("│                BIT — V3" + " " * 20 + "")
print("└" + "─" * 46 + "┘")
print("  [*] Presione ENTER para empezar a grabar")
print("  [*] Presione ENTER para detener y procesar")
print("  [*] Presione Ctrl+C para salir.\n")
speaker_controller.hablar("Bienvenido, Juan.")

try:
    while True:
        input()  # Espera ENTER

        if not esta_grabando:
            iniciar_grabacion()
        else:
            esta_grabando = False
            procesar_y_responder()

except KeyboardInterrupt:
    print("\n[*] Cerrando JARVIS...")
    if stream_audio:
        stream_audio.stop()
        stream_audio.close()
    speaker_controller.hablar("Hasta luego, señor.")
    subprocess.run(["xdotool", "getactivewindow", "windowkill"])
    #cerrar ventana luego de despedida : 
    #sudo pacman -S xdotool

