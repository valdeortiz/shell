#! /usr/bin/env python
import shutil
import click
import logging
from click_shell import shell
import os
import getpass
import ftplib
import socket
from os import listdir
import fileinput
import crypt
import signal
import subprocess
from datetime import datetime




#variables globales del código:
#archivo_usuario: contiene el path junto al nombre del archivo donde se guardará la 
#información de los usuarios creados con la shell, la información consiste en su nombre, 
#hora de entrada, hora de salida y su ip de conexión
# archivo = "/var/log" path para lfs
archivo_usuario = "/var/log/usuarios.log"
archivo_personal_horarios = "/var/log/usuario_horarios.log"
archivo_personal_transferencias = "/var/log/Shell_transferencias.log"


# Creamos nuestro logger principal y usamos el metodo basicConfig para configurar
logging.basicConfig(level=logging.INFO,
                    # formato del horario (YYYY-MM-DD hh:min:sec),
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    # name es el user, asctime es hora y fecha, levelname: severidad, message: mensaje del error.
                    filename="/var/log/shell.log")

# creamos otro logger para guardar los errores del sistema
# cambiar el nombre del archivo a el path del log donde se desea guardar los errores
# los errores de comandos van separados de los errores de inicio de sesion
log_error = logging.getLogger("")
fhp = logging.FileHandler("/var/log/errores.log")
fhp.setLevel(logging.ERROR)
log_error.addHandler(fhp)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhp.setFormatter(formatter)
log_error.addHandler(fhp)



@shell(prompt=f'shell>', intro='**** Bienvenido ***')
def cli():
    pass


#Comando ir, se utiliza para cambiar de directorio, recibe como parametro la 
#ruta del directorio la cual de ser posible se convierte en el nuevo
#working directory, utiliza la libreria os.
@cli.command()
@click.argument('ruta',nargs=1)
def ir(ruta):
    """Cambio de Directorio."""
    log(f'ir {ruta}')
    try:
        if os.path.exists(ruta):
            os.chdir(ruta)
            click.echo(f"Directorio actual: {os.getcwd()}")
            log("cambio al directorio: " + os.getcwd())
        else:
            click.echo("Error al ejecutar el comando <ir>, el directorio no existe")
            log_error.error("Error al ejecutar el comando <ir>, el directorio no existe")
    except click.ClickException as e:
        click.echo(f"Error {e}-> Ejecute help <ir> para mas informacion")
        log_error.error(f"codigo del error: {e} -> al ejecutar <ir> ")

#comando diractual, sirve para imprimir en pantalla
#el directorio de trabajo actual,el comando recibe un argumento, este argumento debe ser vacio, 
#esto es para verificarque el comando no reciba argumentos demas, 
#utiliza la libreria os.
@cli.command()
@click.argument('l', default='')
def diractual(l):

    """Imprime en pantalla el directorio actual"""
    log(f"diractual {l}")
    try:
        click.echo(f"Directorio actual: {os.getcwd()}")
    except:
        log_error.error("Error al mostrar el directorio actual.")

#comando copiar, recibe como parametro el archivo a copiar junto con su path en caso
# que no se encuentre en el directorio actual y el directorio destino donde se creara
#una copia del archivo indicado, utiliza la libreria os.
@cli.command()
@click.argument('origen',  nargs=1)
@click.argument('destino', nargs=1)
def copiar(origen,destino):
    """Copia un archivo a un directorio."""
    log(f'copiar {origen} {destino}')
    try:
        if (os.path.exists(origen) and os.path.exists(destino)):
            shutil.copy(origen, destino)
            click.echo(f"Se copio {click.format_filename(origen)} a {click.format_filename(destino)} con exito.")
            log(f"Se copio {click.format_filename(origen)} a {click.format_filename(destino)} con exito.")
        else:
            click.echo("Error -> nombres y archivos especificados no válidos o no es posible modificarlos.")
            log_error.error("nombres y rutas de archivos no válidos o inaccesibles. Al ejecutar <copiar>")
    except OSError:
        click.echo("Error -> nombres y archivos especificados no válidos o no es posible modificarlos.")
        log_error.error("nombres y rutas de archivos no válidos o inaccesibles. Al ejecutar <copiar>")
    except Exception as e:
        print(f"Error {e}-> Ejecute help <copiar> para mas informacion")
        log_error.error(f"codigo del error: {e} -> al ejecutar <copiar> ")

