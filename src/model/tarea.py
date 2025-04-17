from datetime import datetime

class Tarea:
    def __init__(self, usuarios_tareas, usuario_actual):
        correo = usuario_actual
        if correo is None:
            print("No hay ningún usuario logueado.")
            return

        nombre_tarea = input("Ingrese el título de la tarea: ")
        if correo not in usuarios_tareas:
            usuarios_tareas[correo] = []

        for tarea in usuarios_tareas[correo]:
            if tarea["nombre"] == nombre_tarea:
                print("La tarea ya existe.")
                return

        texto_tarea = input("Ingrese el texto de la tarea: ")
        if not texto_tarea:
            print("Error: El texto no puede estar vacío")
            return

        categoria_tarea = input("Ingrese una categoría para la tarea: ")
        if not categoria_tarea:
            print("Error: La categoría es requerida")
            return

        estado_tarea = input("Estado de la tarea (Completada, Por Hacer, En Progreso): ")
        if not estado_tarea:
            print("Error: El estado es requerido")
            return

        tarea = {
            "nombre": nombre_tarea,
            "texto": texto_tarea,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "categoría": categoria_tarea,
            "estado": estado_tarea
        }

        usuarios_tareas[correo].append(tarea)  

        print("Tarea creada con éxito.")

        
        
        

   


