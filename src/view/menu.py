from datetime import datetime
from src.controller.sistema import Sistema
from src.model.Usuario import Usuario
from src.model.tarea import Tarea 

class Menu:
    """
    Clase que representa el menú principal de la aplicación.
    Gestiona la interacción del usuario a través de un menú con opciones para gestionar usuarios y tareas.
    """
    def __init__(self):
        """
        Inicializa el sistema que gestiona las operaciones de usuario y tarea.
        """
        self.sistema = Sistema()

    def menu_principal(self):
        """
        Muestra el menú principal de la aplicación.
        Permite al usuario seleccionar una opción para crear usuarios, iniciar sesión,
        cambiar la contraseña, crear, editar, eliminar tareas, o mostrar las tareas.
        """
        while True:
            print("\n--- Menú Principal ---")
            print("1. Crear Usuario")
            print("2. Iniciar Sesión")
            print("3. Cambiar Contraseña")
            print("4. Crear Tarea")
            print("5. Editar Tarea")
            print("6. Eliminar Tarea")
            print("7. Mostrar Tareas")
            print("8. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.crear_usuario()
            elif opcion == "2":
                self.iniciar_sesion()
            elif opcion == "3":
                self.cambiar_contraseña()
            elif opcion == "4":
                self.crear_tarea()
            elif opcion == "5":
                self.editar_tarea()
            elif opcion == "6":
                self.eliminar_tarea()
            elif opcion == "7":
                self.mostrar_tareas()
            elif opcion == "8":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def crear_usuario(self):
        """
        Permite al usuario ingresar los datos necesarios para crear una cuenta.
        Recoge el nombre, apellido, correo y contraseña del usuario e intenta crear un objeto Usuario.
        Si los datos no son válidos, muestra un mensaje de error.
        """
        nombre_usuario = input("Ingrese nombre: ")
        apellido = input("Ingrese apellido: ")
        correo = input("Ingrese correo: ")
        contraseña = input("Ingrese contraseña: ")
        
        try:
            Usuario(nombre_usuario, apellido, correo, contraseña)
        except ValueError as e:
            print(e)

    def iniciar_sesion(self):
        """
        Permite al usuario iniciar sesión proporcionando su correo y contraseña.
        Si la autenticación es exitosa, muestra un mensaje de bienvenida.
        """
        correo = input("Ingrese correo: ")
        contraseña = input("Ingrese contraseña: ")
        resultado = self.sistema.iniciar_sesion(correo, contraseña)
        print(resultado)

    def cambiar_contraseña(self):
        """
        Permite al usuario cambiar su contraseña actual.
        El usuario debe proporcionar su correo, la contraseña actual, la nueva contraseña y confirmar la nueva contraseña.
        Si la operación es exitosa, muestra un mensaje de éxito.
        """
        correo = input("Ingrese correo: ")
        contraseña_actual = input("Ingrese contraseña actual: ")
        nueva_contraseña = input("Ingrese nueva contraseña: ")
        confirmar_contraseña = input("Confirme nueva contraseña: ")
        resultado = self.sistema.cambiar_contraseña_usuario(correo, contraseña_actual, nueva_contraseña, confirmar_contraseña)
        print(resultado)

    def crear_tarea(self):
        """
        Permite al usuario crear una nueva tarea.
        El usuario debe ingresar el nombre, texto, categoría y estado de la tarea.
        Se asocia la tarea al usuario actual mediante el correo.
        """
        correo = self.sistema.usuario_actual_id
        nombre_tarea = input("Ingrese nombre de la tarea: ")
        texto_tarea = input("Ingrese texto de la tarea: ")
        categoria = input("Ingrese categoría de la tarea: ")
        estado = input("Ingrese estado de la tarea: ")
        Tarea(correo, nombre_tarea, texto_tarea, categoria, estado)

    def editar_tarea(self):
        """
        Permite al usuario editar los detalles de una tarea existente.
        El usuario debe ingresar el nombre de la tarea a editar y los nuevos valores de texto, categoría y estado.
        """
        nombre_tarea = input("Ingrese nombre de la tarea a editar: ")
        nuevo_texto = input("Ingrese nuevo texto de la tarea: ")
        nueva_categoria = input("Ingrese nueva categoría de la tarea: ")
        nuevo_estado = input("Ingrese nuevo estado de la tarea: ")
        resultado = self.sistema.editar_tarea(nombre_tarea, nuevo_texto, nueva_categoria, nuevo_estado)
        print(resultado)

    def eliminar_tarea(self):
        """
        Permite al usuario eliminar una tarea existente.
        El usuario debe ingresar el nombre de la tarea a eliminar.
        Si la operación es exitosa, muestra un mensaje confirmando la eliminación.
        """
        nombre_tarea = input("Ingrese nombre de la tarea a eliminar: ")
        resultado = self.sistema.eliminar_tarea(nombre_tarea)
        print(resultado)

    def mostrar_tareas(self):
        """
        Muestra todas las tareas del usuario actual.
        Recupera las tareas del usuario y las imprime con sus detalles (nombre, texto, categoría, estado y fecha).
        """
        tareas = self.sistema.mostrar_tareas_usuario()
        if isinstance(tareas, str):
            print(tareas)
        else:
            for tarea in tareas:
                print(f"Nombre: {tarea[0]}, Texto: {tarea[1]}, Categoría: {tarea[2]}, Estado: {tarea[3]}, Fecha: {tarea[4]}")

if __name__ == "__main__":
    """
    Ejecuta la aplicación mostrando el menú principal.
    Permite al usuario interactuar con el sistema y gestionar usuarios y tareas.
    """
    menu = Menu()
    menu.menu_principal()