#comando propietarios, recibe como parametro el archivo junto a su path de no encontrarse en el directorio
#actual el nuevo usuario y/o nuevo grupo, utiliza la libreria os.
@cli.command()
@click.argument('archivo',nargs=1)
@click.argument('usuario',nargs=1)
@click.argument('grupo', nargs=1)
def propietarios(archivo,usuario,grupo):
    """Cambia el propietario de un directorio"""
    try:
        if os.path.exists(archivo):
            log(f"propietarios {archivo} {usuario} {grupo}")
            os.chown(archivo, usuario, grupo)
        else:
            click.echo("Error -> nombres y archivos especificados no válidos o no es posible modificarlos.")
            log_error.error("nombres y rutas de archivos no válidos o inaccesibles. Al ejecutar <propietarios>")
    except OSError:
        click.echo("Error -> nombres y archivos especificados no válidos o no es posible modificarlos.")
        log_error.error("nombres y rutas de archivos no válidos o inaccesibles. Al ejecutar <propietarios>")
    except Exception as e:
        print(f"Error {e}-> Ejecute help <propietarios> para mas informacion")
        log_error.error(f"codigo del error: {e} -> al ejecutar <propietarios> ")

#comando nombrehost, imprime en pantalla el nombre del anfitrion de la maquina,
#el comando recibe un argumento, este argumento debe ser vacio, esto es para verificar
#que el comando no reciba argumentos demas,utiliza la libreria socket.
@cli.command()
@click.argument('l', default='')
def nombrehost(l):
    """Imprime en pantalla el nombre del host"""
    log(f"nombrehost {l}")
    try:
        if (l == ''):
            click.echo(socket.gethostname())
        else:
            click.echo("Error -> Argumentos extra")
            log_error.error("Error -> Argumentos extra al ejecutar el comando <nombrehost>")
    except:
        click.echo("Error al ejecutar el comando nombrehost")
        log_error.error("Error al ejecutar el comando nombrehost")

        
#comando para listar los directorios y archivos dentro de un directorio, imprime en
#pantalla todos los directorios y archivos dentro del directorio actual,el comando recibe un argumento, este argumento debe ser vacio, 
#esto es para verificar que el comando no reciba argumentos demas, es posible cambiar la forma en la los elementos se
#imprimen, todos los datos se encuentran en la variable "lista", utiliza la libreria os.
@cli.command()
@click.argument('l', default='')
def listardirectorios(l):
    """Imprime en pantalla los archivos o directorios contenidos en el directorio actual"""
    log(f"listardirectorios {l}")
    try:
        if(l==''):
            lista=(listdir(os.getcwd()))
            for x in range(len(lista)):
                click.echo(lista[x])
        else:
            click.echo("Error -> Argumentos extra")
            log_error.error("Error -> Argumentos extra al ejecutar el comando <listardirectorios>")
    except click.ClickException as e:
        click.echo(f" Error: {e} -> al ejecutar <listardirectorios>")
        log_error.error(f" codigo del error: {e} -> al ejecutar <listardirectorios>")
#comando para crear un directorio, recibe como parametro el nombre o el nombre más el path donde 
#desea crear un directorio, utiliza la libreria os.
@cli.command()
@click.argument('direccion')
def creardir(direccion):
    """Crea un directorio en la ubicación especificada o en la actual"""
    log(f"creadir {direccion}")
    try:
        os.mkdir(direccion)
    except OSError:
        click.echo("Error -> nombres y rutas de archivos no válidos o inaccesibles.")
        log_error.error("nombres y rutas de archivos no válidos o inaccesibles. Al ejecutar <creadir>")
    except Exception as e:
        click.echo(f" Error: {e} -> al ejecutar <creadir>")
        log_error.error(f" codigo del error: {e} -> al ejecutar <creadir>")
