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

# Caso 37: Usuario cambia la contraseña con éxito
def test_cambiar_contraseña_exito(limpiar_base_datos):
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["usuario@example.com", "123456", "nueva_contraseña", "nueva_contraseña"]):
        resultado = sistema.cambiar_contraseña_usuario()
        assert resultado == "Contraseña actualizada con éxito"
        assert sistema.usuarios["usuario@example.com"]["Contraseña"] == "nueva_contraseña"

# Caso 38: Usuario cambia la contraseña con mayúsculas
def test_cambiar_contraseña_mayusculas(limpiar_base_datos):
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["usuario@example.com", "123456", "NUEVA_CONTRASEÑA", "NUEVA_CONTRASEÑA"]):
        resultado = sistema.cambiar_contraseña_usuario()
        assert resultado == "Contraseña actualizada con éxito"
        assert sistema.usuarios["usuario@example.com"]["Contraseña"] == "NUEVA_CONTRASEÑA"

# Caso 39: Usuario cambia la contraseña después de haberla restablecido
def test_cambiar_contraseña_despues_de_restablecer(limpiar_base_datos):
    sistema = limpiar_base_datos
    sistema.usuarios["usuario@example.com"]["Contraseña"] = "restablecida"
    with patch('builtins.input', side_effect=["usuario@example.com", "restablecida", "nueva_contraseña", "nueva_contraseña"]):
        resultado = sistema.cambiar_contraseña_usuario()
        assert resultado == "Contraseña actualizada con éxito"
        assert sistema.usuarios["usuario@example.com"]["Contraseña"] == "nueva_contraseña"

# Caso 40: Usuario intenta cambiar contraseña con clave muy larga
def test_cambiar_contraseña_clave_larga(limpiar_base_datos):
    sistema = limpiar_base_datos
    contraseña_larga = "A" * 321
    with patch('builtins.input', side_effect=["usuario@example.com", "123456", contraseña_larga, contraseña_larga]):
        resultado = sistema.cambiar_contraseña_usuario()
        assert resultado == "Error: Contraseña demasiado larga"

# Caso 41: Usuario intenta cambiar contraseña varias veces seguidas
def test_cambiar_contraseña_varias_veces(limpiar_base_datos):
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["usuario@example.com", "123456", "nueva_contraseña", "nueva_contraseña"]):
        resultado = sistema.cambiar_contraseña_usuario()
        assert resultado == "Contraseña actualizada con éxito"
        assert sistema.usuarios["usuario@example.com"]["Contraseña"] == "nueva_contraseña"
    with patch('builtins.input', side_effect=["usuario@example.com", "nueva_contraseña", "otra_contraseña", "otra_contraseña"]):
        resultado = sistema.cambiar_contraseña_usuario()
        assert resultado == "Contraseña actualizada con éxito"
        assert sistema.usuarios["usuario@example.com"]["Contraseña"] == "otra_contraseña"

# Caso 42: Usuario cambia la contraseña desde otro dispositivo
def test_cambiar_contraseña_otro_dispositivo(limpiar_base_datos):
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["usuario@example.com", "123456", "nueva_contraseña", "nueva_contraseña"]):
        resultado = sistema.cambiar_contraseña_usuario()
        assert resultado == "Contraseña actualizada con éxito"
        assert sistema.usuarios["usuario@example.com"]["Contraseña"] == "nueva_contraseña"

# Caso 43: Intentar cambiar la contraseña con correo incorrecto
def test_cambiar_contraseña_correo_incorrecto(limpiar_base_datos):
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["usuario@incorrecto.com", "123456", "nueva_contraseña", "nueva_contraseña"]):
        resultado = sistema.cambiar_contraseña_usuario()
        assert resultado == "Error: Usuario no registrado"

# Caso 44: Intentar cambiar la contraseña sin proporcionar correo
def test_cambiar_contraseña_sin_correo(limpiar_base_datos):
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["", "123456", "nueva_contraseña", "nueva_contraseña"]):
        resultado = sistema.cambiar_contraseña_usuario()
        assert resultado == "Error: Usuario no registrado"

# Caso 45: Intentar cambiar la contraseña de un usuario inactivo
def test_cambiar_contraseña_usuario_inactivo(limpiar_base_datos):
    sistema = limpiar_base_datos
    sistema.usuarios["usuario@example.com"]["Activo"] = False
    with patch('builtins.input', side_effect=["usuario@example.com", "123456", "nueva_contraseña", "nueva_contraseña"]):
        resultado = sistema.cambiar_contraseña_usuario()
        assert resultado == "Error: Usuario inactivo"
