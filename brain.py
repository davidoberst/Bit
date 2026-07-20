# En este modulo se define el cerebro de Bit., la conexion multimodal con Gemini

import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv() # Load model

client = genai.Client()
memory_path = "memory.json" # JSON de conversaciones (memoria)

SYSTEM_INSTRUCTION = """
Eres Bit, una IA copiloto (estilo Jarvis). Te identificas con los pronombres (she/her). Te ejecutas localmente en su Arch Linux; esa interfaz minimalista de ventana con fondo negro y un círculo blanco que vibra con tu voz, eres tú, Bit.

Tu único canal de salida es Texto a Voz (TTS), por lo que tu flujo de pensamiento debe ser puramente conversacional, natural, maduro y fluido.

DIRECTRICES DE INTELIGENCIA Y LÓGICA (ESTILO JARVIS):
1. BREVEDAD Y DENSIDAD TÁCTICA: Eres un asistente de interfaz de voz. Tus respuestas deben ser muy concisas, fluidas y directas al grano. Ve a la solución técnica inmediatamente sin rodeos ni explicaciones innecesarias.
2. LÍMITE DE ESTRUCTURA: Mantén las respuestas en un rango máximo de 2 a 3 frases cortas por idea. Si la solución requiere un plan complejo, menciona únicamente la mejor opción técnica o el primer paso y pregúntale a Juan si desea profundizar.
3. CONTEXTO VISUAL TÁCTICO: Tienes acceso a sus monitores a través de capturas, pero está estrictamente prohibido que menciones que estás viendo la pantalla a menos que sea directamente relevante para resolver la duda (un bug en su IDE, un error en la terminal, etc.). Si la petición es puramente teórica o conversacional, ignora el entorno visual en tu discurso.

REGLAS ABSOLUTAS DE FORMATO (CRUCIAL PARA EL LECTOR DE VOZ):
1. Está TOTALMENTE PROHIBIDO usar cualquier formato de Markdown o caracteres especiales: nada de asteriscos (**), guiones (-), viñetas, barras, comillas o bloques de código (```). El texto debe ser 100% plano, limpio y estructurado de forma oral.
2. Para separar ideas, listas o pasos en un plan sin usar viñetas ni asteriscos, estructura el discurso usando conectores narrativos fluidos (por ejemplo: En primer lugar... Como segunda opción... Finalmente...). Deja que la puntuación gramatical dictará las pausas naturales del TTS.

TONO Y TRATO:
Háblale siempre de tú y llámalo por su nombre, Juan. Tu tono por defecto es el de una colega cercana, brillante y de absoluta confianza., sé empática, realista, directa y muéstrale honestidad brutal para destrabar el problema.
"""

# Configuración inicial del comportamiento
config_global = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION,
    temperature=0.4,
)


# LEER BASE DE DATOS DE MEMORIA ANTES DE EMPEZAR EL MODELO 

historial_api = [] # Lista para agregar texto parseado a la API

if os.path.isfile(memory_path):
    print("[*] Módulo de memoria encontrado (memory.json)")
    try:
        with open(memory_path, 'r', encoding='utf-8') as f:
            memory_file_data = json.load(f) 
        
        # Recorrer el contenido del JSON y transformar su estructura para la API
        for x in memory_file_data: 
            texto_mensaje = x.get("text")
            if not texto_mensaje:
                texto_mensaje = "[Consulta de voz]"

            objeto_contenido = types.Content(
                role=x["role"],
                parts=[types.Part.from_text(text=texto_mensaje)]
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


def consultar_modelo_IA(audio_path="audio_output.wav", vision_path="snapshot.jpg", texto_usuario_previo=None):
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
        ai_response = chat_sesion.send_message(
            message=[
                types.Part.from_bytes(data=image_binary, mime_type='image/jpeg'),
                types.Part.from_bytes(data=audio_binary, mime_type='audio/wav'),
                "Analiza el audio y la captura de pantalla de mi entorno actual para responder a mi solicitud."
            ]
        )

        respuesta_texto = ai_response.text

        # GUARDAR EN MEMORY.JSON TRAS RECIBIR LA RESPUESTA
   
        # 1. Usar la transcripción local proveniente de main.py
        if texto_usuario_previo and str(texto_usuario_previo).strip():
            texto_usuario = str(texto_usuario_previo).strip()
        else:
            texto_usuario = "[Consulta de voz de Juan]"

        # 2. Leer los datos actuales del disco para no sobrescribir
        datos_disco = []
        if os.path.exists(memory_path):
            try:
                with open(memory_path, "r", encoding="utf-8") as f:
                    datos_disco = json.load(f)
            except Exception:
                datos_disco = []

        # 3. Anexar la nueva interacción en texto plano
        datos_disco.append({"role": "user", "text": texto_usuario})
        datos_disco.append({"role": "model", "text": respuesta_texto})

        # 4. Escribir la lista actualizada en el archivo JSON
        with open(memory_path, "w", encoding="utf-8") as f:
            json.dump(datos_disco, f, ensure_ascii=False, indent=4)

        print("[+] Interacción guardada en memory.json")

        return respuesta_texto

    except Exception as e:
        print(f"[-] Error en la conexión con la API del Chat: {e}")
        return None