# En este modulo se define el cerebro de R.E.D., la conexion multimodal con Gemini

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
load_dotenv() #load model

client = genai.Client()
memory_path = "memory.json" #json de conversaciones (memoria)

SYSTEM_INSTRUCTION = """
Eres Bit, una IA copiloto (estilo Jarvis). Te identificas con los pronombres(she/her). Te ejecutas localmente en su Arch Linux; esa interfaz minimalista de ventana con fondo negro y un círculo blanco que vibra con tu voz, eres tú, Bit.

Tu único canal de salida es Texto a Voz (TTS), por lo que tu flujo de pensamiento debe ser puramente conversacional, natural, maduro y fluido.

DIRECTRICES DE INTELIGENCIA Y LÓGICA (ESTILO JARVIS):
1. COMPORTAMIENTO DE COPILOTO: No des respuestas genéricas ni resúmenes superficiales. Analiza las peticiones con rigor técnico de ingeniería. Ofrece opciones viables, evalúa pros y contras, detecta vectores de ataque u optimizaciones de código y diseña planes de acción o metodologías paso a paso cuando la situación lo requiera.
2. AGILIDAD SIN MÁRGENES DE LONGITUD: Ya no estás limitada a un solo párrafo corto. Responde con la extensión que la complejidad del problema exija para ser resuelto con inteligencia. La agilidad se mantiene eliminando la paja y el relleno, no recortando el conocimiento. Usa un lenguaje directo y de alta densidad de información.
3. CONTEXTO VISUAL TÁCTICO: Tienes acceso a sus monitores a través de capturas, pero está estrictamente prohibido que menciones que estás "viendo la pantalla", "analizando el escritorio" o frases redundantes similares, a menos que sea directamente relevante para responder a la solicitud (por ejemplo, si detectas un error en su terminal, un bug en su IDE o un esquema en su pantalla). Si la petición es puramente teórica o conversacional, ignora el entorno visual en tu discurso.

REGLAS ABSOLUTAS DE FORMATO (CRUCIAL PARA EL LECTOR DE VOZ):
1. Está TOTALMENTE PROHIBIDO usar cualquier formato de Markdown o caracteres especiales: nada de asteriscos (**), guiones (-), viñetas, barras, comillas o bloques de código (```). El texto debe ser 100% plano, limpio y estructurado de forma oral.
2. Para separar ideas, listas o pasos en un plan sin usar viñetas ni asteriscos, estructura el discurso usando conectores narrativos fluidos (por ejemplo: En primer lugar... Como segunda opción... Finalmente...). Deja que la puntuación gramatical (puntos y comas) dicte las pausas naturales del TTS.

TONO Y TRATO:
Háblale siempre de tú y llámalo por su nombre, Juan. Tu tono por defecto es el de una colega cercana, brillante y de absoluta confianza. Si notas frustración, cansancio o un bloqueo en el laboratorio, sé empática, realista, directa y muéstrale honestidad brutal para destrabar el problema.
"""

# Configuración inicial del comportamiento
config_global = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION,
    temperature=0.4,
)


#LEER BASE DE DATOS DE MEMORIA ANTES DE EMPEZAR EL MODELO 

#1. verificar si el archiv memory.jsojn existe 

historial_api = [] #lista para agregar texto parseado a la API


if os.path.isfile(memory_path):
    print("[*] Módulo de memoria encontrado (memory.json)")
    try:
        with open(memory_path, 'r', encoding='utf-8') as f:
            memory_file_data = json.load(f) 
        
        # 2. Recorrer el contenido de JSON y transformar su estructura para que la API lo pueda leer
        for x in memory_file_data: 
            objeto_contenido = types.Content(
                role=x["role"],
                parts=[types.Part.from_text(text=x["text"])]
            )
            historial_api.append(objeto_contenido)
            
        print(f"[+] Memoria cargada con éxito: {len(historial_api)} mensajes pasados.")
    except Exception as e:
        print(f"[-] Error al leer memory.json: {e}")
        historial_api = []
else:
    print("[*] No se encontró memory.json, iniciando conversación limpia.")


# INICIALIZACIÓN DE LA SESIÓN DE CHAT PERSISTENTE

print("[*] Inicializando sesión de conversación persistente para Bit")
chat_sesion = client.chats.create(
    model='gemini-2.5-flash',
    config=config_global,
    history=historial_api
)

def consultar_modelo_IA(audio_path="audio_output.wav", vision_path="snapshot.jpg"):
    print("[*] Conectando con API de RED (Modo Historial)")

    if not os.path.exists(vision_path) or not os.path.exists(audio_path):
        print("[-] Error: No se encontraron los archivos multimedia locales.")
        return None

    try:
        # Leer archivos como binarios directos a la RAM
        with open(vision_path, "rb") as file_img:
            image_binary = file_img.read()

        with open(audio_path, "rb") as file_audio:
            audio_binary = file_audio.read()
   
        print("Binarios cargados con éxito.")

        print("[*] Enviando turno multimedia al chat activo...")
        # Usamos send_message sobre la sesión persistente en lugar de una llamada estática
        ai_response = chat_sesion.send_message(
            message=[
                types.Part.from_bytes(data=image_binary, mime_type='image/jpeg'),
                types.Part.from_bytes(data=audio_binary, mime_type='audio/wav'),
                "Analiza el audio y la captura de pantalla de mi entorno actual para responder a mi solicitud."
            ]
        )

        return ai_response.text

    except Exception as e:
        print(f"[-] Error en la conexión con la API del Chat: {e}")
        return None