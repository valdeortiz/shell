import logging
from cmd import cmd
#archivo = "/var/log" path para lfs
archivo_usuario = "usuarios_log" # /var/log/usuarios_log
archivo_personalHorarios = "personal_horarios_log" # /var/log/personal_horarios_log

class Comandos(cmd):
    """
        Clase principal que hereda de la clase Cmd
        que contiene todo lo necesario para la construccion
        de la shell.
    """
    # Atributos de la clase Cmd
    intro = "***  Shell  *** \n=> introduzca <help> para visualizar los comandos." #Mensaje de bienvenida al ejecutarse la shell
    prompt = "Introduza un comando: " #mensaje a la izquierda del comando
    misc_header="Documentacion de los metodos" 
    doc_header = "Ayuda de comandos documentados. Presione help <comando>"
    undoc_header="Los siguientes comandos no estan documentados:"
    ruler = "*" # caracter separador al ejecutar help=menu de ayuda
    
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

    def do_salir(self, args):
        """Termina el loop y emite un mensaje de despedida """
        print("Hasta pronto!")
        return True 


if __name__ == '__main__':
    user = 'Admin'
    logger = logging.getLogger(archivo_personalHorarios)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(archivo_personalHorarios) #/var/log/archivo_personal
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info(f'Inicio de sesion de {user}')
    try:
        Comandos().cmdloop()  # iniciamos el loop para que capture los comandos ingresados 
    except KeyboardInterrupt: # en caso de ctrl + c se ejecuta una interrupcion del teclado y se termina la sesion
        print(f"\nCierre de sesion : {user} - Interrupcion de teclado")
        logger.info(f" {user} Cerro sesion por Interrupcion de teclado")
        exit()
    else: # en cualquier caso. a la hora de salida se informa del cierre de sesion
        logger.info(f"Cierre de sesion : {user}")


