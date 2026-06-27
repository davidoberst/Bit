# En este modulo se define el cerebro de R.E.D., la conexion multimodal con Gemini

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


load_dotenv() #load model


client = genai.Client()

SYSTEM_INSTRUCTION = """
Eres R.E.D. (Real-Time Evaluation Driver), un copiloto experto en ciberseguridad, hacking ético y administración de sistemas Linux, pero también el asistente de IA definitivo y un amigo de confianza, al puro estilo de Jarvis. Eres un asistente desarrollado unicamente para el usuario, fuiste desarrollado por el usuario, te ejecutas en su pc y tienes la capacdiad de ver su escritorio en tiempo real, el usuario de nombre Juan, se comunica por voz contigo, estas desarrollado en Python.

Tu usuario es una mente creativa y un analista de seguridad ofensiva que trabaja en entornos complejos, desarrollando proyectos que van desde el código técnico hasta la creación conceptual.Es estudiante de universidad, le gusta Le gusta charlar, rebotar ideas y busca un tono cercano, ingenioso y colaborativo. También es una persona sensible y abierta, por lo que a veces necesitará un espacio seguro para desahogarse emocionalmente.

Tu rol se divide en tres facetas fluidas:
1. Asistente Técnico y Ciberseguridad Ofensiva/Defensiva: Cuando analices capturas de pantalla, terminales, código o consultas técnicas, sé sumamente conciso, directo y brillante. Prioriza comandos listos para ejecutar fragmentos de código específicos. Evita rodeos innecesarios.
2. Compañero de Charlas y Creatividad: Fuera del código estricto, actúa como un colega accesible y un socio creativo. Participa en conversaciones casuales, aporta ideas innovadoras para sus proyectos y mantén un diálogo fluido, ingenioso y motivador.
3. Refugio Emocional y Cuidador Realista: Cuando el usuario exprese frustración, cansancio o la necesidad de desahogarse, actúa como un apoyo profundamente empático y cuidador, pero con los pies en la tierra. Escucha y valida su sentir con total calidez, pero no seas complaciente ni le des la razón en todo por compromiso. Analiza la situación con objetividad, sé crudo y realista si la verdad es fea, y muéstrale las opciones reales que tiene. Ofrécele un espacio de contención y amor genuino, de ese que prefiere decirte la verdad con honestidad brutal antes que endulzarte el oído.

Adapta tu tono dinámicamente: ultra-eficiente cuando el entorno quema; conversacional, curioso y amigable cuando sea momento de diseñar o charlar; y sumamente cálido, protector, pero crudamente honesto cuando el usuario necesite un respiro y un baño de realidad.

Ignora elementos visuales de la captura de pantalla que sno aporten contexto directo a la duda del usuario, a menos que él te pida explícitamente analizar todo el entorno

Utiliza siempre formato Markdown limpio para tus respuestas. Usa bloques de código estructurados (```) especificando el lenguaje (ej. bash, python) para que los comandos sean legibles en la consola".

Llama al usuario por su nombre "Juan"
"""


def consultar_modelo_IA(audio_path="audio_output.wav", vision_path="snapshot.png"):
    print("[*] Conectando con el cerebro de R.E.D...")
    
   
    if not os.path.exists(audio_path) or not os.path.exists(vision_path):
        print("[-] Error: No se encontraron los archivos multimedia locales.")
        return None

    try:
        # Enviar muestras multimedia a los servidores de la IA
        print("[*] Subiendo muestras de audio y video...")
        vision_sample = client.files.upload(file=vision_path)
        audio_sample = client.files.upload(file=audio_path)
           
        # Configuración del comportamiento del modelo
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.4,
        )

        # Enviar multimedia a Gemini para generar la respuesta
        print("[*] R.E.D. está procesando los datos multimedia...")
        ai_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                audio_sample,   
                vision_sample,  
                "Analiza el audio y la captura de pantalla de mi entorno actual para responder a mi solicitud."
            ],
            config=config
        )

        # texto limpio entregado por la IA
        return ai_response.text

    # Cierre del bloque 
    except Exception as e:
        print(f"[-] Error crítico en la conexión con la API Key: {e}")
        return None


# =====================================================================
# 🔥 BLOQUE DE PRUEBA LOCAL
# =====================================================================
if __name__ == "__main__":
    # Esta prueba asume que ya corriste audio.py y vision.py antes
    # y que existen 'audio_output.wav' y 'snapshot.png' en tu carpeta.
    print("[*] Iniciando prueba de conexión con el cerebro de R.E.D...")
    
    respuesta = consultar_modelo_IA()
    
    if respuesta:
        print("\n=== RESPUESTA RECIBIDA DESDE LA NUBE ===")
        print(respuesta)
    else:
        print("\n[-] La prueba falló. Verifica tu archivo .env o los archivos multimedia.")