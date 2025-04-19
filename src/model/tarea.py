from datetime import datetime

class Tarea:
    """
    Clase para crear una nueva tarea mediante la entrada de datos por consola.
    """
    def __init__(self, usuarios_tareas, usuario_actual):
        """
        Inicializa una nueva tarea y la agrega al diccionario de tareas del usuario si los datos son válidos.

        Args:
            usuarios_tareas (dict): Diccionario de tareas de los usuarios.
            usuario_actual (str): Correo del usuario actual logueado.

        """
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

class Tarea_kv:
    """
    Clase para crear una nueva tarea mediante la entrada de datos desde la interfaz Kivy.
    """
    def __init__(self, nombre_tarea, texto_tarea, categoria_tarea, estado_tarea, usuarios_tareas, usuario_actual):
        """
        Inicializa una nueva tarea y la agrega al diccionario de tareas del usuario si los datos son válidos.

        Args:
            nombre_tarea (str): Título de la tarea.
            texto_tarea (str): Descripción de la tarea.
            categoria_tarea (str): Categoría de la tarea.
            estado_tarea (str): Estado de la tarea (Completada, Por Hacer, En Progreso).
            usuarios_tareas (dict): Diccionario de tareas de los usuarios.
            usuario_actual (str): Correo del usuario actual logueado.

        """
        correo = usuario_actual
        if correo is None:
            print("No hay ningún usuario logueado.")
            return

        if correo not in usuarios_tareas:
            usuarios_tareas[correo] = []

        for tarea in usuarios_tareas[correo]:
            if tarea["nombre"] == nombre_tarea:
                print("La tarea ya existe.")
                return

        if not texto_tarea:
            print("Error: El texto no puede estar vacío")
            return

        if not categoria_tarea:
            print("Error: La categoría es requerida")
            return

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
