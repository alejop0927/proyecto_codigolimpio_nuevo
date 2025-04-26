from datetime import datetime
from src.model.conexion import obtener_conexion_bd

class Tarea:
    """
    Clase que representa una tarea y permite su creación y asignación a un usuario específico en la base de datos.
    """

    def __init__(self, usuario_id, nombre_tarea, texto_tarea, categoria, estado):
        """
        Inicializa una nueva tarea y la registra en la base de datos si los datos son válidos.

        Parámetros:
            usuario_id (int): ID del usuario al que se le asignará la tarea.
            nombre_tarea (str): Nombre de la tarea (no debe estar vacío ni repetido para el mismo usuario).
            texto_tarea (str): Descripción o contenido de la tarea.
            categoria (str): Categoría de la tarea.
            estado (str): Estado inicial de la tarea (ej. 'pendiente', 'completada').
        """
        if not nombre_tarea:
            raise ValueError("Error: El nombre de la tarea es requerido")

        if not texto_tarea:
            raise ValueError("Error: El texto no puede estar vacío")

        if not categoria:
            raise ValueError("Error: La categoría es requerida")

        if not estado:
            raise ValueError("Error: El estado es requerido")

        conn = obtener_conexion_bd()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT correo FROM usuario WHERE id_usuario = %s", (usuario_id,))
            resultado = cursor.fetchone()
            if not resultado:
                raise ValueError("Error: El usuario no existe en la base de datos.")

            correo_usuario = resultado[0]

            cursor.execute("""
                SELECT t.id_tarea 
                FROM tarea t
                JOIN tarea_usuario tu ON t.id_tarea = tu.id_tarea
                WHERE t.nombre_tarea = %s AND tu.id_usuario = %s""", 
                (nombre_tarea, usuario_id))

            if cursor.fetchone():
                raise ValueError("La tarea ya existe para este usuario.")

            fecha_creacion = datetime.now()
            cursor.execute(
                "INSERT INTO tarea (nombre_tarea, texto_tarea, categoria, estado, fecha_creacion) VALUES (%s, %s, %s, %s, %s)",
                (nombre_tarea, texto_tarea, categoria, estado, fecha_creacion)
            )
            conn.commit()

            cursor.execute("SELECT currval(pg_get_serial_sequence('tarea','id_tarea'))")
            id_tarea = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO tarea_usuario (id_tarea, id_usuario) VALUES (%s, %s)",
                (id_tarea, usuario_id)
            )
            conn.commit()

            print(f"Tarea '{nombre_tarea}' creada con éxito y asignada a {correo_usuario}.")

        except Exception as e:
            print(f"Error al crear la tarea: {e}")
        finally:
            cursor.close()
            conn.close()
