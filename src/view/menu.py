from datetime import datetime
from src.controller.sistema import Sistema
from src.model.Usuario import Usuario
from src.model.tarea import Tarea 


class Menu:
    def __init__(self):
        self.sistema = Sistema()

    def menu_principal(self):
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
        Usuario(self.sistema.usuarios)

    def iniciar_sesion(self):
        resultado = self.sistema.iniciar_sesion()
        print(resultado)

    def cambiar_contraseña(self):
        resultado = self.sistema.cambiar_contraseña_usuario()
        print(resultado)

    def crear_tarea(self):
        Tarea(self.sistema.usuarios_tareas, self.sistema.usuario_actual)

    def editar_tarea(self):
        resultado = self.sistema.editar_tarea()
        print(resultado)

    def eliminar_tarea(self):
        resultado = self.sistema.eliminar_tarea()
        print(resultado)

    def mostrar_tareas(self):
        self.sistema.mostrar_tareas_usuario()


if __name__ == "__main__":
    menu = Menu()
    menu.menu_principal()
