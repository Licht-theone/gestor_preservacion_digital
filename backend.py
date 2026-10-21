import hashlib
import subprocess
import os
import shutil

def calcular_hash_rar(ruta_a_archivo):
    sha256 = hashlib.sha256()
    with open(ruta_a_archivo, 'rb') as archivo:
        for chunk in iter(lambda: archivo.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def generar_rar(ruta_a_archivos, ruta_destino):
    # parametros default
    rar_exe = r"C:\Program Files\WinRAR\Rar.exe"
    add = "a"
    recovery = "-rr5p"
    compress = "-m5"
    exc_dir = "-ep1"
    werror = "-inul"
    command = [rar_exe, add, recovery, compress,
               exc_dir, werror, ruta_destino, ruta_a_archivos]
    subprocess.run(command, check=True)

def calcular_capacidad_usada(ruta):
    tamano = 0
    if os.path.exists(ruta):
        for root, _, files in os.walk(ruta):
            for file in files:
                ruta_file = os.path.join(root, file)
                try:
                    tamano += os.path.getsize(ruta_file)
                except FileNotFoundError:
                    pass
    return tamano

def escanear_para_archivo(ruta):
    datos_bbdd = []
    if os.path.exists(ruta):
        for root, dirs, files in os.walk(ruta):
            for file in files:
                datos_bbdd.append(file)
    return datos_bbdd

def leer_archivos(ruta):
    if os.path.exists(ruta):
        return os.listdir(ruta)
    else:
        return None

def mover_archivos(origen, destino):
    try:
        shutil.move(origen, destino)
        return True
    except Exception as e:
        print("Error al mover: {e}")
        return False

def lanzar_img_burn():
    ruta = r"C:\Program Files (x86)\ImgBurn\ImgBurn.exe"
    if os.path.exists(ruta):
        subprocess.Popen(ruta)
    else:
        return