#comando para levantar o apagar un demonio, utiliza el paquete signal y la libreria subprocess
#recibe como parametro la opcion ya sea levantar o apagar y el pid del proceso.
@cli.command()
@click.argument('opcion')
@click.argument('pid')
def demonio(opcion, pid):
    """Levanta o apaga demonios. Necesita como parametro
    la accion y el ID de proceso en caso de apagar,
    y el archivo a ejecutar en caso de levantar."""
    try:
        if (opcion == 'levantar'):
            try:
                subprocess.Popen(pid)
                log(f"demonio {opcion} {pid}")
            except Exception as e:
                print(e)
                print('Ocurrio un error o el parametro introducido es invalido.')
                log_error.error(f" codigo del error: {e} -> al ejecutar <demonio>")
        elif (opcion == 'apagar'):
            try:
                # SIGKILL no puede ser ignorado, SIGTERM si
                print(pid)
                pid = int(pid)
                
                os.kill(pid, signal.SIGTERM)
                os.kill(pid, signal.SIGKILL)
                log(f"demonio {opcion} {PID}")
            except Exception as e:
                print(e)
                print('Ocurrio un error o el parametro introducido es invalido.')
                log_error.error(f" codigo del error: {e} -> al ejecutar <demonio>")
    except Exception as e:
        print(e)
        print('Ocurrio un error o el comando se utilizo incorrectamente.')
        log_error.error(f" codigo del error: {e} -> al ejecutar <demonio>")
        
#comando renombrar, recibe como parametro el nombre a cambiar y el nuevo nombre
# utiliza la libreria os.
@cli.command()
@click.argument('origen')
@click.argument('destino')
def renombrar(origen: str, destino: str) -> None:

        """Renombrar un archivo o directorio
        Recibe dos parametros-> <nombre_actual> <nombre_cambiado>
        Manera de ejecutar: renombrar <nombre_actual> <nombre_a_cambiar>
        """
        try:
            log(f"renombrar {origen} {destino} ")
            os.rename(origen,destino)
            click.echo(f"< origen > fue renombrado a < destino >")
        except OSError:
            click.echo("Error -> nombres y rutas de archivos no válidos o inaccesibles.")
            log_error.error("nombres y rutas de archivos no válidos o inaccesibles. Al ejecutar <renombrar>")
        except Exception as e:
            click.echo(f" Error: {e} -> al ejecutar <renombrar>")
            log_error.error(f" codigo del error: {e} -> al ejecutar <renombrar>")



#comando para cambiar los permisos de un archivo o directorio, recibe como parametro la ruta
#del archivo a modificar y un entero que representa las opciones y campos a modificar.
@cli.command()
@click.argument('ruta')
@click.argument('permisos', type=click.INT)
def cambiarpermisos(ruta, permisos: int):#Error int() can't convert non-string with explicit base
    """Cambiar los permisos de un archivo o directorio.
    Recibe dos parametros-> <ruta> <permisos> 
    Manera de ejecutar:-> cambiarpermisos <ruta> <permisos>
    """
    try:
        os.chmod(ruta,int(permisos,8)) #EL segundo parametro que recibe chmod debe ser entero y en octal
        print("<",ruta,">", "permisos cambiado")
    except OSError:
        print("Error -> nombres y rutas de archivos no válidos o inaccesibles.")
        log_error.error("nombres y rutas de archivos no válidos o inaccesibles. Al ejecutar <permisos>")
    except Exception as e:
        print(f"Error {e}-> Ejecute help <permisos> para mas informacion")
        log_error.error(f"codigo del error: {e} -> al ejecutar <permisos> ")
        
        
#comando para mover archivos o directorios, recibe como parametros el directorio o archivo 
# a ser movido y el path del directorio donde desea que se mueva, tambien puede ser
# utilizado para cambiar el nombre de algun directorio.

@cli.command()
@click.argument('directorio_actual')
@click.argument('directorio_cambiado')
def mover(directorio_actual, directorio_cambiado):
    """
    Mover o renombrar un archivo o directorio.
    Recibe dos parametros-> <directorio_actual> <directorio_cambiado>
                          o para renombrar un archivo: <nombre_actual> <nombre_cambiado>
    Manera de ejecutar:-> mover <directorio_actual> <directorio_a_cambiar>
                    -> renombrar: mover <nombre_actual> <nombre_a_cambiar>
    """
    log(f"mover {directorio_actual} {directorio_cambiado} ")

    try:
        shutil.move(directorio_actual, directorio_cambiado)
        click.echo(f"<{directorio_actual}> fue movido a < {directorio_cambiado} >")
    except OSError:
        click.echo("Error -> nombres y rutas de archivos no válidos o inaccesibles.")
        log_error.error("nombres y rutas de archivos no válidos o inaccesibles. Al ejecutar <mover>")
    except Exception as e:
        click.echo(f"Error {e}-> Ejecute help <mover> para mas informacion")
        log_error.error(f" codigo del error: {e} -> Al ejecutar mover")

