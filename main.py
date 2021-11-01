#! /usr/bin/env python
import shutil
import click
import logging
from click_shell import shell
import getpass
import os
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


#UpdatePrompt=os.getcwd()
def UpdatePrompt():#Esto no funciona por alguna razon
    return f"shell>{os.getcwd()}>"

@shell(prompt=f'[{UpdatePrompt()}]>', intro='**** Bienvenido ***')
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
@click.argument('path')
def ir(path):
    """Cambio de Directorio."""
    log(f'ir {path}')
    try:
        os.chdir(path)
        log("cambio al directorio: " + os.getcwd())
    except:
        log("No es posible acceder al directorio o no existe.")
        click.echo("No es posible acceder al directorio o no existe.")


@cli.command()
@click.argument('source', type=click.Path(exists=True))
@click.argument('destination', type=click.Path(exists=True))
def copiar(source,destination):
    """Copia un archivo a un directorio."""
    log(f'copiar {source} {destination}')
    try:
        shutil.copy(source, destination)
        click.echo(f"Se copio {click.format_filename(source)} a {click.format_filename(destination)} con exito.")
        log(f"Se copio {click.format_filename(source)} a {click.format_filename(destination)} con exito.")
    except:
        log_error.error("Error al copiar documentos, no tiene los permisos necesarios o error al especificar la ubicacion"
              "de los archivos o directorios")

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
@click.argument('ruta', type=click.Path(exists=True))
@click.argument('permisos', type=click.INT)
def cambiarpermisos(ruta, permisos: int):
    """
    Cambiar los permisos de un archivo o directorio. 
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


