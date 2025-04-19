from datetime import datetime

class Sistema:
    """
    Clase que gestiona el sistema de usuarios y tareas. Permite la creación de cuentas, inicio de sesión,
    edición y eliminación de tareas, y actualización de contraseñas de usuario.

    Atributos:
        usuarios (dict): Diccionario que almacena los usuarios registrados, con el correo como clave.
        usuarios_tareas (dict): Diccionario que almacena las tareas de cada usuario, con el correo como clave.
        usuario_actual (str | None): Correo del usuario actualmente autenticado. Si no hay usuario autenticado, es None.

    Métodos:
        cambiar_contraseña_usuario(): Permite cambiar la contraseña de un usuario autenticado.
        iniciar_sesion(): Permite iniciar sesión con el correo y la contraseña de un usuario.
        editar_tarea(): Permite editar una tarea de un usuario autenticado.
        eliminar_tarea(): Permite eliminar una tarea de un usuario autenticado.
        mostrar_tareas_usuario(): Muestra todas las tareas de un usuario autenticado.
    """

    def __init__(self):
        self.usuarios = {}
        self.usuarios_tareas = {}
        self.usuario_actual = None

    def cambiar_contraseña_usuario(self):
        """
        Permite cambiar la contraseña de un usuario autenticado, solicitando la contraseña actual
        y una nueva contraseña que debe ser confirmada.

        Returns:
            str: Mensaje indicando si la contraseña se actualizó con éxito o si hubo un error.
        """
        intentos = 3
        correo = input("Ingrese su correo: ")

        if correo not in self.usuarios:
            return "Error: Usuario no registrado"
        if not self.usuarios[correo].get("Activo", True):
            return "Error: Usuario inactivo"

        contraseña_actual = input("Ingrese su contraseña actual: ")
        if self.usuarios[correo]["Contraseña"] != contraseña_actual:
            return "Error: Contraseña incorrecta"

        while intentos > 0:
            nueva_contraseña = input("Ingrese una contraseña nueva: ")
            confirmar = input("Ingrese nuevamente la contraseña nueva: ")
            if nueva_contraseña == confirmar:
                if len(nueva_contraseña) > 320:
                    return "Error: Contraseña demasiado larga"
                self.usuarios[correo]["Contraseña"] = nueva_contraseña
                return "Contraseña actualizada con éxito"
            else:
                intentos -= 1
                print(f"Las contraseñas son diferentes, te quedan {intentos} intentos disponibles")

        return "Demasiados intentos fallidos, inténtalo más tarde"

    def iniciar_sesion(self):
        """
        Permite iniciar sesión con el correo y la contraseña de un usuario.

        Returns:
            str: Mensaje indicando si el inicio de sesión fue exitoso o si hubo un error.
        """
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
        """
        Permite editar una tarea de un usuario autenticado.

        Returns:
            str: Mensaje indicando si la tarea fue actualizada con éxito o si hubo un error.
        """
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
        """
        Permite eliminar una tarea de un usuario autenticado.

        Returns:
            str: Mensaje indicando si la tarea fue eliminada con éxito o si no se encontró.
        """
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
        """
        Muestra todas las tareas de un usuario autenticado.

        Returns:
            None: Imprime las tareas del usuario en consola o un mensaje de error si no hay tareas.
        """
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

