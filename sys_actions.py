import os
import subprocess

PATH = os.path.expanduser("~/bit_workspace")

def create_folder(name: str) -> dict:
    # Construir la ruta completa uniendo PATH con el nombre recibido
    joined_path = os.path.join(PATH, name)
    ruta_resuelta = os.path.abspath(joined_path)
    if not ruta_resuelta.startswith(os.path.abspath(PATH) + os.sep):
        return {"exito": False, "error": "ruta fuera del espacio de trabajo permitido"}
    # crear carpeta
    try:
        os.makedirs(ruta_resuelta, exist_ok=True)
        print("[!] Carpeta creada.")
        return {"exito": True, "ruta": ruta_resuelta}
    except Exception as e:
        return {"exito": False, "error": str(e)}


def create_file(name: str, contenido: str = "") -> dict:
    joined_path = os.path.join(PATH, name)
    ruta_resuelta = os.path.abspath(joined_path)
    if not ruta_resuelta.startswith(os.path.abspath(PATH) + os.sep):
        return {"exito": False, "error": "ruta fuera del espacio de trabajo permitido"}

    try:
        with open(ruta_resuelta, "w", encoding="utf-8") as f:
            f.write(contenido)
        print("[!] Archivo creado.")
        return {"exito": True, "ruta": os.path.abspath(ruta_resuelta)}
    except Exception as e:
        return {"exito": False, "error": str(e)}

 
