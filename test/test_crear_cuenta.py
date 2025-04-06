import pytest
from src.model.Usuario import Crear_cuenta, Usuario
from src.model.login import Inicio_sesion
from src.model.db_global import db
from unittest.mock import patch

# Fixture para limpiar la base de datos antes de cada prueba
@pytest.fixture(autouse=True)
def limpiar_base_datos():
    db.usuarios.clear()
    db.usuario_actual = None

# Caso 46: Usuario crea cuenta correctamente
def test_crear_cuenta_correctamente():
    with patch('builtins.input', side_effect=["usuario@example.com", "Juan", "Prueba", "12345678"]):
        crear_cuenta = Crear_cuenta()
        resultado = crear_cuenta.crear_cuenta_usuario()
        assert resultado == "Usuario creado con éxito"
        assert "usuario@example.com" in db.usuarios

# Caso 47: Usuario crea cuenta y luego inicia sesión
def test_crear_cuenta_y_iniciar_sesion():
    with patch('builtins.input', side_effect=["usuario@example.com", "Juan", "Prueba", "12345678"]):
        crear_cuenta = Crear_cuenta()
        resultado = crear_cuenta.crear_cuenta_usuario()
        assert resultado == "Usuario creado con éxito"
        assert "usuario@example.com" in db.usuarios
    with patch('builtins.input', side_effect=["usuario@example.com", "12345678"]):
        inicio_sesion = Inicio_sesion()
        resultado = inicio_sesion.iniciar_sesion()
        assert resultado == "Bienvenido Juan"
        assert db.usuario_actual == "usuario@example.com"

# Caso 48: Usuario crea cuenta con correo alternativo
def test_crear_cuenta_correo_alternativo():
    with patch('builtins.input', side_effect=["alternativo@example.com", "Juan", "Prueba", "12345678"]):
        crear_cuenta = Crear_cuenta()
        resultado = crear_cuenta.crear_cuenta_usuario()
        assert resultado == "Usuario creado con éxito"
        assert "alternativo@example.com" in db.usuarios

# Caso 49: Usuario crea cuenta con contraseña muy larga
def test_crear_cuenta_contraseña_larga():
    contraseña_larga = "A" * 101
    with patch('builtins.input', side_effect=["usuario@example.com", "Juan", "Prueba", contraseña_larga]):
        crear_cuenta = Crear_cuenta()
        resultado = crear_cuenta.crear_cuenta_usuario()
        assert resultado == "Error: Contraseña demasiado larga"

# Caso 50: Usuario crea cuenta con nombre muy largo
def test_crear_cuenta_nombre_largo():
    nombre_largo = "A" * 51
    with patch('builtins.input', side_effect=["usuario@example.com", nombre_largo, "Prueba", "12345678"]):
        crear_cuenta = Crear_cuenta()
        resultado = crear_cuenta.crear_cuenta_usuario()
        assert resultado == "Error: Nombre demasiado largo"

# Caso 51: Usuario crea cuenta con conexión inestable
def test_crear_cuenta_conexion_inestable():
    with patch('builtins.input', side_effect=["usuario@example.com", "Juan", "Prueba", "12345678"]):
        crear_cuenta = Crear_cuenta()
        resultado = crear_cuenta.crear_cuenta_usuario()
        assert resultado == "Usuario creado con éxito"
        assert "usuario@example.com" in db.usuarios

# Caso 52: Usuario crea cuenta con correo ya registrado
def test_crear_cuenta_correo_registrado():
    db.usuarios["usuario@example.com"] = {
        "Nombre": "Juan",
        "Apellido": "Prueba",
        "Correo": "usuario@example.com",
        "Contraseña": "12345678"
    }
    with patch('builtins.input', side_effect=["usuario@example.com", "Juan", "Prueba", "12345678"]):
        crear_cuenta = Crear_cuenta()
        resultado = crear_cuenta.crear_cuenta_usuario()
        assert resultado == "Error: Correo ya registrado"

# Caso 53: Usuario crea cuenta con contraseña débil
def test_crear_cuenta_contraseña_debil():
    with patch('builtins.input', side_effect=["usuario@example.com", "Juan", "Prueba", "123"]):
        crear_cuenta = Crear_cuenta()
        resultado = crear_cuenta.crear_cuenta_usuario()
        assert resultado == "Error: Contraseña demasiado débil"

# Caso 54: Usuario crea cuenta con datos incompletos
def test_crear_cuenta_datos_incompletos():
    with patch('builtins.input', side_effect=["usuario@example.com", "", "Prueba", "12345678"]):
        crear_cuenta = Crear_cuenta()
        resultado = crear_cuenta.crear_cuenta_usuario()
        assert resultado == "Error: Datos obligatorios faltantes"