from datetime import datetime
from src.model.conexion import obtener_conexion_bd

class Sistema:
    """
    Clase que administra el sistema de gestión de usuarios y tareas.

    Funcionalidades:
        - Iniciar sesión de usuario.
        - Cambiar contraseña.
        - Editar, eliminar y mostrar tareas asignadas a un usuario.
    """

    def __init__(self):
        """
        Inicializa la conexión a la base de datos y variables de sesión del usuario.
        """
        self.conn = obtener_conexion_bd()
        self.cursor = self.conn.cursor()
        self.usuario_actual_id = None
        self.nombre_usuario = None

    def iniciar_sesion(self, correo, contraseña):
        """
        Inicia sesión del usuario.

        Parámetros:
            correo (str): Correo del usuario.
            contraseña (str): Contraseña del usuario.

        Retorna:
            str: Mensaje de bienvenida o error.
        """
        correo = correo.lower()  # Normalizar el correo a minúsculas
        self.cursor.execute("""
            SELECT id_usuario, nombre_usuario, contraseña, activo
            FROM Usuario
            WHERE correo = %s
        """, (correo,))
        resultado = self.cursor.fetchone()

        if not resultado:
            return "Error: Usuario no registrado"

        id_usuario, nombre_usuario, contraseña_db, activo = resultado

        if not activo:
            return "Error: Usuario inactivo"

        if contraseña != contraseña_db:
            return "Error: Contraseña incorrecta"

        self.usuario_actual_id = id_usuario
        self.nombre_usuario = nombre_usuario
        return f"Bienvenido {nombre_usuario}"

    def cambiar_contraseña_usuario(self, correo, contraseña_actual, nueva_contraseña, confirmar_contraseña):
        """
        Permite a un usuario cambiar su contraseña.

        Parámetros:
            correo (str): Correo del usuario.
            contraseña_actual (str): Contraseña actual del usuario.
            nueva_contraseña (str): Nueva contraseña deseada.
            confirmar_contraseña (str): Confirmación de la nueva contraseña.

        Retorna:
            str: Mensaje de éxito o error.
        """
        self.cursor.execute("""
            SELECT id_usuario, contraseña FROM Usuario WHERE correo = %s
        """, (correo,))
        resultado = self.cursor.fetchone()

        if not resultado:
            return "Error: Usuario no encontrado"

        id_usuario, contraseña_db = resultado

        if contraseña_actual != contraseña_db:
            return "Error: Contraseña actual incorrecta"

        if nueva_contraseña != confirmar_contraseña:
            return "Error: Las contraseñas no coinciden"

        self.cursor.execute("""
            UPDATE Usuario SET contraseña = %s WHERE id_usuario = %s
        """, (nueva_contraseña, id_usuario))
        self.conn.commit()
        return "Contraseña actualizada correctamente"

    def editar_tarea(self, nombre_tarea, nuevo_texto, nueva_categoria, nuevo_estado):
        """
        Permite al usuario editar una tarea existente.

        Parámetros:
            nombre_tarea (str): Nombre de la tarea a editar.
            nuevo_texto (str): Nuevo contenido de la tarea.
            nueva_categoria (str): Nueva categoría de la tarea.
            nuevo_estado (str): Nuevo estado de la tarea.

        Retorna:
            str: Mensaje de éxito o error.
        """
        if self.usuario_actual_id is None:
            return "Debes iniciar sesión"

        self.cursor.execute("""
            SELECT T.id_tarea FROM Tarea T
            JOIN Tarea_usuario TU ON T.id_tarea = TU.id_tarea
            WHERE TU.id_usuario = %s AND T.nombre_tarea = %s
        """, (self.usuario_actual_id, nombre_tarea))
        resultado = self.cursor.fetchone()

        if not resultado:
            return "Tarea no encontrada"

        id_tarea = resultado[0]

        if not nuevo_texto and not nueva_categoria and not nuevo_estado:
            return "No hay cambios registrados"

        self.cursor.execute("""
            UPDATE Tarea SET texto_tarea = %s, categoria = %s, estado = %s, fecha_creacion = %s
            WHERE id_tarea = %s
        """, (nuevo_texto, nueva_categoria, nuevo_estado, datetime.now(), id_tarea))

        self.conn.commit()
        return "Tarea actualizada correctamente"

    def eliminar_tarea(self, nombre_tarea):
        """
        Elimina una tarea asignada al usuario actual.

        Parámetros:
            nombre_tarea (str): Nombre de la tarea a eliminar.

        Retorna:
            str: Mensaje de éxito o error.
        """
        if self.usuario_actual_id is None:
            return "Error: Debe iniciar sesión"

        if not nombre_tarea:
            return "Error: Debe proporcionar un nombre de tarea"

        self.cursor.execute("""
            SELECT T.id_tarea, T.estado, TU.id_usuario
            FROM Tarea T
            JOIN Tarea_usuario TU ON T.id_tarea = TU.id_tarea
            WHERE T.nombre_tarea = %s
            LIMIT 1
        """, (nombre_tarea,))
        resultado = self.cursor.fetchone()

        if not resultado:
            return "Error: La tarea no existe"

        id_tarea, estado_tarea, id_usuario_propietario = resultado

        if id_usuario_propietario != self.usuario_actual_id:
            return "Error: No tiene permisos"

        if estado_tarea == "Completada":
            return "Error: No se puede eliminar una tarea completada"

        self.cursor.execute("""
            DELETE FROM Tarea_usuario WHERE id_tarea = %s AND id_usuario = %s
        """, (id_tarea, self.usuario_actual_id))

        self.cursor.execute("""
            DELETE FROM Tarea WHERE id_tarea = %s
        """, (id_tarea,))
        
        self.conn.commit()
        return "Tarea eliminada correctamente"

    def mostrar_tareas_usuario(self):
        """
        Muestra todas las tareas asignadas al usuario actualmente autenticado.

        Retorna:
            str | list: Mensaje de error si no ha iniciado sesión, o lista de tareas si existen.
        """
        if self.usuario_actual_id is None:
            return "Debes iniciar sesión"

        self.cursor.execute("""
            SELECT T.nombre_tarea, T.texto_tarea, T.categoria, T.estado, T.fecha_creacion
            FROM Tarea T
            JOIN Tarea_usuario TU ON T.id_tarea = TU.id_tarea
            WHERE TU.id_usuario = %s
        """, (self.usuario_actual_id,))
        tareas = self.cursor.fetchall()

        if not tareas:
            return "No tienes tareas registradas"

        return tareas
