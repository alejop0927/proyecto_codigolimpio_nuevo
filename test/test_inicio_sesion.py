import pytest
from src.model.bd_mock.base_datos_mock import Base_datos_mock
from unittest.mock import patch

class Inicio_sesion:
    """
    Clase para gestionar el inicio de sesión de usuarios en la base de datos mock.
    """

    def __init__(self):
        """
        Inicializa la clase Inicio_sesion con la base de datos mock.
        """
        self.db = db_mock

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
        usuario = self.db.usuarios.get(correo)

        if not usuario:
            return "Error: Usuario no registrado"

        if not usuario.get("Activo", True):
            return "Error: Usuario inactivo"

        if contraseña != usuario["Contraseña"]:
            return "Error: Contraseña incorrecta"

        self.db.usuario_actual = correo
        return f"Bienvenido {usuario['Nombre']}"


# Instancia de la base de datos mock
db_mock = Base_datos_mock()

@pytest.fixture(autouse=True)
def limpiar_base_datos():
    """
    Fixture que limpia la base de datos antes de cada prueba.
    """
    db_mock.usuarios.clear()
    db_mock.usuario_actual = None
    db_mock.usuarios["usuario@example.com"] = {
        "Nombre": "Juan",
        "Apellido": "Prueba",
        "Correo": "usuario@example.com",
        "Contraseña": "123456",
        "Activo": True
    }

def test_iniciar_sesion_correctamente():
    """
    Prueba que verifica el inicio de sesión correcto con correo y contraseña válidos.
    """
    with patch('builtins.input', side_effect=["usuario@example.com", "123456"]):
        inicio_sesion = Inicio_sesion()
        resultado = inicio_sesion.iniciar_sesion("usuario@example.com", "123456")
        assert resultado == "Bienvenido Juan"
        assert db_mock.usuario_actual == "usuario@example.com"

def test_iniciar_sesion_mayusculas():
    """
    Prueba que verifica el inicio de sesión con correo en mayúsculas.
    """
    with patch('builtins.input', side_effect=["USUARIO@EXAMPLE.COM", "123456"]):
        inicio_sesion = Inicio_sesion()
        resultado = inicio_sesion.iniciar_sesion("USUARIO@EXAMPLE.COM", "123456")
        assert resultado == "Bienvenido Juan"
        assert db_mock.usuario_actual == "usuario@example.com"

def test_iniciar_sesion_despues_de_cerrar_sesion():
    """
    Prueba que verifica el inicio de sesión después de cerrar sesión previamente.
    """
    db_mock.usuario_actual = None
    with patch('builtins.input', side_effect=["usuario@example.com", "123456"]):
        inicio_sesion = Inicio_sesion()
        resultado = inicio_sesion.iniciar_sesion("usuario@example.com", "123456")
        assert resultado == "Bienvenido Juan"
        assert db_mock.usuario_actual == "usuario@example.com"

def test_iniciar_sesion_contrasena_larga():
    """
    Prueba que verifica el inicio de sesión con una contraseña larga.
    """
    contrasena_larga = "A" * 128
    db_mock.usuarios["usuario@example.com"]["Contraseña"] = contrasena_larga
    with patch('builtins.input', side_effect=["usuario@example.com", contrasena_larga]):
        inicio_sesion = Inicio_sesion()
        resultado = inicio_sesion.iniciar_sesion("usuario@example.com", contrasena_larga)
        assert resultado == "Bienvenido Juan"
        assert db_mock.usuario_actual == "usuario@example.com"

def test_iniciar_sesion_correo_largo():
    """
    Prueba que verifica el inicio de sesión con un correo electrónico largo.
    """
    correo_largo = "a" * 64 + "@" + "b" * 185 + ".com"
    db_mock.usuarios[correo_largo] = {
        "Nombre": "Juan",
        "Apellido": "Prueba",
        "Correo": correo_largo,
        "Contraseña": "123456",
        "Activo": True
    }
    with patch('builtins.input', side_effect=[correo_largo, "123456"]):
        inicio_sesion = Inicio_sesion()
        resultado = inicio_sesion.iniciar_sesion(correo_largo, "123456")
        assert resultado == "Bienvenido Juan"
        assert db_mock.usuario_actual == correo_largo

def test_iniciar_sesion_multiples_intentos():
    """
    Prueba que verifica el inicio de sesión con varios intentos fallidos seguidos.
    """
    with patch('builtins.input', side_effect=["usuario@example.com", "incorrecta", "usuario@example.com", "123456"]):
        inicio_sesion = Inicio_sesion()
        resultado = inicio_sesion.iniciar_sesion("usuario@example.com", "incorrecta")
        assert resultado == "Error: Contraseña incorrecta"
        resultado = inicio_sesion.iniciar_sesion("usuario@example.com", "123456")
        assert resultado == "Bienvenido Juan"
        assert db_mock.usuario_actual == "usuario@example.com"

def test_iniciar_sesion_correo_incorrecto():
    """
    Prueba que verifica el inicio de sesión con un correo incorrecto.
    """
    with patch('builtins.input', side_effect=["usuario@incorrecto.com", "123456"]):
        inicio_sesion = Inicio_sesion()
        resultado = inicio_sesion.iniciar_sesion("usuario@incorrecto.com", "123456")
        assert resultado == "Error: Usuario no registrado"

def test_iniciar_sesion_contrasena_incorrecta():
    """
    Prueba que verifica el inicio de sesión con una contraseña incorrecta.
    """
    with patch('builtins.input', side_effect=["usuario@example.com", "incorrecta"]):
        inicio_sesion = Inicio_sesion()
        resultado = inicio_sesion.iniciar_sesion("usuario@example.com", "incorrecta")
        assert resultado == "Error: Contraseña incorrecta"

def test_iniciar_sesion_usuario_inactivo():
    """
    Prueba que verifica el inicio de sesión con un usuario inactivo.
    """
    db_mock.usuarios["usuario@example.com"]["Activo"] = False
    with patch('builtins.input', side_effect=["usuario@example.com", "123456"]):
        inicio_sesion = Inicio_sesion()
        resultado = inicio_sesion.iniciar_sesion("usuario@example.com", "123456")
        assert resultado == "Error: Usuario inactivo"
