import pytest
from src.model.login import Inicio_sesion
from src.model.db_global import db
from unittest.mock import patch


@pytest.fixture(autouse=True)
def limpiar_base_datos():
    db.usuarios.clear()
    db.usuario_actual = None
    db.usuarios["usuario@example.com"] = {
        "Nombre": "Juan",
        "Apellido": "Prueba",
        "Correo": "usuario@example.com",
        "Contraseña": "123456"
    }


def test_iniciar_sesion_correctamente():
    with patch('builtins.input', side_effect=["usuario@example.com", "123456"]):
        inicio_sesion = Inicio_sesion()
        resultado = inicio_sesion.iniciar_sesion()
        assert resultado == "Bienvenido Juan"
        assert db.usuario_actual == "usuario@example.com"


def test_iniciar_sesion_mayusculas():
    with patch('builtins.input', side_effect=["USUARIO@EXAMPLE.COM", "123456"]):
        inicio_sesion = Inicio_sesion()
        resultado = inicio_sesion.iniciar_sesion()
        assert resultado == "Bienvenido Juan"
        assert db.usuario_actual == "usuario@example.com"


def test_iniciar_sesion_despues_de_cerrar_sesion():
    db.usuario_actual = None
    with patch('builtins.input', side_effect=["usuario@example.com", "123456"]):
        inicio_sesion = Inicio_sesion()
        resultado = inicio_sesion.iniciar_sesion()
        assert resultado == "Bienvenido Juan"
        assert db.usuario_actual == "usuario@example.com"


def test_iniciar_sesion_contrasena_larga():
    contrasena_larga = "A" * 128
    db.usuarios["usuario@example.com"]["Contraseña"] = contrasena_larga
    with patch('builtins.input', side_effect=["usuario@example.com", contrasena_larga]):
        inicio_sesion = Inicio_sesion()
        resultado = inicio_sesion.iniciar_sesion()
        assert resultado == "Bienvenido Juan"
        assert db.usuario_actual == "usuario@example.com"


def test_iniciar_sesion_correo_largo():
    correo_largo = "a" * 64 + "@" + "b" * 185 + ".com"  

    db.usuarios[correo_largo] = {
        "Nombre": "Juan",
        "Apellido": "Prueba",
        "Correo": correo_largo,
        "Contraseña": "123456"
    }
    with patch('builtins.input', side_effect=[correo_largo, "123456"]):
        inicio_sesion = Inicio_sesion()
        resultado = inicio_sesion.iniciar_sesion()
        assert resultado == "Bienvenido Juan"
        assert db.usuario_actual == correo_largo


def test_iniciar_sesion_multiples_intentos():
    with patch('builtins.input', side_effect=["usuario@example.com", "incorrecta", "usuario@example.com", "123456"]):
        inicio_sesion = Inicio_sesion()
        resultado = inicio_sesion.iniciar_sesion()
        assert resultado == "Error: Credenciales incorrectas"
        resultado = inicio_sesion.iniciar_sesion()
        assert resultado == "Bienvenido Juan"
        assert db.usuario_actual == "usuario@example.com"


def test_iniciar_sesion_correo_incorrecto():
    with patch('builtins.input', side_effect=["usuario@incorrecto.com", "123456"]):
        inicio_sesion = Inicio_sesion()
        resultado = inicio_sesion.iniciar_sesion()
        assert resultado == "Error: Usuario no registrado"


def test_iniciar_sesion_contrasena_incorrecta():
    with patch('builtins.input', side_effect=["usuario@example.com", "incorrecta"]):
        inicio_sesion = Inicio_sesion()
        resultado = inicio_sesion.iniciar_sesion()
        assert resultado == "Error: Credenciales incorrectas"


def test_iniciar_sesion_usuario_inactivo():
    db.usuarios["usuario@example.com"]["Activo"] = False
    with patch('builtins.input', side_effect=["usuario@example.com", "123456"]):
        inicio_sesion = Inicio_sesion()
        resultado = inicio_sesion.iniciar_sesion()
        assert resultado == "Error: Usuario inactivo"