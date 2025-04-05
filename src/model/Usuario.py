from .base_datos import Base_datos

class Usuario:
    def __init__(self, Nombre, Apellido, Correo, Contraseña):
        self.Nombre = Nombre
        self.Apellido = Apellido
        self.Correo = Correo
        self.Contraseña = Contraseña

class Crear_cuenta(Usuario):
    def crear_cuenta_usuario(self):
        Correo = input("Ingrese su correo: ")
        
        if Correo in Base_datos.usuarios:
            print("El usuario ya existe.")
            return

        Nombre = input("Ingrese su nombre: ")
        Apellido = input("Ingrese su apellido: ")
        Contraseña = input("Ingrese su contraseña: ")

        
        nuevo_usuario = Usuario(Nombre, Apellido, Correo, Contraseña)

        
        Base_datos.usuarios[Correo] = {
            "Nombre": nuevo_usuario.Nombre,
            "Apellido": nuevo_usuario.Apellido,
            "Correo": nuevo_usuario.Correo,
            "Contraseña": nuevo_usuario.Contraseña
        }

        print("✅ Usuario creado con éxito.")
        
class Cambiar_contraseña:
    def cambiar_contraseña_usuario(self):
        intentos=3
        
        Correo = input("Ingrese su correo: ")
        
        if Correo not in Base_datos.usuarios:
            print("El usuario no existe.")
        
        while intentos>0:
           nueva_contraseña=input("ingrese una contraseña nueva")
           escribir_nuevamente_nueva_contraseña=input("ingrese una contraseña nueva")
           if nueva_contraseña == escribir_nuevamente_nueva_contraseña:
             Base_datos.Usuarios[Correo]["Contraseña"]=escribir_nuevamente_nueva_contraseña
             print("contraseña actualizada con exito")
             break
           else:
             intentos-=1
             print(f"las contraseñas son diferentes, te quedan {intentos} intentos disponibles")
        if intentos ==0:
            print("demasiados intentos fallidos, intentalo mas tarde")
             
            
            
