import pytest
from src.controller.sistema import Sistema
from src.model.conexion import obtener_conexion_bd
from unittest.mock import patch

# Fixture para limpiar la base de datos antes de cada prueba
@pytest.fixture(autouse=True)
def limpiar_base_datos():
    """
    Fixture que limpia la base de datos antes de cada prueba. 
    Elimina todas las tareas, relaciones de tareas y usuarios, 
    y luego inserta un usuario de prueba en la base de datos.
    """
    sistema = Sistema()
    sistema.conn = obtener_conexion_bd()
    sistema.cursor = sistema.conn.cursor()
    
    # Eliminar todas las relaciones de tareas y usuarios
    sistema.cursor.execute("DELETE FROM Tarea_usuario")
    # Eliminar todas las tareas
    sistema.cursor.execute("DELETE FROM Tarea")
    # Eliminar todos los usuarios
    sistema.cursor.execute("DELETE FROM Usuario")
    
    # Insertar usuario de prueba
    sistema.cursor.execute("""
        INSERT INTO Usuario (nombre_usuario, apellido, correo, contraseña, activo)
        VALUES ('Juan', 'Prueba', 'usuario@example.com', '123456', TRUE)
    """)
    sistema.conn.commit()
    
    sistema.usuario_actual_id = None
    sistema.nombre_usuario = None
    return sistema

def test_iniciar_sesion_correctamente(limpiar_base_datos):
    """
    Prueba que verifica el inicio de sesión correcto con correo y contraseña válidos.
    Se asegura de que el usuario sea bienvenido, el ID del usuario esté asignado y 
    el nombre del usuario sea correcto.
    """
    sistema = limpiar_base_datos
    resultado = sistema.iniciar_sesion("usuario@example.com", "123456")
    assert resultado == "Bienvenido Juan"
    assert sistema.usuario_actual_id is not None
    assert sistema.nombre_usuario == "Juan"

def test_iniciar_sesion_mayusculas(limpiar_base_datos):
    """
    Prueba que verifica el inicio de sesión con correo en mayúsculas. 
    El sistema debe aceptar correos en cualquier combinación de mayúsculas y minúsculas.
    """
    sistema = limpiar_base_datos
    resultado = sistema.iniciar_sesion("USUARIO@EXAMPLE.COM", "123456")
    assert resultado == "Bienvenido Juan"
    assert sistema.usuario_actual_id is not None
    assert sistema.nombre_usuario == "Juan"

def test_iniciar_sesion_despues_de_cerrar_sesion(limpiar_base_datos):
    """
    Prueba que verifica el inicio de sesión después de cerrar sesión previamente.
    Se asegura de que el sistema permita iniciar sesión correctamente después de cerrar sesión.
    """
    sistema = limpiar_base_datos
    sistema.usuario_actual_id = None
    resultado = sistema.iniciar_sesion("usuario@example.com", "123456")
    assert resultado == "Bienvenido Juan"
    assert sistema.usuario_actual_id is not None
    assert sistema.nombre_usuario == "Juan"

def test_iniciar_sesion_contrasena_larga(limpiar_base_datos):
    """
    Prueba que verifica el inicio de sesión con una contraseña larga.
    Se asegura de que el sistema maneje contraseñas largas sin errores.
    """
    sistema = limpiar_base_datos
    contrasena_larga = "A" * 128
    sistema.cursor.execute("UPDATE Usuario SET contraseña = %s WHERE correo = %s", (contrasena_larga, "usuario@example.com"))
    sistema.conn.commit()
    resultado = sistema.iniciar_sesion("usuario@example.com", contrasena_larga)
    assert resultado == "Bienvenido Juan"
    assert sistema.usuario_actual_id is not None
    assert sistema.nombre_usuario == "Juan"

def test_iniciar_sesion_correo_largo(limpiar_base_datos):
    """
    Prueba que verifica el inicio de sesión con un correo electrónico largo.
    Se asegura de que el sistema maneje correos electrónicos largos sin errores.
    """
    sistema = limpiar_base_datos
    correo_largo = "a" * 64 + "@" + "b" * 185 + ".com"
    sistema.cursor.execute("""
        INSERT INTO Usuario (nombre_usuario, apellido, correo, contraseña, activo)
        VALUES ('Juan', 'Prueba', %s, '123456', TRUE)
    """, (correo_largo,))
    sistema.conn.commit()
    resultado = sistema.iniciar_sesion(correo_largo, "123456")
    assert resultado == "Bienvenido Juan"
    assert sistema.usuario_actual_id is not None
    assert sistema.nombre_usuario == "Juan"

def test_iniciar_sesion_multiples_intentos(limpiar_base_datos):
    """
    Prueba que verifica el inicio de sesión con varios intentos fallidos seguidos.
    Se asegura de que el sistema proporcione un mensaje de error adecuado para los intentos incorrectos.
    """
    sistema = limpiar_base_datos
    resultado = sistema.iniciar_sesion("usuario@example.com", "incorrecta")
    assert resultado == "Error: Contraseña incorrecta"
    resultado = sistema.iniciar_sesion("usuario@example.com", "123456")
    assert resultado == "Bienvenido Juan"
    assert sistema.usuario_actual_id is not None
    assert sistema.nombre_usuario == "Juan"

def test_iniciar_sesion_correo_incorrecto(limpiar_base_datos):
    """
    Prueba que verifica el inicio de sesión con un correo incorrecto.
    Se asegura de que el sistema devuelva un mensaje de error cuando el correo no está registrado.
    """
    sistema = limpiar_base_datos
    resultado = sistema.iniciar_sesion("usuario@incorrecto.com", "123456")
    assert resultado == "Error: Usuario no registrado"

def test_iniciar_sesion_contrasena_incorrecta(limpiar_base_datos):
    """
    Prueba que verifica el inicio de sesión con una contraseña incorrecta.
    Se asegura de que el sistema devuelva un mensaje de error cuando la contraseña es incorrecta.
    """
    sistema = limpiar_base_datos
    resultado = sistema.iniciar_sesion("usuario@example.com", "incorrecta")
    assert resultado == "Error: Contraseña incorrecta"

def test_iniciar_sesion_usuario_inactivo(limpiar_base_datos):
    """
    Prueba que verifica el inicio de sesión con un usuario inactivo.
    Se asegura de que el sistema devuelva un mensaje de error cuando el usuario está marcado como inactivo.
    """
    sistema = limpiar_base_datos
    sistema.cursor.execute("UPDATE Usuario SET activo = FALSE WHERE correo = %s", ("usuario@example.com",))
    sistema.conn.commit()
    resultado = sistema.iniciar_sesion("usuario@example.com", "123456")
    assert resultado == "Error: Usuario inactivo"
