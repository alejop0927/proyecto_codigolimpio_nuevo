from datetime import datetime
class Sistema:
    def __init__(self):
        self.usuarios = {}
        self.usuarios_tareas = {}
        self.usuario_actual = None

    def cambiar_contraseña_usuario(self):
        intentos = 3
        
        correo = input("Ingrese su correo: ")
        
        if correo not in self.usuarios:
            return "Error: Usuario no registrado"
        
        if not self.usuarios[correo]["Activo"]:
            return "Error: Usuario inactivo"
        
        contraseña_actual = input("Ingrese su contraseña actual: ")
        if self.usuarios[correo]["Contraseña"] != contraseña_actual:
            return "Error: Contraseña incorrecta"
        
        while intentos > 0:
            nueva_contraseña = input("Ingrese una contraseña nueva: ")
            escribir_nuevamente_nueva_contraseña = input("Ingrese nuevamente la contraseña nueva: ")
            if nueva_contraseña == escribir_nuevamente_nueva_contraseña:
                if len(nueva_contraseña) > 320:
                    return "Error: Contraseña demasiado larga"
                self.usuarios[correo]["Contraseña"] = escribir_nuevamente_nueva_contraseña
                return "Contraseña actualizada con éxito"
            else:
                intentos -= 1
                print(f"Las contraseñas son diferentes, te quedan {intentos} intentos disponibles")
        
        return "Demasiados intentos fallidos, inténtalo más tarde"

    def iniciar_sesion(self):
        correo = input("Ingrese su correo: ").lower()  
        contraseña = input("Ingrese su contraseña: ")
        
        if correo not in self.usuarios:
            return "Error: Usuario no registrado"
        
        if not self.usuarios[correo].get("Activo", True):  
            return "Error: Usuario inactivo"
        
        if contraseña == self.usuarios[correo]["Contraseña"]:
            self.usuario_actual = correo
            return f"Bienvenido {self.usuarios[correo]['Nombre']}"
        
        return "Error: Credenciales incorrectas"

    def editar_tarea(self):
        correo = self.usuario_actual
        if correo is None:
            return "No hay usuario logueado."

        nombre_tarea = input("Ingrese el título de la tarea que desea editar: ")

        tareas = self.usuarios_tareas.get(correo, [])
        for tarea in tareas:
            if tarea["nombre"] == nombre_tarea:
                nuevo_texto = input("Ingresa el nuevo texto de la tarea: ")
                nueva_categoria = input("Ingrese una nueva categoría para la tarea: ")
                nuevo_estado = input("Estado actualizado de la tarea (Completada, Por Hacer, En Progreso): ")

                if not nuevo_texto and not nueva_categoria and not nuevo_estado:
                    return "Error: No hay cambios registrados"

                tarea["texto"] = nuevo_texto if nuevo_texto else tarea["texto"]
                tarea["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                tarea["categoría"] = nueva_categoria if nueva_categoria else tarea["categoría"]
                tarea["estado"] = nuevo_estado if nuevo_estado else tarea["estado"]
                return "Tarea actualizada con éxito."

        return "La tarea no existe."

    def eliminar_tarea(self):
        correo = self.usuario_actual
        if correo is None:
            return "No hay usuario logueado."

        nombre_tarea = input("Ingrese el título de la tarea que desea eliminar: ")

        if not nombre_tarea:
            return "Error: Debe proporcionar un ID"

        tareas = self.usuarios_tareas.get(correo, [])
        for i, tarea in enumerate(tareas):
            if tarea["nombre"] == nombre_tarea:
                del tareas[i]
                return "Tarea eliminada."

        return "Tarea no encontrada."

    def mostrar_tareas_usuario(self):
        correo = self.usuario_actual
        if correo is None:
            print("No hay usuario logueado.")
            return

        tareas = self.usuarios_tareas.get(correo, [])
        if not tareas:
            print("No tienes tareas.")
            return

        for tarea in tareas:
            print("\n---")
            print(f"Nombre: {tarea['nombre']}")
            print(f"Texto: {tarea['texto']}")
            print(f"Fecha: {tarea['fecha']}")
            print(f"Categoría: {tarea['categoría']}")
            print(f"Estado: {tarea['estado']}")
