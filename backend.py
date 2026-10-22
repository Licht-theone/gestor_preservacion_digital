import hashlib
import subprocess
import os
import shutil

def calcular_hash_rar(ruta_a_archivo):
    """Metodo que calcula el hash de un archivo rar
    :param (str) ruta_a_archivo: ruta al archivo.rar completa
    :return (str): hash sha256 en formato string
    """
    sha256 = hashlib.sha256()
    with open(ruta_a_archivo, 'rb') as archivo:
        for chunk in iter(lambda: archivo.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def generar_rar(ruta_a_archivos, ruta_destino):
    """Metodo que genera un archivo .rar con 5% recuperacion y maxima compresion
    :param (str) ruta_a_archivos: ruta a la carpeta cuyo contenido se empaquetara
    :param (str) ruta_destino: ruta de salida del archivo.rar
    :return (None):
    """
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
    """Metodo que calcula el tamaño en bytes de un directorio con subdirectorios
    :param (str) ruta: ruta a la carpeta
    :return (int): el tamaño en bytes del directorio
    """
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
    """Metodo que escanea un directorio en busca de todos sus archivos (en subdirectorios incluido)
    :param (str) ruta: ruta a la carpeta a escanear
    :returns (List): lista de todos los archivos encontrados
    """
    datos_bbdd = []
    if os.path.exists(ruta):
        for root, dirs, files in os.walk(ruta):
            for file in files:
                datos_bbdd.append(file)
    return datos_bbdd

def leer_archivos(ruta):
    """Metodo que lee los archivos de una carpeta concreta
    :param (str) ruta: ruta a la carpeta
    :return (List): lista de archivos concreta
    """
    if os.path.exists(ruta):
        return os.listdir(ruta)
    else:
        return None

def mover_archivos(origen, destino):
    """Metodo que mueve un archivo de una carpeta a otra
    :param (str) origen: ruta a origen (completa hasta el archivo.extension)
    :param (str) destino: ruta a destino (completa hasta el archivo.extension)
    :return (boolean): true si se mueve con exito, false en cualquier otro caso
    """
    try:
        shutil.move(origen, destino)
        return True
    except Exception as e:
        print("Error al mover: {e}")
        return False

def lanzar_img_burn():
    """Metodo que lanza imgburn de existir"""
    ruta = r"C:\Program Files (x86)\ImgBurn\ImgBurn.exe"
    if os.path.exists(ruta):
        subprocess.Popen(ruta)
    else:
        return