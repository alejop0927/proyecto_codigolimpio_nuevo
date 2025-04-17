class Usuario:
    def __init__(self, usuarios):  
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