#comando para cambiar la contraseña de algun usuario, recibe como parametro 
# el nombre del usuario, para luego ingresar su nueva contraseña, este comando
#modifica el archivo /etc/shadow por lo tanto el usuario debe tener permisos de 
#administrador

@cli.command()
@click.argument('usuario')
@click.option('--contra', prompt="Introduce la contrasena: ", hide_input=True, required=True)
def ccontra(usuario, contra):
    """ Cambiar la contrasenha de un usuario
    parametros:
        -> [usuario]
    Modo de Ejecucion:
        -> ccontra [usuario]
    """
    # os.system(f"passwd {args}")
    # contra_nueva = getpass.getpass("Introduce el nuevo password")
    # click.echo(contra_nueva)
    # verificar si se cambia contrase;a en usuarios_log
    try:
        log(f"ccontra {usuario}, contrasena: {contra}")
        # TODO: Cambiar, no se puede utilizar passwd
        # os.system(f"passwd {usuario}")
        archivo = "/etc/shadow"
#         # zeus:$6$jq62gTbU$kYZgWuKLuNTX0Ur.UWiuBJuIYltW3hc7EdI2/4RpldwUoLlRl9IdXgJb6B3kxEoAxWolDwXDCqOnz8SN0CKkJ1:17739:0:99999:7:::
#         Los campos se separan por :; el primer campo es el usuario y el segundo, el hash de su password. Este hash tiene la forma $id$salt$hashed, y cada parte significa algo:

        # 6 → es algoritmo usado para el hash, donde “6” significa SHA-512.
        # jq62gTbU → el algoritmo SHA-512 requiere de un salt para combinar con la contraseña antes del hash, por seguridad.
        # kYZgWuKLuNTX0Ur.UWiuBJuIYltW3hc7EdI2/4RpldwUoLlRl9IdXgJb6B3kxEoAxWolDwXDCqOnz8SN0CKkJ1 → este es el hash propiamente dicho.
        # TODO: Cambiar a /etc/shadow
        existe_usuario = False
        with fileinput.FileInput(archivo, backup='_old', inplace=True) as file:
            for line in file:
                datos = line.split(':')
                if usuario == datos[0]:
                    # datos = line.split(':')
                    contra_hash = crypt.crypt(contra, salt=crypt.mksalt())
                    # print(line.replace(datos[2], contra_hash))
                    #datos.insert(1, contra_hash)
                    datos[1]=contra_hash
                    #datos.pop()
                    # print(*datos)
                    info = ''
                    for index, value in enumerate(datos):
                        info +=f"{value}{':' if index!=len(datos) -1 else''}"
                    print(info)
                    existe_usuario = True
                else:
                    if line != '\n':
                        print(line.replace('\n', ''))
            else:
                if not existe_usuario:
                    raise Exception("Usuario incorrecto")


    except Exception as e:
        click.echo(f"Error {e} -> Ejecute help <ccontra> para mas informacion")
        log_error.error(f"Error {e} -> al ejecutar <ccontra>")


@cli.command()
@click.argument('url')
def ftp(url):
    """Ftp brinda la posibilad de conectarse a traves del protocolo FTP. Posibilitando la tranferencia o descarga de un archivo
    Parametros: [urlFtp] -> Url del servidor FTP.
    Ejecucion: ftp [urlFtp]
    """
    # https://dlptest.com/ftp-test/

    log(f"ftp {url} ")
    try:
        ftp = ftplib.FTP(url, timeout=100)
        usuario = input("Introduce el usuario: ")
        contra = getpass.getpass("Introduce la contrasenha: ")
        ftp.login(usuario, contra)
        # ftp.retrlines("LIST")
        # (cmd, fp) cmd debe ser un RERT apropiado y fp el archivo destino
        # FTP.storlines(cmd, fp) para subir archivos
        # ftp.storbinary('STOR archivo2.txt', text_file)
        # ftp.retrbinary('RETR FTP.txt', open('archivodescargado.txt', 'wb').write)
        dec = int(input("1 - subir || 2 - descargar || 3 - salir -> "))
        while dec != 3:
            if dec == 1:
                archivo = input("Introduce el nombre del archivo(obs: con su extension al final): ")
                file = open(archivo, 'rb')
                ftp.storbinary(f'STOR {archivo}', file)
                ftp.retrlines('LIST')
            else:
                ftp.retrlines('LIST')
                archivo = input("Introduce el nombre del archivo(obs: con su extension al final)")
                ftp.retrbinary(f'RETR {archivo}', open(archivo, 'wb').write)
            with open("transferencia_log", "a+") as transferencia:
                transferencia.write(f"se realizo una transferencia ftp con el {usuario} en {url} ")
            dec = int(input("1 - subir || 2 - descargar || 3 - salir"))

        ftp.quit()
    except Exception as e:
        log_error.error(f"Error {e} -> al ejecutar <ftp>")
        click.echo("no se pudo conectar")
        click.echo(e)

