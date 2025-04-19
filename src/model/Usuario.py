class Usuario:
    """
    Clase para crear un nuevo usuario mediante la entrada de datos por consola.
    """
    def __init__(self, usuarios):
        """
        Inicializa un nuevo usuario y lo agrega al diccionario de usuarios si los datos son válidos.

        Args:
            usuarios (dict): Diccionario de usuarios existentes.

        """
        correo = input("Ingrese su correo: ")
        if correo in usuarios:
            print("Error: Correo ya registrado")
            return
        
        nombre = input("Ingrese su nombre: ")
        if not nombre or len(nombre) > 50:
            print("Error: Nombre demasiado largo o faltante")
            return

        apellido = input("Ingrese su apellido: ")
        if not apellido:
            print("Error: Apellido faltante")
            return

        contraseña = input("Ingrese su contraseña: ")
        if len(contraseña) > 100:
            print("Error: Contraseña demasiado larga")
            return
        if len(contraseña) < 8:
            print("Error: Contraseña demasiado débil")
            return

        usuarios[correo] = {
            "Nombre": nombre,
            "Apellido": apellido,
            "Correo": correo,
            "Contraseña": contraseña
        }

        print("Usuario creado con éxito")

class Usuario_kv:
    """
    Clase para crear un nuevo usuario mediante la entrada de datos desde la interfaz Kivy.
    """
    def __init__(self, nombre, apellido, correo, contraseña, usuarios):
        """
        Inicializa un nuevo usuario y lo agrega al diccionario de usuarios si los datos son válidos.

        Args:
            nombre (str): Nombre del usuario.
            apellido (str): Apellido del usuario.
            correo (str): Correo electrónico del usuario.
            contraseña (str): Contraseña del usuario.
            usuarios (dict): Diccionario de usuarios existentes.

        """
        if correo in usuarios:
            print("Error: Correo ya registrado")
            return
        
        if not nombre or len(nombre) > 50:
            print("Error: Nombre demasiado largo o faltante")
            return
        
        if not apellido:
            print("Error: Apellido faltante")
            return
        
        if len(contraseña) > 100:
            print("Error: Contraseña demasiado larga")
            return
        
        if len(contraseña) < 8:
            print("Error: Contraseña demasiado débil")
            return

        usuarios[correo] = {
            "Nombre": nombre,
            "Apellido": apellido,
            "Correo": correo,
            "Contraseña": contraseña
        }

        print("Usuario creado con éxito")
