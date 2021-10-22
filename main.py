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
    print("Bienvenido!")
    pass


@cli.command()
def salida():
    """Termina el loop y emite un mensaje de despedida """
    print("Hasta pronto!")
    return True

@cli.command()
@click.argument('path')
def ir(path):
    """Cambio de Directorio."""
    try:
        os.chdir(path)
        print("Directorio Actual: ", os.getcwd())
    except:
        print("No es posible acceder al directorio o no existe.")

@cli.command()
@click.argument('SOURCE', type=click.Path(exists=True))
@click.argument('DESTINATION', type=click.Path(exists=True))
def copiar(SOURCE,DESTINATION):
    """Copia un archivo a un directorio."""
    try:
        shutil.copy(SOURCE, DESTINATION)
        print(f"Se copio {click.format_filename(SOURCE)} a {click.format_filename(DESTINATION)} con exito.")
    except:
        print("Error al copiar documentos, no tiene los permisos necesarios o error al especificar la ubicación"
              "del archivo o directorio")



def log(args):
    logging.info(f"Se ejecuto el comando -- {args}")


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
        print(f"\nCierre de sesion : {user} - Interrupcion de teclado")
        logger.info(f" {user} Cerro sesion por Interrupcion de teclado")
        exit()
    else:  # en cualquier caso. a la hora de salida se informa del cierre de sesion
        logger.info(f"Cierre de sesion : {user}")


