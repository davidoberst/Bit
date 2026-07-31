import os
import subprocess

PATH = os.path.expanduser("~/bit_workspace")

def create_folder(name : str) -> dict:
 #Construir la ruta completa uniendo CARPETA_BASE con el nombre recibido  
 joined_path = os.path.join(PATH,name)
 #crear carpeta 
 try:
  os.makedirs(joined_path, exist_ok=True)
  return{"exito": True, "ruta": os.path.abspath(joined_path) }
  print("[!] Carpeta creada.")
 except:
     return{"exito": False, "error": str(e) }

def create_file(name: str)-> dict:
    joined_path = os.path.join(PATH,name)
    try:
     file = os.open(name)   
     os.close(fd)
     return{"exito": True, "ruta": os.path.abspath(joined_path) }
     print("[!] Archivo creado.")
    except:
     return{"exito": False, "error": str(e) }





 
