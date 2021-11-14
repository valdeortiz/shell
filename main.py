#! /usr/bin/env python
import shutil
import click
import logging
from click_shell import shell
import getpass
import os
import ftplib
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


# UpdatePrompt=os.getcwd()
#def UpdatePrompt():
#    return f"shell>{os.getcwd()}>"


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
@click.argument('ruta',type=click.Path(exists=True))
def ir(ruta):
    """Cambio de Directorio."""
    log(f'ir {ruta}')
    try:
        os.chdir(ruta)
        click.echo(f"Directorio actual: {os.getcwd()}")
        log("cambio al directorio: " + os.getcwd())
    except:
        log("No es posible acceder al directorio o no existe.")
        click.echo("No es posible acceder al directorio o no existe.")


@cli.command()
@click.argument('source', type=click.Path(exists=True), nargs=1)
@click.argument('destination', type=click.Path(exists=True), nargs=1)
def copiar(origen,destino):
    """Copia un archivo a un directorio."""
    log(f'copiar {origen} {destino}')
    try:
        shutil.copy(origen, destino)
        click.echo(f"Se copio {click.format_filename(origen)} a {click.format_filename(destino)} con exito.")
        log(f"Se copio {click.format_filename(origen)} a {click.format_filename(destino)} con exito.")
    except:
        log_error.error("Error al copiar documentos, no tiene los permisos necesarios o error al especificar la ubicacion"
              "de los archivos o directorios")

@cli.command()
@click.argument('usuario',nargs=1)
@click.argument('grupo', nargs=1)
@click.argument('archivo', type=click.Path(exists=True),nargs=1)
def propietarios(usuario,grupo,archivo):
    try:
        log(f"propietarios {grupo}  {usuario} {archivo}")
        os.chown(archivo, usuario, grupo)
    except OSError:
        click.echo("Error -> nombres y archivos especificados no válidos o no es posible modificarlos.")
        log_error.error("nombres y rutas de archivos no válidos o inaccesibles. Al ejecutar <propietarios>")


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
        os.rename(origen, destino)
        click.echo(f" { origen } fue renombrado a { destino} >")
    except OSError:
        click.echo("Error -> nombres y rutas de archivos no válidos o inaccesibles.")
        log_error.error("nombres y rutas de archivos no válidos o inaccesibles. Al ejecutar <renombrar>")
    except Exception as e:
        click.echo(f" Error: {e} -> al ejecutar <renombrar>")
        log_error.error(f" codigo del error: {e} -> al ejecutar <renombrar>")


# os.geteuid() para saber el userid
# os.getgid() para saber el grupid
@cli.command()
@click.argument('ruta', type=click.Path(exists=True))
@click.argument('permisos', type=click.INT)
def cambiarpermisos(ruta, permisos: int):
    """
    Cambiar los permisos de un archivo o directorio.
    Recibe dos parametros-> <ruta> <permisos>
    Manera de ejecutar:-> cambiarpermisos <ruta> <permisos>
    """
    try:
        os.chmod(ruta, int(permisos, 8))  # EL segundo parametro que recibe chmod debe ser entero y en octal
        click.echo("<", ruta, ">", "permisos cambiado")
    except OSError:
        click.echo("Error -> nombres y rutas de archivos no válidos o inaccesibles.")
        log_error.error("nombres y rutas de archivos no válidos o inaccesibles. Al ejecutar <permisos>")
    except Exception as e:
        click.echo(f"Error {e}-> Ejecute help <permisos> para mas informacion")
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
        #os.system(f"passwd {args}")
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
        #https://dlptest.com/ftp-test/

        log(f"ftp {url} ")
        try:
            ftp = ftplib.FTP(url, timeout=100)
            usuario = input("Introduce el usuario: ")
            contra = getpass.getpass("Introduce la contrasenha: ")
            ftp.login(usuario, contra)
            #ftp.retrlines("LIST")
            # (cmd, fp) cmd debe ser un RERT apropiado y fp el archivo destino
            #FTP.storlines(cmd, fp) para subir archivos
            #ftp.storbinary('STOR archivo2.txt', text_file)
            #ftp.retrbinary('RETR FTP.txt', open('archivodescargado.txt', 'wb').write)
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
                with open("transferencia_log","a+") as transferencia:
                    transferencia.write(f"se realizo una transferencia ftp con el {usuario} en {url} ")   
                dec = int(input("1 - subir || 2 - descargar || 3 - salir"))

            ftp.quit()
        except Exception as e:
            log_error.error(f"Error {e} -> al ejecutar <ftp>")
            click.echo("no se pudo conectar")
            click.echo(e)    

def log(comando: str) -> None:
    logging.info(f"Se ejecuto el comando -- {comando}")


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

