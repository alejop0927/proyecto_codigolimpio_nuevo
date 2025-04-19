import pytest
from src.controller.sistema import Sistema
from unittest.mock import patch

# Fixture para limpiar la base de datos antes de cada prueba
@pytest.fixture(autouse=True)
def limpiar_base_datos():
    """
    Fixture para limpiar la base de datos antes de cada prueba.
    Inicializa el sistema y limpia los usuarios y el usuario actual.
    Además, agrega un usuario de prueba activo.
    
    Returns:
        Sistema: Una instancia del sistema con la base de datos limpia.
    """
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

def test_cambiar_contraseña_exito(limpiar_base_datos):
    """
    Verifica que un usuario puede cambiar su contraseña con éxito.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["usuario@example.com", "123456", "nueva_contraseña", "nueva_contraseña"]):
        resultado = sistema.cambiar_contraseña_usuario()
        assert resultado == "Contraseña actualizada con éxito"
        assert sistema.usuarios["usuario@example.com"]["Contraseña"] == "nueva_contraseña"

def test_cambiar_contraseña_mayusculas(limpiar_base_datos):
    """
    Verifica que un usuario puede cambiar su contraseña a una que contenga mayúsculas.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["usuario@example.com", "123456", "NUEVA_CONTRASEÑA", "NUEVA_CONTRASEÑA"]):
        resultado = sistema.cambiar_contraseña_usuario()
        assert resultado == "Contraseña actualizada con éxito"
        assert sistema.usuarios["usuario@example.com"]["Contraseña"] == "NUEVA_CONTRASEÑA"

def test_cambiar_contraseña_despues_de_restablecer(limpiar_base_datos):
    """
    Verifica que un usuario puede cambiar su contraseña después de haberla restablecido.
    """
    sistema = limpiar_base_datos
    sistema.usuarios["usuario@example.com"]["Contraseña"] = "restablecida"
    with patch('builtins.input', side_effect=["usuario@example.com", "restablecida", "nueva_contraseña", "nueva_contraseña"]):
        resultado = sistema.cambiar_contraseña_usuario()
        assert resultado == "Contraseña actualizada con éxito"
        assert sistema.usuarios["usuario@example.com"]["Contraseña"] == "nueva_contraseña"


def test_cambiar_contraseña_clave_larga(limpiar_base_datos):
    """
    Verifica que el sistema rechaza contraseñas demasiado largas.
    """
    sistema = limpiar_base_datos
    contraseña_larga = "A" * 321
    with patch('builtins.input', side_effect=["usuario@example.com", "123456", contraseña_larga, contraseña_larga]):
        resultado = sistema.cambiar_contraseña_usuario()
        assert resultado == "Error: Contraseña demasiado larga"


def test_cambiar_contraseña_varias_veces(limpiar_base_datos):
    """
    Verifica que un usuario puede cambiar su contraseña varias veces seguidas.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["usuario@example.com", "123456", "nueva_contraseña", "nueva_contraseña"]):
        resultado = sistema.cambiar_contraseña_usuario()
        assert resultado == "Contraseña actualizada con éxito"
        assert sistema.usuarios["usuario@example.com"]["Contraseña"] == "nueva_contraseña"
    with patch('builtins.input', side_effect=["usuario@example.com", "nueva_contraseña", "otra_contraseña", "otra_contraseña"]):
        resultado = sistema.cambiar_contraseña_usuario()
        assert resultado == "Contraseña actualizada con éxito"
        assert sistema.usuarios["usuario@example.com"]["Contraseña"] == "otra_contraseña"

def test_cambiar_contraseña_otro_dispositivo(limpiar_base_datos):
    """
    Verifica que un usuario puede cambiar su contraseña desde otro dispositivo.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["usuario@example.com", "123456", "nueva_contraseña", "nueva_contraseña"]):
        resultado = sistema.cambiar_contraseña_usuario()
        assert resultado == "Contraseña actualizada con éxito"
        assert sistema.usuarios["usuario@example.com"]["Contraseña"] == "nueva_contraseña"


def test_cambiar_contraseña_correo_incorrecto(limpiar_base_datos):
    """
    Verifica que el sistema rechaza intentos de cambiar la contraseña con un correo incorrecto.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["usuario@incorrecto.com", "123456", "nueva_contraseña", "nueva_contraseña"]):
        resultado = sistema.cambiar_contraseña_usuario()
        assert resultado == "Error: Usuario no registrado"


def test_cambiar_contraseña_sin_correo(limpiar_base_datos):
    """
    Verifica que el sistema rechaza intentos de cambiar la contraseña sin proporcionar un correo.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["", "123456", "nueva_contraseña", "nueva_contraseña"]):
        resultado = sistema.cambiar_contraseña_usuario()
        assert resultado == "Error: Usuario no registrado"


def test_cambiar_contraseña_usuario_inactivo(limpiar_base_datos):
    """
    Verifica que el sistema rechaza intentos de cambiar la contraseña de un usuario inactivo.
    """
    sistema = limpiar_base_datos
    sistema.usuarios["usuario@example.com"]["Activo"] = False
    with patch('builtins.input', side_effect=["usuario@example.com", "123456", "nueva_contraseña", "nueva_contraseña"]):
        resultado = sistema.cambiar_contraseña_usuario()
        assert resultado == "Error: Usuario inactivo"
