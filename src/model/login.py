from .Usuario import Usuario
from src.model.db_global import db  


class Inicio_sesion:
    def iniciar_sesion(self):
        Correo = input("Ingrese su correo: ").lower()  
        Contraseña = input("Ingrese su contraseña: ")
        
        if Correo not in db.usuarios:
            return "Error: Usuario no registrado"
        
        if not db.usuarios[Correo].get("Activo", True):  
            return "Error: Usuario inactivo"
        
        if Contraseña == db.usuarios[Correo]["Contraseña"]:
            db.usuario_actual = Correo
            return f"Bienvenido {db.usuarios[Correo]['Nombre']}"
        
        return "Error: Credenciales incorrectas"
