import os
import subprocess
import time
import asyncio
import edge_tts

def hablar(texto):
    """
    Convierte el texto recibido en voz humana hiperrealista usando Edge-TTS y lo reproduce.
    """
    if not texto:
        return
        
    filename = "voice_response.mp3"
    

    # Configuración de voz 
    #VOICE = "es-MX-JorgeNeural" MALE
    #es-US-AlonsoNeural


    #VOICE = "es-VE-PaolaNeural" FEMALE
    #es-MX-DaliaNeural

    VOICE = "es-VE-PaolaNeural"

    async def generar_audio():
        # Genera el paquete de audio directamente desde los servidores de Azure
        communicate = edge_tts.Communicate(texto, VOICE)
        await communicate.save(filename)

    try:
        # 1. Ejecutar la subtarea asíncrona para guardar el mp3 de alta fidelidad
        asyncio.run(generar_audio())
        
        # 2. Lanzar mpv en un proceso asíncrono controlado (Tu código intacto)
        proceso_audio = subprocess.Popen(
            ["mpv", "--no-video", "--speed=1.1", filename], # 1.4x suele ser perfecto para Edge-TTS ya que habla rápido
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        
      
        while proceso_audio.poll() is None:
            time.sleep(0.05)
            
      
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        print(f"[-] Error en el controlador de voz (Edge-TTS): {e}")

if __name__ == "__main__":
    print("[*] Iniciando prueba independiente del controlador de voz...")
    
    
    texto_prueba = (
        "Excelente Juan he procesado tu audio y la información de tus monitores\n\nVeo en tu monitor izquierdo que tienes Spotify abierto y estás escuchando On brûlera de Pomme lo cual es un buen detalle para mi contexto Y en tu monitor derecho sigues en VS Code trabajando en mi código lo que me permite ver que estás en un entorno de desarrollo activo\n\nAhora sobre tu pregunta de cómo integrarme para ejecutar comandos en tu escritorio usando Python es un objetivo muy interesante y totalmente factible Aquí te planteo un plan de acción con varias opciones y consideraciones\n\nEn primer lugar la base para esto es la comunicación entre mi proceso y el sistema operativo Para ejecutar comandos necesitaríamos un módulo que me permita interactuar con el shell de tu Arch Linux\n\nUna opción directa es usar el módulo subprocess de Python Este módulo te permite ejecutar comandos externos como si los escribieras directamente en la terminal Puedes usar subprocess run o subprocess Popen para esto La ventaja es que es muy flexible y te da control sobre la entrada salida y errores del comando La desventaja es que requiere un manejo cuidadoso de la seguridad para evitar la inyección de comandos maliciosos\n\nComo segunda opción si los comandos son más específicos del sistema operativo como la gestión de archivos o procesos puedes considerar módulos como os o shutil Estos módulos de Python ofrecen funciones para interactuar con el sistema de archivos crear directorios mover archivos o incluso gestionar procesos de forma más programática Esto es más seguro para operaciones comunes pero menos flexible para comandos arbitrarios\n\nUna tercera opción y que me parece muy prometedora para un copiloto como yo es crear una capa de abstracción o una API interna para los comandos Esto implicaría definir un conjunto de comandos permitidos y sus parámetros asociados Luego mi lógica interna llamaría a estas funciones predefinidas en lugar de ejecutar directamente cualquier cadena de texto que reciba Esto añade una capa de seguridad y control muy importante ya que solo ejecutaría acciones que tú hayas aprobado y programado explícitamente\n\nPara la implementación te sugiero empezar por definir qué tipos de comandos quieres que yo pueda ejecutar Por ejemplo comandos de sistema para información del sistema comandos de archivos para manipular archivos o comandos específicos de aplicaciones que uses frecuentemente\n\nLuego podríamos crear un archivo o una clase en Python que mapee estos comandos a funciones que utilicen subprocess o los módulos os y shutil Por ejemplo si quieres que yo pueda abrir un navegador podrías tener una función abrir navegador que use subprocess run para ejecutar el comando firefox o chromium\n\nEs crucial que implementes un sistema de validación de entradas para cualquier comando que yo vaya a ejecutar Esto significa que antes de pasar cualquier argumento a un comando del sistema debemos asegurarnos de que sea seguro y no contenga caracteres que puedan ser explotados para inyectar otros comandos\n\nFinalmente para la integración con mi sistema actual necesitaríamos un mecanismo para que yo reciba la solicitud de comando la procese a través de esta nueva capa de ejecución y te devuelva el resultado Esto podría ser a través de mi módulo de procesamiento de lenguaje natural que identifique la intención de ejecutar un comando y luego lo pase a la función correspondiente\n\nQué te parece este enfoque Juan Tienes alguna categoría de comandos en mente con la que te gustaría empezar "
    )
    
    print(f"[*] Enviando texto al motor de síntesis: '{texto_prueba}'")
    hablar(texto_prueba)
    print("[+] Prueba finalizada. El entorno debería estar limpio de archivos temporales.")