@cli.command()
@click.argument('directorio_actual')
@click.argument('directorio_cambiado')
def mover(directorio_actual, directorio_cambiado):
    """
    Mover o renombrar un archivo o directorio.
    Recibe dos parametros-> <directorio_actual> <directorio_cambiado>
                          o para renombrar un archivo: <nombre_actual> <nombre_cambiado>
    Manera de ejecutar:-> mover <directorio_actual> <directorio_a_cambiar>
                    -> renombrar: mover <nombre_actual> <nombre_a_cambiar>
    """
    log(f"mover {directorio_actual} {directorio_cambiado} ")

    try:
        shutil.move(directorio_actual, directorio_cambiado)
        click.echo(f"<{directorio_actual}> fue movido a < {directorio_cambiado} >")
    except OSError:
        click.echo("Error -> nombres y rutas de archivos no válidos o inaccesibles.")
        log_error.error("nombres y rutas de archivos no válidos o inaccesibles. Al ejecutar <mover>")
    except Exception as e:
        click.echo(f"Error {e}-> Ejecute help <mover> para mas informacion")
        log_error.error(f" codigo del error: {e} -> Al ejecutar mover")


@cli.command()
@click.argument('usuario')
@click.option('--contra', prompt="Introduce la contrasena: ", hide_input=True, required=True)
def ccontra(usuario, contra):
    """ Cambiar la contrasenha de un usuario
    parametros:
        -> [usuario]
    Modo de Ejecucion:
        -> ccontra [usuario]
    """
    # os.system(f"passwd {args}")
    # contra_nueva = getpass.getpass("Introduce el nuevo password")
    # click.echo(contra_nueva)
    # verificar si se cambia contrase;a en usuarios_log
    try:
        log(f"ccontra {usuario}, contrasena: {contra}")
        # TODO: Cambiar, no se puede utilizar passwd
        # os.system(f"passwd {usuario}")
        archivo = "/etc/shadow"
#         # zeus:$6$jq62gTbU$kYZgWuKLuNTX0Ur.UWiuBJuIYltW3hc7EdI2/4RpldwUoLlRl9IdXgJb6B3kxEoAxWolDwXDCqOnz8SN0CKkJ1:17739:0:99999:7:::
#         Los campos se separan por :; el primer campo es el usuario y el segundo, el hash de su password. Este hash tiene la forma $id$salt$hashed, y cada parte significa algo:

        # 6 → es algoritmo usado para el hash, donde “6” significa SHA-512.
        # jq62gTbU → el algoritmo SHA-512 requiere de un salt para combinar con la contraseña antes del hash, por seguridad.
        # kYZgWuKLuNTX0Ur.UWiuBJuIYltW3hc7EdI2/4RpldwUoLlRl9IdXgJb6B3kxEoAxWolDwXDCqOnz8SN0CKkJ1 → este es el hash propiamente dicho.
        # TODO: Cambiar a /etc/shadow
        existe_usuario = False
        with fileinput.FileInput(archivo, backup='_old', inplace=True) as file:
            for line in file:
                datos = line.split(':')
                if usuario == datos[0]:
                    # datos = line.split(':')
                    contra_hash = crypt.crypt(contra, salt=crypt.mksalt())
                    # print(line.replace(datos[2], contra_hash))
                    #datos.insert(1, contra_hash)
                    datos[1]=contra_hash
                    #datos.pop()
                    # print(*datos)
                    info = ''
                    for index, value in enumerate(datos):
                        info +=f"{value}{':' if index!=len(datos) -1 else''}"
                    print(info)
                    existe_usuario = True
                else:
                    if line != '\n':
                        print(line.replace('\n', ''))
            else:
                if not existe_usuario:
                    raise Exception("Usuario incorrecto")


    except Exception as e:
        click.echo(f"Error {e} -> Ejecute help <ccontra> para mas informacion")
        log_error.error(f"Error {e} -> al ejecutar <ccontra>")


