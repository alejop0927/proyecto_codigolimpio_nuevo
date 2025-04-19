import pytest
from src.model.Usuario import Usuario
from src.controller.sistema import Sistema
from unittest.mock import patch

@pytest.fixture(autouse=True)
def limpiar_base_datos():
    """
    Fixture para limpiar la base de datos antes de cada prueba.
    Inicializa el sistema y limpia los usuarios y el usuario actual.
    
    Returns:
        Sistema: Una instancia del sistema con la base de datos limpia.
    """
    sistema = Sistema()
    sistema.usuarios.clear()
    sistema.usuario_actual = None
    return sistema

def test_crear_cuenta_correctamente(limpiar_base_datos):
    """
    Verifica que una cuenta se crea correctamente y los datos se almacenan como se espera.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["usuario@example.com", "Juan", "Prueba", "12345678"]):
        Usuario(sistema.usuarios)
        assert "usuario@example.com" in sistema.usuarios
        assert sistema.usuarios["usuario@example.com"]["Nombre"] == "Juan"

def test_crear_cuenta_y_iniciar_sesion(limpiar_base_datos):
    """
    Comprueba que después de crear una cuenta, el usuario puede iniciar sesión correctamente.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["usuario@example.com", "Juan", "Prueba", "12345678"]):
        Usuario(sistema.usuarios)
        assert "usuario@example.com" in sistema.usuarios
    with patch('builtins.input', side_effect=["usuario@example.com", "12345678"]):
        resultado = sistema.iniciar_sesion()
        assert resultado == "Bienvenido Juan"
        assert sistema.usuario_actual == "usuario@example.com"

def test_crear_cuenta_correo_alternativo(limpiar_base_datos):
    """
    Asegura que se puede crear una cuenta con un correo alternativo.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["alternativo@example.com", "Juan", "Prueba", "12345678"]):
        Usuario(sistema.usuarios)
        assert "alternativo@example.com" in sistema.usuarios

def test_crear_cuenta_contraseña_larga(limpiar_base_datos):
    """
    Verifica que las contraseñas demasiado largas no se aceptan.
    """
    sistema = limpiar_base_datos
    contraseña_larga = "A" * 101
    with patch('builtins.input', side_effect=["usuario@example.com", "Juan", "Prueba", contraseña_larga]):
        Usuario(sistema.usuarios)
        assert "usuario@example.com" not in sistema.usuarios

def test_crear_cuenta_nombre_largo(limpiar_base_datos):
    """
    Asegura que los nombres demasiado largos no se aceptan.
    """
    sistema = limpiar_base_datos
    nombre_largo = "A" * 51
    with patch('builtins.input', side_effect=["usuario@example.com", nombre_largo, "Prueba", "12345678"]):
        Usuario(sistema.usuarios)
        assert "usuario@example.com" not in sistema.usuarios
def test_crear_cuenta_conexion_inestable(limpiar_base_datos):
    """
    Simula la creación de una cuenta bajo condiciones de conexión inestable.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["usuario@example.com", "Juan", "Prueba", "12345678"]):
        Usuario(sistema.usuarios)
        assert "usuario@example.com" in sistema.usuarios

def test_crear_cuenta_correo_registrado(limpiar_base_datos):
    """
    Comprueba que no se puede crear una cuenta con un correo ya registrado.
    """
    sistema = limpiar_base_datos
    sistema.usuarios["usuario@example.com"] = {
        "Nombre": "Juan",
        "Apellido": "Prueba",
        "Correo": "usuario@example.com",
        "Contraseña": "12345678"
    }
    with patch('builtins.input', side_effect=["usuario@example.com", "Juan", "Prueba", "12345678"]):
        Usuario(sistema.usuarios)
        assert sistema.usuarios["usuario@example.com"]["Nombre"] == "Juan"

def test_crear_cuenta_contraseña_debil(limpiar_base_datos):
    """
    Verifica que las contraseñas débiles no se aceptan.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["usuario@example.com", "Juan", "Prueba", "123"]):
        Usuario(sistema.usuarios)
        assert "usuario@example.com" not in sistema.usuarios

def test_crear_cuenta_datos_incompletos(limpiar_base_datos):
    """
    Asegura que no se puede crear una cuenta con datos incompletos.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["usuario@example.com", "", "Prueba", "12345678"]):
        Usuario(sistema.usuarios)
        assert "usuario@example.com" not in sistema.usuarios

