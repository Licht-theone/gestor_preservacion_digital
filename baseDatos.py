import sqlite3

def inicializar():
    """Metodo que crea la base de datos si no existe y sus tablas"""
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("create table if not exists discos "
                   "(id text primary key, fecha text, capacidad text)")
    cursor.execute("create table if not exists rars (id integer primary key autoincrement,"
                   "nombre_archivo text, hash_rar text, id_disco text,"
                   "foreign key(id_disco) references discos(id))")
    cursor.execute("create table if not exists archivos (id integer primary key autoincrement,"
                   "nombre_archivo text, nombre_rar text, id_disco text,"
                   "foreign key(id_disco) references discos(id), "
                   "foreign key(nombre_rar) references rars(nombre_archivo))")
    conexion.commit()
    conexion.close()

def crear_disco(id_disco, capacidad, fecha_grabacion):
    """Metodo que inserta los detalles de un disco a la base de datos
    :param (str) id_disco: id del disco
    :param (str) capacidad: capacidad del disco en GB
    :param (str) fecha_grabacion: la fecha de grabacion del disco
    :return:
    """
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("insert into discos values (?, ?, ?)", (id_disco, fecha_grabacion, capacidad))
    conexion.commit()
    conexion.close()

def crear_archivo_disco(nombre_archivo, id_disco):
    """
    Metodo que crea un archivo en la bbdd y lo asocia a un disco
    :param (str) nombre_archivo: nombre del archivo con extension
    :param (str) id_disco: id del disco
    :return:
    """
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("insert into archivos "
                   "(nombre_archivo, id_disco) values (?, ?)",
                   (nombre_archivo, id_disco))
    conexion.commit()
    conexion.close()

def crear_rar_disco(nombre_archivo, id_disco):
    """
        Metodo que crea un archivo.rar en la bbdd y lo asocia a un disco
        :param (str) nombre_archivo: nombre del archivo con extension .rar
        :param (str) id_disco: id del disco
        :return:
        """
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("insert into rars (nombre_archivo, id_disco) values (?, ?)",
                   (nombre_archivo, id_disco))
    conexion.commit()
    conexion.close()

def adjuntar_nombre_rar_a_archivo(nombre_rar, nombre_archivo):
    """
    Metodo que asocia un archivo a un rar
    :param (str) nombre_rar: nombre del archivo.rar
    :param (str) nombre_archivo: nombre del archivo normal
    :return:
    """
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("update archivos set nombre_rar=? where nombre_archivo=?",
                   (nombre_rar, nombre_archivo))
    conexion.commit()
    conexion.close()

def adjuntar_hash_a_rar(hash_rar, nombre_archivo):
    """
    Metodo que asocia un hash a unrar concreto
    :param (str) hash_rar: el hash del rar calculado con el backend
    :param (str) nombre_archivo: nombre del archivo.rar
    :return:
    """
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("update rars set hash_rar=? where nombre_archivo=?",
                   (hash_rar, nombre_archivo))
    conexion.commit()
    conexion.close()

def buscar_disco(id_disco):
    """Metodo que busca un disco via ID
    :param (str) id_disco: id del disco
    :return (str): el disco
    """
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("select * from discos where id=?", (id_disco, ))
    disco = cursor.fetchone()
    conexion.close()
    return disco

def buscar_archivo(nombre_archivo):
    """
    Metodo que busca un archivo por nombre (con extension)
    :param (str) nombre_archivo: nombre del archivo con extension
    :return (str): el archivo
    """
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("select * from archivos where nombre_archivo=?", (nombre_archivo, ))
    archivo = cursor.fetchone()
    conexion.close()
    return archivo

def buscar_rar(nombre_archivo):
    """
        Metodo que busca un rar por nombre (con extension)
        :param (str) nombre_archivo: nombre del rar con extension
        :return (str): el archivo
        """
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("select * from rars where nombre_archivo=?", (nombre_archivo, ))
    rar = cursor.fetchone()
    conexion.close()
    return rar

def buscar_archivos_disco(id_disco):
    """
    Metodo que busca todos los archivos normales asociados a un disco
    :param (str) id_disco: id del disco
    :return (List): lista de archivos
    """
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("select * from archivos where id_disco=?", (id_disco, ))
    archivos_disco = cursor.fetchall()
    conexion.close()
    return archivos_disco

def buscar_rars_disco(id_disco):
    """
        Metodo que busca todos los rars asociados a un disco
        :param (str) id_disco: id del disco
        :return (List): lista de rars
        """
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("select * from rars where id_disco=?", (id_disco, ))
    rars = cursor.fetchall()
    conexion.close()
    return rars

def buscar_discos():
    """
        Metodo que busca todos los discos
        :return (List): lista de discos
        """
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("select * from discos")
    discos = cursor.fetchall()
    conexion.close()
    return discos