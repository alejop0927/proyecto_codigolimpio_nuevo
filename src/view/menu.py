from datetime import datetime
from src.controller.sistema import Sistema
from src.model.Usuario import Usuario
from src.model.tarea import Tarea 

class Menu:
    """
    Clase que representa el menú principal de la aplicación.

    Esta clase ofrece una interfaz de texto para que el usuario interactúe con el sistema, 
    permitiendo realizar varias acciones, como crear un usuario, iniciar sesión, cambiar la contraseña, 
    gestionar tareas (crear, editar, eliminar, mostrar) y salir de la aplicación.

    Atributos:
        sistema (Sistema): Instancia del sistema que gestiona usuarios y tareas.

    Métodos:
        __init__: Inicializa el sistema y crea una instancia de la clase Menu.
        menu_principal: Muestra el menú principal y gestiona la interacción del usuario, 
                        permitiendo elegir entre las opciones disponibles.
        crear_usuario: Permite crear un nuevo usuario en el sistema.
        iniciar_sesion: Permite al usuario iniciar sesión en el sistema.
        cambiar_contraseña: Permite al usuario cambiar su contraseña.
        crear_tarea: Permite crear una nueva tarea asociada al usuario actual.
        editar_tarea: Permite editar una tarea existente.
        eliminar_tarea: Permite eliminar una tarea existente.
        mostrar_tareas: Muestra todas las tareas asociadas al usuario actual.
    """

    def __init__(self):
        """
        Inicializa la instancia de la clase Menu con un sistema vacío.
        Crea una instancia de la clase Sistema que gestiona la lógica de usuarios y tareas.
        """
        self.sistema = Sistema()

    def menu_principal(self):
        """
        Muestra el menú principal de la aplicación y gestiona la interacción del usuario.

        Ofrece un conjunto de opciones que permiten al usuario:
        - Crear un usuario
        - Iniciar sesión
        - Cambiar contraseña
        - Crear tareas
        - Editar tareas
        - Eliminar tareas
        - Mostrar tareas
        - Salir del sistema

        El ciclo continúa hasta que el usuario elige la opción de salir.
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
        Crea un nuevo usuario en el sistema.

        Llama a la clase Usuario para crear un nuevo usuario y agregarlo al sistema.
        """
        Usuario(self.sistema.usuarios)

    def iniciar_sesion(self):
        """
        Permite al usuario iniciar sesión.

        Llama al método de iniciar sesión del sistema y muestra el resultado al usuario.
        """
        resultado = self.sistema.iniciar_sesion()
        print(resultado)

    def cambiar_contraseña(self):
        """
        Permite al usuario cambiar su contraseña.

        Llama al método de cambio de contraseña del sistema y muestra el resultado al usuario.
        """
        resultado = self.sistema.cambiar_contraseña_usuario()
        print(resultado)

    def crear_tarea(self):
        """
        Crea una nueva tarea para el usuario actual.

        Llama a la clase Tarea para crear una tarea y agregarla a las tareas del usuario.
        """
        Tarea(self.sistema.usuarios_tareas, self.sistema.usuario_actual)

    def editar_tarea(self):
        """
        Permite al usuario editar una tarea existente.

        Llama al método de edición de tareas del sistema y muestra el resultado al usuario.
        """
        resultado = self.sistema.editar_tarea()
        print(resultado)

    def eliminar_tarea(self):
        """
        Permite al usuario eliminar una tarea existente.

        Llama al método de eliminación de tareas del sistema y muestra el resultado al usuario.
        """
        resultado = self.sistema.eliminar_tarea()
        print(resultado)

    def mostrar_tareas(self):
        """
        Muestra todas las tareas asociadas al usuario actual.

        Llama al método de mostrar tareas del sistema y las muestra en la consola.
        """
        self.sistema.mostrar_tareas_usuario()


if __name__ == "__main__":
    """
    Ejecuta el menú principal de la aplicación.

    Crea una instancia de la clase Menu y ejecuta el método menu_principal 
    para permitir la interacción del usuario con el sistema.
    """
    menu = Menu()
    menu.menu_principal()
