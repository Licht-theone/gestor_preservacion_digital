import sqlite3

def inicializar():
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
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("insert into discos values (?, ?, ?)", (id_disco, fecha_grabacion, capacidad))
    conexion.commit()
    conexion.close()

def crear_archivo_disco(nombre_archivo, id_disco):
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("insert into archivos "
                   "(nombre_archivo, id_disco) values (?, ?)",
                   (nombre_archivo, id_disco))
    conexion.commit()
    conexion.close()

def crear_rar_disco(nombre_archivo, id_disco):
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("insert into rars (nombre_archivo, id_disco) values (?, ?)",
                   (nombre_archivo, id_disco))
    conexion.commit()
    conexion.close()

def adjuntar_nombre_rar_a_archivo(nombre_rar, nombre_archivo):
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("update archivos set nombre_rar=? where nombre_archivo=?",
                   (nombre_rar, nombre_archivo))
    conexion.commit()
    conexion.close()

def adjuntar_hash_a_rar(hash_rar, nombre_archivo):
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("update rars set hash_rar=? where nombre_archivo=?",
                   (hash_rar, nombre_archivo))
    conexion.commit()
    conexion.close()

def buscar_disco(id_disco):
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("select * from discos where id=?", (id_disco, ))
    disco = cursor.fetchall()
    conexion.close()
    return disco

def buscar_archivo(nombre_archivo):
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("select * from archivos where nombre_archivo=?", (nombre_archivo, ))
    archivo = cursor.fetchall()
    conexion.close()
    return archivo

def buscar_rar(nombre_archivo):
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("select * from rars where nombre_archivo=?", (nombre_archivo, ))
    rar = cursor.fetchall()
    conexion.close()
    return rar

def buscar_archivos_disco(id_disco):
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("select * from archivos where id_disco=?", (id_disco, ))
    archivos_disco = cursor.fetchall()
    conexion.close()
    return archivos_disco

def buscar_rars_disco(id_disco):
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("select * from rars where id_disco=?", (id_disco, ))
    rars = cursor.fetchall()
    conexion.close()
    return rars

def buscar_discos():
    conexion = sqlite3.connect('./BD-R_archive.db')
    cursor = conexion.cursor()
    cursor.execute("select * from discos")
    discos = cursor.fetchall()
    conexion.close()
    return discos