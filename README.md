# Gestor de preservación digital
## Info proyecto
Este proyecto es una aplicacion desarrollada en python para ayudarme en el archivado de mis copias de seguridad físicas en Blu-Ray. 
Consta de un fichero que gestiona una base de datos SQLite, otro que gestiona la logica que se comunica con el sistema operativo a 
la hora de tocar ficheros, generar hashes y escanear directorios y por último tiene el fichero que guarda la interfaz gráfica y 
el resto de la lógica (threads, explorar directorios, etc).
## Otra info relevante
Esta pensado para windows por lo que las rutas de los programas de los que depende son rutas a .exe con formato de windows,
son las rutas que tiene una instalación por defecto en el caso de ambos programas (Winrar, Imgburn).
## Tutorial
La aplicación consta de 3 pestañas:
* Generar RARs
* Preparar buffer y grabar disco
* Gestión de base de datos
### Generar RARs
La interfaz es la siguiente:
<img width="1918" height="1198" alt="imagen" src="https://github.com/user-attachments/assets/63176698-ac84-48d4-9d46-6afcfca490fe" />
Simplemente seleccionas la carpeta que contenga los archivos que quieres comprimir y donde quieres el archivo de salida .rar,
además de su nombre.

Por defecto omite el directorio padre (no comprime el directorio dentro del rar, solo el contenido del directorio),
usa máxima compresión y un registro de recuperación del 5%. La compresión se realiza en segundo plano con otro hilo por lo que
la GUI no queda bloqueada hasta que la compresión termina.
### Preparar buffer y grabar disco
La interfaz es la siguiente:
<img width="1918" height="1198" alt="imagen" src="https://github.com/user-attachments/assets/7cf640b7-4d79-432b-bdd9-1e0aad4c84cc" />
Seleccionas el directorio en la que tienes todo lo que quieres que acabe en un Blu-Ray y el directorio que quieres usar de buffer de grabación.
Luego para que se cargue en la interfaz hay que pulsar el botón "cargar carpetas". También puedes modificar que disco vas a grabar
en función de si es de una, dos, tres o cuatro capas. 

La interfaz muestra una barra de llenado en base al tamaño del contenido del directorio escogido como buffer de grabación 
para que se pueda optimizar al máximo el espacio de cada disco.

Desde la interfaz se pueden mover archivos y directorios entre ambos directorios de forma transparente sin tocar nada en el explorador
de archivos, cada vez que se hace se refresca la interfaz y la barra de llenado.

Por último hay un botón que lanza el ejecutable de ImgBurn de estar presente en el equipo para que puedas empezar la grabación.
### Gestión de base de datos
La interfaz es la siguiente:
<img width="1918" height="1198" alt="imagen" src="https://github.com/user-attachments/assets/8d7a9e6c-3dcf-48af-919d-a640872477d5" />
Puedes buscar en la BBDD archivos, RARs (que estan separados de todo el resto de archivos porque los uso como contenedor) y discos grabados.
Por defecto si buscas discos y no introduces un ID válido, mostrará una lista de todos los discos grabados registrados.

Si buscas un disco concreto muestra un resumen de los ficheros que contiene ademas de la información del disco (fecha y capacidad).

Al buscar RARs y ficheros normales puedes introducir un id de disco y mostrará todos los archivos que conste que están en ese disco.
Por último si buscas por nombre de archivo (tanto rar como otro) es necesaria la extensión y se muestra toda la info disponible.
