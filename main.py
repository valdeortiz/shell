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
# archivo = "/var/log" path para lfs
archivo_usuario = "usuarios_log"  # /var/log/usuarios_log
archivo_personal_horarios = "usuario_horarios.log"  # /var/log/(usuario_horarios_log)
archivo_personal_horarios = "Shell_transferencias.log"  # /var/log/(usuario_horarios_log)



# archivo = "/var/log" path para lfs
archivo_usuario = "usuarios_log"  # /var/log/usuarios_log
archivo_personal_horarios = "usuario_horarios.log"  # /var/log/(usuario_horarios_log)
archivo_personal_horarios = "Shell_transferencias.log"  # /var/log/(usuario_horarios_log)


# Creamos nuestro logger principal y usamos el metodo basicConfig para configurar
logging.basicConfig(level=logging.INFO,
                    # formato del horario (YYYY-MM-DD hh:min:sec),
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    # name es el user, asctime es hora y fecha, levelname: severidad, message: mensaje del error.
                    filename="shell.log")

# creamos otro logger para guardar los errores del sistema
# cambiar el nombre del archivo a el path del log donde se desea guardar los errores
# los errores de comandos van separados de los errores de inicio de sesion
log_error = logging.getLogger("")
fhp = logging.FileHandler("errores.log")
fhp.setLevel(logging.ERROR)
log_error.addHandler(fhp)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhp.setFormatter(formatter)
log_error.addHandler(fhp)



@shell(prompt=f'shell>', intro='**** Bienvenido ***')
def cli():
    pass


@cli.command()
def bienvenida():
    """emite un mensaje de bienvenida """
    click.echo("Bienvenido!")
    pass


@cli.command()
def salida():
    """Termina el loop y emite un mensaje de despedida """
    click.echo("Hasta pronto!")
    return True

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

@cli.command()
@click.argument('l', default='')
def diractual():

    """Imprime en pantalla el directorio actual"""
    log("diractual")
    try:
        click.echo(f"Directorio actual: {os.getcwd()}")
    except:
        log_error.error("Error al mostrar el directorio actual.")

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

@cli.command()
@click.argument('usuario',nargs=1)
@click.argument('grupo', nargs=1)
@click.argument('archivo',nargs=1)
def propietarios(usuario,grupo,archivo):
    """Cambia el propietario de un directorio"""
    try:
        if os.path.exists(archivo):
            log(f"propietarios {grupo}  {usuario} {archivo}")
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

#os.geteuid() para saber el userid
    #os.getgid() para saber el grupid


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
def ccontra(usuario):
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
        log(f"ccontra {usuario} ")
        # el nombre original debe de ser cambiarContra pero no tengo nh por eso uso ccontra
        os.system(f"passwd {usuario}")
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

if __name__ == '__main__':
    user = getpass.getuser()  # capturamos el nombre de usuario de la pc.

    # creamos un nuevo log con nombre sesion_log
    logger = logging.getLogger(archivo_personal_horarios)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(archivo_personal_horarios)  # /var/log/archivo_personal
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info(f'Inicio de sesion de {user}')
    try:
        cli()  # iniciamos el loop para que capture los comandos ingresados
    except KeyboardInterrupt:  # en caso de ctrl + c se ejecuta una interrupcion del teclado y se termina la sesion
        click.echo(f"\nCierre de sesion : {user} - Interrupcion de teclado")
        logger.info(f" {user} Cerro sesion por Interrupcion de teclado")
        exit()
    else:  # en cualquier caso. a la hora de salida se informa del cierre de sesion
        logger.info(f"Cierre de sesion : {user}")



