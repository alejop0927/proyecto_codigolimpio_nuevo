from model.Usuario import Crear_cuenta, Cambiar_contraseña
from model.login import Inicio_sesion
from model.tarea import Crear, Editar, Eliminar, Mostrar
from model.db_global import db  
from datetime import datetime



def menu_principal():
    crear = Crear("", "", "", "", "")
    editar = Editar()
    eliminar = Eliminar()
    mostrar = Mostrar()
    sesion = Inicio_sesion()
    cuenta = Crear_cuenta("", "", "", "")
    cambiar_pass = Cambiar_contraseña()

    while True:
        print("\n------ MENÚ PRINCIPAL ------")
        print("1. Crear cuenta")
        print("2. Iniciar sesión")
        print("3. Cambiar contraseña")
        print("4. Crear tarea")
        print("5. Editar tarea")
        print("6. Eliminar tarea")
        print("7. Mostrar tareas")
        print("8. Cerrar sesión")
        print("9. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            cuenta.crear_cuenta_usuario()
        elif opcion == "2":
            sesion.iniciar_sesion()
        elif opcion == "3":
            cambiar_pass.cambiar_contraseña_usuario()
        elif opcion == "4":
            crear.crear_tareas()
        elif opcion == "5":
            editar.editar_tarea()
        elif opcion == "6":
            eliminar.eliminar_tarea()
        elif opcion == "7":
            mostrar.mostrar_tareas_usuario()
        elif opcion == "8":
            db.usuario_actual = None
            print("Sesión cerrada con éxito.")
        elif opcion == "9":
            print("Gracias por usar el sistema.")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    menu_principal()
