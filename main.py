#! /usr/bin/env python
import logging
import click
from click_shell import shell
import getpass
import os

#archivo = "/var/log" path para lfs
archivo_usuario = "usuarios_log" # /var/log/usuarios_log
archivo_personal_horarios = "usuario_horarios.log" # /var/log/(usuario_horarios_log)
archivo_personal_horarios = "Shell_transferencias.log" # /var/log/(usuario_horarios_log)

#Creamos nuestro logger principal y usamos el metodo basicConfig para configurar 
logging.basicConfig( level=logging.INFO,
                    # formato del horario (YYYY-MM-DD hh:min:sec), 
                    format='%(asctime)s %(name)s %(levelname)s %(message)s', # name es el user, asctime es hora y fecha, levelname: severidad, message: mensaje del error.
                    filename="shell.log")

#creamos otro logger para guardar los errores del sistema
# cambiar el nombre del archivo a el path del log donde se desea guardar los errores
# los errores de comandos van separados de los errores de inicio de sesion
log_error = logging.getLogger("")
fhp = logging.FileHandler("errores.log")
fhp.setLevel(logging.ERROR)
log_error.addHandler(fhp)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhp.setFormatter(formatter)
log_error.addHandler(fhp)

@shell(prompt='shell> ', intro='**** Bienvenido ***')
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
@click.argument('src', nargs=-1, type=click.STRING)
@click.argument('dst', nargs=1, type=click.STRING)
def renombrar(src: str, dst: str) -> None:
        """Renombrar un archivo o directorio
        Recibe dos parametros-> <nombre_actual> <nombre_cambiado>
        Manera de ejecutar: renombrar <nombre_actual> <nombre_a_cambiar>
        """
        try:
            log(f"renombrar {src} {dst} ")
            os.rename(src,dst)
            print("<",src,">", "fue renombrado a ","<",dst,">")
        except OSError:
            print("Error -> nombres y rutas de archivos no válidos o inaccesibles.")
            log_error.error("nombres y rutas de archivos no válidos o inaccesibles. Al ejecutar <renombrar>")
        except Exception as e:
            print(f" Error: {e} -> al ejecutar <renombrar>")
            log_error.error(f" codigo del error: {e} -> al ejecutar <renombrar>")
        
def log(comando: str):
        logging.info(f"Se ejecuto el comando -- {comando}")


if __name__ == '__main__':
    user = getpass.getuser() # capturamos el nombre de usuario de la pc.
    
    # creamos un nuevo log con nombre sesion_log
    logger = logging.getLogger(archivo_personal_horarios)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(archivo_personal_horarios) #/var/log/archivo_personal
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info(f'Inicio de sesion de {user}')
    try:
        cli()  # iniciamos el loop para que capture los comandos ingresados 
    except KeyboardInterrupt: # en caso de ctrl + c se ejecuta una interrupcion del teclado y se termina la sesion
        print(f"\nCierre de sesion : {user} - Interrupcion de teclado")
        logger.info(f" {user} Cerro sesion por Interrupcion de teclado")
        exit()
    else: # en cualquier caso. a la hora de salida se informa del cierre de sesion
        logger.info(f"Cierre de sesion : {user}")


