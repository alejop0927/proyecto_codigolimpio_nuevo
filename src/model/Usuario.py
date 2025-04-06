from src.model.db_global import db 


class Usuario:
    def __init__(self, Nombre, Apellido, Correo, Contraseña):
        self.Nombre = Nombre
        self.Apellido = Apellido
        self.Correo = Correo
        self.Contraseña = Contraseña

class Crear_cuenta:
    def crear_cuenta_usuario(self):
        Correo = input("Ingrese su correo: ")
        
        if Correo in db.usuarios:
            return "Error: Correo ya registrado"

        Nombre = input("Ingrese su nombre: ")
        if len(Nombre) > 50:
            return "Error: Nombre demasiado largo"

        Apellido = input("Ingrese su apellido: ")
        Contraseña = input("Ingrese su contraseña: ")
        if len(Contraseña) > 100:
            return "Error: Contraseña demasiado larga"
        if len(Contraseña) < 8:
            return "Error: Contraseña demasiado débil"

        if not Correo or not Nombre or not Apellido or not Contraseña:
            return "Error: Datos obligatorios faltantes"

        nuevo_usuario = Usuario(Nombre, Apellido, Correo, Contraseña)

        db.usuarios[Correo] = {
            "Nombre": nuevo_usuario.Nombre,
            "Apellido": nuevo_usuario.Apellido,
            "Correo": nuevo_usuario.Correo,
            "Contraseña": nuevo_usuario.Contraseña
        }

        return "Usuario creado con éxito"
        
class Cambiar_contraseña:
    def cambiar_contraseña_usuario(self):
        intentos = 3
        
        Correo = input("Ingrese su correo: ")
        
        if Correo not in db.usuarios:
            return "Error: Usuario no registrado"
        
        if not db.usuarios[Correo]["Activo"]:
            return "Error: Usuario inactivo"
        
        contraseña_actual = input("Ingrese su contraseña actual: ")
        if db.usuarios[Correo]["Contraseña"] != contraseña_actual:
            return "Error: Contraseña incorrecta"
        
        while intentos > 0:
            nueva_contraseña = input("Ingrese una contraseña nueva: ")
            escribir_nuevamente_nueva_contraseña = input("Ingrese nuevamente la contraseña nueva: ")
            if nueva_contraseña == escribir_nuevamente_nueva_contraseña:
                if len(nueva_contraseña) > 320:
                    return "Error: Contraseña demasiado larga"
                db.usuarios[Correo]["Contraseña"] = escribir_nuevamente_nueva_contraseña
                return "Contraseña actualizada con éxito"
            else:
                intentos -= 1
                print(f"Las contraseñas son diferentes, te quedan {intentos} intentos disponibles")
        
        return "Demasiados intentos fallidos, inténtalo más tarde"

            
            
