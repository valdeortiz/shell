import logging
import click
import getpass

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

@click.group()
def cli():
    pass

@cli.command()
def bienvenida(args):
    """emite un mensaje de bienvenida """
    print("Bienvenido!")

@cli.command()
def salida( args):
    """Termina el loop y emite un mensaje de despedida """
    print("Hasta pronto!")
    return True 
    
def log( args):
        logging.info(f"Se ejecuto el comando -- {args}")



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


