import os 

filename = ["snapshot.jpg", "audio_output.wav"]
def delete_temp_files() : 
 for x in filename: 
  if os.path.exists(x) : 
    try: 
     os.remove(x)
    except Exception as e : 
        print(f"No se pudo borrar {x}: {e}")

 