@cli.command()
@click.argument('url')
def ftp(url):
    """Ftp brinda la posibilad de conectarse a traves del protocolo FTP. Posibilitando la tranferencia o descarga de un archivo
    Parametros: [urlFtp] -> Url del servidor FTP.
    Ejecucion: ftp [urlFtp]
    """
    # https://dlptest.com/ftp-test/

    log(f"ftp {url} ")
    try:
        ftp = ftplib.FTP(url, timeout=100)
        usuario = input("Introduce el usuario: ")
        contra = getpass.getpass("Introduce la contrasenha: ")
        ftp.login(usuario, contra)
        # ftp.retrlines("LIST")
        # (cmd, fp) cmd debe ser un RERT apropiado y fp el archivo destino
        # FTP.storlines(cmd, fp) para subir archivos
        # ftp.storbinary('STOR archivo2.txt', text_file)
        # ftp.retrbinary('RETR FTP.txt', open('archivodescargado.txt', 'wb').write)
        dec = int(input("1 - subir || 2 - descargar || 3 - salir -> "))
        while dec != 3:
            if dec == 1:
                archivo = input("Introduce el nombre del archivo(obs: con su extension al final): ")
                file = open(archivo, 'rb')
                ftp.storbinary(f'STOR {archivo}', file)
                ftp.retrlines('LIST')
            else:
                ftp.retrlines('LIST')
                archivo = input("Introduce el nombre del archivo(obs: con su extension al final)")
                ftp.retrbinary(f'RETR {archivo}', open(archivo, 'wb').write)
            with open("transferencia_log", "a+") as transferencia:
                transferencia.write(f"se realizo una transferencia ftp con el {usuario} en {url} ")
            dec = int(input("1 - subir || 2 - descargar || 3 - salir"))

        ftp.quit()
    except Exception as e:
        log_error.error(f"Error {e} -> al ejecutar <ftp>")
        click.echo("no se pudo conectar")
        click.echo(e)

def log(comando: str) -> None:
        logging.info(f"Se ejecuto el comando -- {comando}")

@cli.command()
@click.argument('ruta', required=True,)
def uso_disco(ruta):
    """Muestra el uso en disco """
    log(f"uso-disco {ruta}")
    disk_usage = shutil.disk_usage(path=ruta)
    click.echo("Espacio total: {:.2f} GB.".format(to_gb(disk_usage.total)))
    click.echo("Espacio libre: {:.2f} GB.".format(to_gb(disk_usage.free)))
    click.echo("Espacio usado: {:.2f} GB.".format(to_gb(disk_usage.used)))

@cli.command()
@click.argument('comando', required=True,)
def ejecutar(comando):
    """ejecuta cualquier comando """
    log(f"ejecutar {comando}")
    try:
        os.system(command=comando)
    except Exception as e:
        click.echo(f"Error al ejecutar el comando {comando}\nError: {e}")


def to_gb(bytes):
    "Convierte bytes a gigabytes."
    return bytes / 1024**3

@cli.command()
@click.argument('nombre')
@click.option('--entrada', prompt="Hora de entrada-09:00", default="09:00", required=True,)
@click.option('--salida', prompt="Hora de salida-09:00", default="09:00", required=True,)
@click.option('--ip', prompt="Ip de conexion", default="127.0.0.0", required=True)
def nuevo_usuario(nombre, entrada, salida, ip):
        """Crea un nuevo usuario en el sistema. Los datos se guardan dentro del archivo /var/log/usuarios_log.
        parametros:
            -> [nombre de usuario] [hora de entrada] [hora de salida] [ip de conexion]
        Ejecucion:
            -> usuario <nombre de usuario> <hora de entrada> <hora de salida> <ip de conexion>
        """

        args = f"{nombre} {entrada} {salida} {ip}"
        log(f"usuario {args} ")
    
        with open(archivo_usuario, "a") as f: # abrimos el archivo y colocamos la informacion al final del archivo
            f.write(args + "\n")
            click.echo("Usuario Registrado en /var/log/usuarios_log")

