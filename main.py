import sounddevice as sd
import numpy as np
import audio_controller
import vision_controller
import brain
import brain_bit_command_model
import speaker_controller
import threading
import concurrent.futures
from delete_temp_files import delete_temp_files
import subprocess
import pyfiglet
# LÓGICA DE CONTROL Y ESTADOS
esta_grabando = False
stream_audio = None
modo_actual = "command"  # "vision" o "command"


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
    print("┌" + "─" * 46 + "┐")
    print("│ [●] Grabando...Presiona Enter para deneter" + " " * 20 + "")
    print("└" + "─" * 46 + "┘")


def decir_frase_carga_async():
    """Lanza la voz de carga en segundo plano para no ralentizar el análisis."""
    if modo_actual == "vision":
        speaker_controller.hablar("Analizando datos de Escritorio.")
    else:
        speaker_controller.hablar("Procesando.")


def procesar_y_responder():
    """Detiene grabación, consulta al modelo según el modo activo, y habla."""
    global stream_audio
    print("[*] Procesando...")

    # 1. Detener micrófono 
    if stream_audio:
        stream_audio.stop()
        stream_audio.close()

    # Lanzar aviso de carga por voz de forma asíncrona
    hilo_voz_carga = threading.Thread(target=decir_frase_carga_async)
    hilo_voz_carga.start()

    if modo_actual == "vision":
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

        print("[*] Sincronizando datos con brain.py...")
        respuesta_ia = brain.consultar_modelo_IA(texto_usuario_previo=texto_transcrito_usuario)

    else:  # modo_actual == "command"
        # 2. Solo transcripción, sin captura de pantalla
        print("[*] Procesando voz...")
        texto_transcrito_usuario = audio_controller.save_audio_output()

        print("[*] Sincronizando datos con brain_bit_command_model.py...")
        respuesta_ia = brain_bit_command_model.consultar_modelo_IA(texto_usuario_previo=texto_transcrito_usuario)

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
        speaker_controller.hablar("Lo siento juan, No se pudo obtener una respuesta de la API, revisa los logs.")
        print("[-] No se pudo obtener respuesta de la API.")


# BUCLE PRINCIPAL EN TERMINAL
print("")
title = pyfiglet.figlet_format("Bit v2", font="smmono12")

print("┌" + "─" * 46 + "┐")

for linea in title.splitlines():
    print("│" + linea.center(46) + "│")

print("│" + "v.2.0".center(46) + "│")
print("└" + "─" * 46 + "┘")
print("  [*] Presione ENTER para empezar a grabar")
print("  [*] Presione ENTER para detener y procesar")
print("  [*] Presione M para ver modos de Asistencia")
print("  [*] Presione Ctrl+C para salir.\n")
speaker_controller.hablar("Hola, Juan.")


try: 
    while True:
        choice = input("> ")

        if choice.lower() == "m":
            print("┌" + "─" * 46 + "┐")
            print("│         MODOS DE ASISTENCIA" + " " * 20 + "")
            print("└" + "─" * 46 + "┘")
            print(f"""1. Bit Vision : Combina visión por computadora y reconocimiento de voz en tiempo real. Al analizar lo que ves en tu escritorio, Bit comprende lo que estás haciendo para resolver dudas sobre el contenido en pantalla, y darte asistencia contextual inmediata sin que tengas que explicarle cada detalle.""")
            print("")
            print("2. Bit Command : Diseñado para una interacción rápida y liviana. Bit se enfoca exclusivamente en responder preguntas, charla o procesar tus instrucciones de voz para ejecutar comandos del sistema, abrir aplicaciones, gestionar tareas y controlar tu computadora sin procesar tu pantalla.")
            print("")
            print(f"Modo activo actualmente: {modo_actual}")
            print("")
            print("Para seleccionar un modelo, simplemente escriba el nombre del modelo en minusculas en la consola : 'vision' o 'command' ")
            print("")
            continue

        if choice.lower() == "vision":
            modo_actual = "vision"
            print("[*] Modo cambiado a Bit Vision.")
            continue

        if choice.lower() == "command":
            modo_actual = "command"
            print("[*] Modo cambiado a Bit Command.")
            continue

        if choice == "": 
            if not esta_grabando:
                iniciar_grabacion()
            else:
                esta_grabando = False
                procesar_y_responder()

except KeyboardInterrupt:
    print("\n[*] Cerrando Bit...")
    if stream_audio:
        stream_audio.stop()
        stream_audio.close()
    speaker_controller.hablar("Hasta luego, Juan.")
    subprocess.run(["xdotool", "getactivewindow", "windowkill"])