class Sistema_KV:
    """
    Clase que gestiona el sistema de usuarios y tareas con un enfoque de trabajo basado en parámetros 
    pasados a los métodos, en lugar de usar entradas interactivas.

    Atributos:
        usuarios (dict): Diccionario que almacena los usuarios registrados, con el correo como clave.
        usuarios_tareas (dict): Diccionario que almacena las tareas de cada usuario, con el correo como clave.
        usuario_actual (str | None): Correo del usuario actualmente autenticado. Si no hay usuario autenticado, es None.

    Métodos:
        cambiar_contraseña_usuario(correo, contraseña_actual, nueva_contraseña, confirmar_contraseña): 
            Permite cambiar la contraseña de un usuario dado su correo y las contraseñas proporcionadas.

        iniciar_sesion(correo, contraseña): 
            Permite iniciar sesión con el correo y la contraseña de un usuario.

        editar_tarea(nombre_tarea, nuevo_texto, nueva_categoria, nuevo_estado): 
            Permite editar una tarea de un usuario autenticado.

        eliminar_tarea(nombre_tarea): 
            Permite eliminar una tarea de un usuario autenticado.

        mostrar_tareas_usuario(): 
            Muestra todas las tareas de un usuario autenticado.
    """

    def __init__(self):
        self.usuarios = {}
        self.usuarios_tareas = {}
        self.usuario_actual = None

    def cambiar_contraseña_usuario(self, correo, contraseña_actual, nueva_contraseña, confirmar_contraseña):
        """
        Permite cambiar la contraseña de un usuario, validando la contraseña actual, la nueva contraseña
        y confirmando que ambas coinciden.

        Args:
            correo (str): Correo del usuario cuya contraseña se desea cambiar.
            contraseña_actual (str): Contraseña actual del usuario.
            nueva_contraseña (str): Nueva contraseña que se desea establecer.
            confirmar_contraseña (str): Confirmación de la nueva contraseña.

        Returns:
            str: Mensaje indicando si la contraseña fue actualizada con éxito o si hubo un error.
        """
        intentos = 3

        if correo not in self.usuarios:
            return "Error: Usuario no registrado"
        if not self.usuarios[correo].get("Activo", True):
            return "Error: Usuario inactivo"
        if self.usuarios[correo]["Contraseña"] != contraseña_actual:
            return "Error: Contraseña incorrecta"

        while intentos > 0:
            if nueva_contraseña == confirmar_contraseña:
                if len(nueva_contraseña) > 320:
                    return "Error: Contraseña demasiado larga"
                self.usuarios[correo]["Contraseña"] = nueva_contraseña
                return "Contraseña actualizada con éxito"
            else:
                intentos -= 1
                if intentos == 0:
                    return "Demasiados intentos fallidos, inténtalo más tarde"
        return "Error inesperado"

    def iniciar_sesion(self, correo, contraseña):
        """
        Permite iniciar sesión con el correo y la contraseña de un usuario.

        Args:
            correo (str): Correo del usuario que intenta iniciar sesión.
            contraseña (str): Contraseña del usuario.

        Returns:
            str: Mensaje indicando si el inicio de sesión fue exitoso o si hubo un error.
        """
        if correo not in self.usuarios:
            return "Error: Usuario no registrado"
        if not self.usuarios[correo].get("Activo", True):
            return "Error: Usuario inactivo"
        if contraseña == self.usuarios[correo]["Contraseña"]:
            self.usuario_actual = correo
            return f"Bienvenido {self.usuarios[correo]['Nombre']}"
        return "Error: Credenciales incorrectas"

    def editar_tarea(self, nombre_tarea, nuevo_texto, nueva_categoria, nuevo_estado):
        """
        Permite editar una tarea de un usuario autenticado.

        Args:
            nombre_tarea (str): Nombre de la tarea a editar.
            nuevo_texto (str): Nuevo texto para la tarea.
            nueva_categoria (str): Nueva categoría para la tarea.
            nuevo_estado (str): Nuevo estado para la tarea.

        Returns:
            str: Mensaje indicando si la tarea fue actualizada con éxito o si hubo un error.
        """
        correo = self.usuario_actual
        if correo is None:
            return "No hay usuario logueado."

        tareas = self.usuarios_tareas.get(correo, [])
        for tarea in tareas:
            if tarea["nombre"] == nombre_tarea:
                tarea["texto"] = nuevo_texto if nuevo_texto else tarea["texto"]
                tarea["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                tarea["categoría"] = nueva_categoria if nueva_categoria else tarea["categoría"]
                tarea["estado"] = nuevo_estado if nuevo_estado else tarea["estado"]
                return "Tarea actualizada con éxito."

        return "La tarea no existe."

    def eliminar_tarea(self, nombre_tarea):
        """
        Permite eliminar una tarea de un usuario autenticado.

        Args:
            nombre_tarea (str): Nombre de la tarea a eliminar.

        Returns:
            str: Mensaje indicando si la tarea fue eliminada con éxito o si no se encontró.
        """
        correo = self.usuario_actual
        if correo is None:
            return "No hay usuario logueado."

        tareas = self.usuarios_tareas.get(correo, [])
        for i, tarea in enumerate(tareas):
            if tarea["nombre"] == nombre_tarea:
                del tareas[i]
                return "Tarea eliminada."

        return "Tarea no encontrada."

    def mostrar_tareas_usuario(self):
        """
        Muestra todas las tareas de un usuario autenticado.

        Returns:
            None: Imprime las tareas del usuario en consola o un mensaje de error si no hay tareas.
        """
        correo = self.usuario_actual
        if correo is None:
            return "No hay usuario logueado."

        tareas = self.usuarios_tareas.get(correo, [])
        if not tareas:
            return "No tienes tareas."
        
        return tareas