def capture_ip():
    """Hacemos ping a 8.8.8.8 en el puerto 80 y solicitamos los datos que nos devulve una tupla (ipPrivada, tiempo)
        y como nos interesa solo la ip privada accedemos al primer elemento y retornamos.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_conexion = s.getsockname()[0]
        s.close()
        return ip_conexion
    except Exception:
        return "0.0.0.0"

def ipVerificacion(ipList, ipDeConexion):
    """verificamos que la ip de conexion se encuentre en la lista de posibles ips registradas en usuarios_log """
    for ip in ipList:
        if ip == ipDeConexion:
            return ipDeConexion
    else:
        return f"Ip no registrado = {ipDeConexion}"

def inicio_sesion(user, ip):
    """Funcion para verificar la existencia del usuario, si se encuentra en horario laboral y con alguna ip reconocidad
        Parametros: [user] -> Es el nombre de usuario de la maquina que se conecto.
                    [ip] -> ip de la maquina conectada.
        Funcion:- Hacemos uso de dos archivos, el principal usuarios_log que es donde se encuentra los datos de los usuarios registrados
            y personal_horarios_log donde guardamos las conexiones y si fue en horario o no. Ambos son abierto en modo append(agregar).
            - hacemos uso de los metodos proporcionados por datetime para la manipulacion de fechas.
        Excepciones: La primera excepcion es en el caso de que no exista el archivo usuarios_log. Nos devuelve un aviso.
            Tenemos una excepcion en el caso de que no se encuentre registrado el usuario en el archivo usuarios_log
    """
    usuario = user
    ipDeConexion = ip
    horario_actual = datetime.now()
    try:
        with open(archivo_usuario,"r+") as archivoUsuario: 
            try:
                for linea in archivoUsuario:
                    usuario_info = linea.split() 
                    if usuario == usuario_info[0]:
                        hora_entrada = datetime.strptime(usuario_info[1], "%H:%M") 
                        hora_salida = datetime.strptime(usuario_info[2], "%H:%M") 
                        ips = usuario_info[3:]
                        strIp = ipVerificacion(ips, ipDeConexion)
                        if hora_entrada.strftime("%H:%M") <= horario_actual.strftime("%H:%M") <= hora_salida.strftime("%H:%M"):
                            horario_actual = horario_actual.strftime("%m/%d/%Y, %H:%M:%S")
                            return f"{ horario_actual } - {usuario} Se conecto dentro de su horario, IP: {strIp}"
                        else:
                            horario_actual = horario_actual.strftime("%m/%d/%Y, %H:%M:%S")
                            return f"{horario_actual} - {usuario} Se conecto fuera del horario, IP: {strIp}"
                        break
                else:
                    raise Exception("No se encontro el usuario")
            except Exception as e:
                horario_actual = horario_actual.strftime("%m/%d/%Y, %H:%M:%S")
                return f"{horario_actual}: Usuario desconocido se conecto, IP: {ipDeConexion}"
    except FileNotFoundError:
        return "No hay usuarios registrados en usuarios_log. Para un nuevo usuario ejecute el comando <nuevo-usuario>"



if __name__ == '__main__':
    user = getpass.getuser()  # capturamos el nombre de usuario de la pc.
    ip_conexion = capture_ip() #capturamos la ip de la pc 

    # creamos un nuevo log con nombre sesion_log
    logger = logging.getLogger(archivo_personal_horarios)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(archivo_personal_horarios)  # /var/log/archivo_personal
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    try:
        result = inicio_sesion(user, ip_conexion) # verificamos el inicio de sesion
        print(result)
        logger.info(f'Inicio de sesion de {user}')
        cli()  # iniciamos el loop para que capture los comandos ingresados
    except KeyboardInterrupt:  # en caso de ctrl + c se ejecuta una interrupcion del teclado y se termina la sesion
        click.echo(f"\nCierre de sesion : {user} - Interrupcion de teclado")
        logger.info(f" {user} Cerro sesion por Interrupcion de teclado")
        exit()
    else:  # en cualquier caso. a la hora de salida se informa del cierre de sesion
        logger.info(f"Cierre de sesion : {user}")



