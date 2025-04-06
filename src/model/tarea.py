from src.model.db_global import db  
from datetime import datetime

class Tarea:
    def __init__(self, nombre_tarea, texto_tarea, fecha_creacion_tarea, categoria_tarea, estado_tarea):
        self.nombre_tarea = nombre_tarea
        self.texto_tarea = texto_tarea
        self.fecha_creacion_tarea = fecha_creacion_tarea
        self.categoria_tarea = categoria_tarea
        self.estado_tarea = estado_tarea

class Crear(Tarea):
    def crear_tareas(self):
        correo = db.usuario_actual
        if correo is None:
            return "No hay ningún usuario logueado."

        nombre_tarea = input("Ingrese el título de la tarea: ")

        if correo not in db.usuarios_tareas:
            db.usuarios_tareas[correo] = []

        for tarea in db.usuarios_tareas[correo]:
            if tarea["nombre"] == nombre_tarea:
                return "La tarea ya existe."

        texto_tarea = input("Ingrese el texto de la tarea: ")
        if not texto_tarea:
            return "Error: El texto no puede estar vacío"

        fecha_creacion_tarea = datetime.now()
        categoria_tarea = input("Ingrese una categoría para la tarea: ")
        if not categoria_tarea:
            return "Error: La categoría es requerida"

        estado_tarea = input("Estado de la tarea (Completada, Por Hacer, En Progreso): ")
        if not estado_tarea:
            return "Error: El estado es requerido"

        db.usuarios_tareas[correo].append({
            "nombre": nombre_tarea,
            "texto": texto_tarea,
            "fecha": fecha_creacion_tarea.strftime("%Y-%m-%d %H:%M:%S"),
            "categoría": categoria_tarea,
            "estado": estado_tarea
        })

        return "Tarea creada con éxito."


class Editar:
    def editar_tarea(self):
        correo = db.usuario_actual
        if correo is None:
            return "No hay usuario logueado."

        nombre_tarea = input("Ingrese el título de la tarea que desea editar: ")

        tareas = db.usuarios_tareas.get(correo, [])
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

    
class Eliminar:
    def eliminar_tarea(self):
        correo = db.usuario_actual
        if correo is None:
            return "No hay usuario logueado."

        nombre_tarea = input("Ingrese el título de la tarea que desea eliminar: ")

        if not nombre_tarea:
            return "Error: Debe proporcionar un ID"

        tareas = db.usuarios_tareas.get(correo, [])
        for i, tarea in enumerate(tareas):
            if tarea["nombre"] == nombre_tarea:
                del tareas[i]
                return "Tarea eliminada."

        return "Tarea no encontrada."
        
class Mostrar:
    def mostrar_tareas_usuario(self):
        correo = db.usuario_actual
        if correo is None:
            print("No hay usuario logueado.")
            return

        tareas = db.usuarios_tareas.get(correo, [])
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


