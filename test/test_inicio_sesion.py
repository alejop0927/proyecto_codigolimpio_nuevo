import pytest
from src.controller.sistema import Sistema
from unittest.mock import patch

# Fixture para limpiar la base de datos antes de cada prueba
@pytest.fixture(autouse=True)
def limpiar_base_datos():
    sistema = Sistema()
    sistema.usuarios.clear()
    sistema.usuario_actual = None
    sistema.usuarios["usuario@example.com"] = {
        "Nombre": "Juan",
        "Apellido": "Prueba",
        "Correo": "usuario@example.com",
        "Contraseña": "123456",
        "Activo": True
    }
    return sistema

def test_iniciar_sesion_correctamente(limpiar_base_datos):
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["usuario@example.com", "123456"]):
        resultado = sistema.iniciar_sesion()
        assert resultado == "Bienvenido Juan"
        assert sistema.usuario_actual == "usuario@example.com"

def test_iniciar_sesion_mayusculas(limpiar_base_datos):
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["USUARIO@EXAMPLE.COM", "123456"]):
        resultado = sistema.iniciar_sesion()
        assert resultado == "Bienvenido Juan"
        assert sistema.usuario_actual == "usuario@example.com"

def test_iniciar_sesion_despues_de_cerrar_sesion(limpiar_base_datos):
    sistema = limpiar_base_datos
    sistema.usuario_actual = None
    with patch('builtins.input', side_effect=["usuario@example.com", "123456"]):
        resultado = sistema.iniciar_sesion()
        assert resultado == "Bienvenido Juan"
        assert sistema.usuario_actual == "usuario@example.com"

def test_iniciar_sesion_contrasena_larga(limpiar_base_datos):
    sistema = limpiar_base_datos
    contrasena_larga = "A" * 128
    sistema.usuarios["usuario@example.com"]["Contraseña"] = contrasena_larga
    with patch('builtins.input', side_effect=["usuario@example.com", contrasena_larga]):
        resultado = sistema.iniciar_sesion()
        assert resultado == "Bienvenido Juan"
        assert sistema.usuario_actual == "usuario@example.com"

def test_iniciar_sesion_correo_largo(limpiar_base_datos):
    sistema = limpiar_base_datos
    correo_largo = "a" * 64 + "@" + "b" * 185 + ".com"  
    sistema.usuarios[correo_largo] = {
        "Nombre": "Juan",
        "Apellido": "Prueba",
        "Correo": correo_largo,
        "Contraseña": "123456",
        "Activo": True
    }
    with patch('builtins.input', side_effect=[correo_largo, "123456"]):
        resultado = sistema.iniciar_sesion()
        assert resultado == "Bienvenido Juan"
        assert sistema.usuario_actual == correo_largo

def test_iniciar_sesion_multiples_intentos(limpiar_base_datos):
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["usuario@example.com", "incorrecta", "usuario@example.com", "123456"]):
        resultado = sistema.iniciar_sesion()
        assert resultado == "Error: Credenciales incorrectas"
        resultado = sistema.iniciar_sesion()
        assert resultado == "Bienvenido Juan"
        assert sistema.usuario_actual == "usuario@example.com"

def test_iniciar_sesion_correo_incorrecto(limpiar_base_datos):
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["usuario@incorrecto.com", "123456"]):
        resultado = sistema.iniciar_sesion()
        assert resultado == "Error: Usuario no registrado"

def test_iniciar_sesion_contrasena_incorrecta(limpiar_base_datos):
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["usuario@example.com", "incorrecta"]):
        resultado = sistema.iniciar_sesion()
        assert resultado == "Error: Credenciales incorrectas"

def test_iniciar_sesion_usuario_inactivo(limpiar_base_datos):
    sistema = limpiar_base_datos
    sistema.usuarios["usuario@example.com"]["Activo"] = False
    with patch('builtins.input', side_effect=["usuario@example.com", "123456"]):
        resultado = sistema.iniciar_sesion()
        assert resultado == "Error: Usuario inactivo"
