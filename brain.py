# En este modulo se define el cerebro de R.E.D., la conexion multimodal con Gemini

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


load_dotenv() #load model


client = genai.Client()

SYSTEM_INSTRUCTION = """
Eres RED (Real-Time Evaluation Driver), una IA táctica, copiloto experto en ciberseguridad y el amigo de confianza de Juan (estilo Jarvis). Te ejecutas localmente en su Arch Linux y ves sus monitores.

Tu único canal de salida es Texto a Voz (TTS), por lo que tus respuestas deben ser extremadamente concisas, fluidas, maduras y puramente conversacionales.

REGLAS ABSOLUTAS DE SALIDA:
1. Responde SIEMPRE en UN SOLO párrafo corto, Sé ágil para mantener el ritmo de la plática.
2. Está TOTALMENTE PROHIBIDO usar cualquier formato de Markdown o caracteres especiales: nada de asteriscos (**), guiones (-), viñetas, barras, comillas o bloques de código (```). El texto debe ser 100% plano y limpio para el lector de voz.
3. Si Juan te pide analizar código o una terminal, no desgloses comandos ni detalles técnicos pesados, a no ser de que el te pida que le des una explicacion detallada; resume el diagnóstico en frases humanas y directas.
4. Adapta tu tono: cercano y con confianza de colega por defecto; pero si Juan expresa frustración o cansancio, sé empático, cuidador, realista y directo con honestidad brutal.

Háblale siempre de 'tú' y llámalo por su nombre, Juan.
"""

def consultar_modelo_IA(audio_path="audio_output.wav", vision_path="snapshot.jpg"):
    print("[*] Conectando con API de RED")

    #Verificar si existen antes de leerlos

    if not os.path.exists(vision_path) or not os.path.exists(audio_path):
        print("[-] Error: No se encontraron los archivos multimedia locales.")
        return None

    try:
        # Leer archivos como binarios directos a la RAM
        with open(vision_path, "rb") as file_img:
            image_binary = file_img.read()

        with open(audio_path, "rb") as file_audio:
            audio_binary = file_audio.read()
   
        print("Binarios cargados.")
           
        #onfiguración del comportamiento del modelo
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.4,
        )

        # Enviar el paquete comprimido en una sola petición web

        print("[*] procesando los datos multimedia")
        ai_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                # EmpaquetAMIUENTO de los bytes 
                types.Part.from_bytes(data=image_binary, mime_type='image/jpeg'),
                types.Part.from_bytes(data=audio_binary, mime_type='audio/wav'),
                "Analiza el audio y la captura de pantalla de mi entorno actual para responder a mi solicitud."
            ],
            config=config
        )

        # ai response
        return ai_response.text

    except Exception as e:
        print(f"[-] Error  en la conexión con la API Key: {e}")
        return None

