import pytest
from src.model.bd_mock.base_datos_mock import Base_datos_mock

db_mock = Base_datos_mock()

def crear_usuario_mock(nombre, apellido, correo, contraseña):
    """
    Simula la creación de un usuario en la base de datos mock.

    Parámetros:
        nombre (str): Nombre del usuario (máx. 50 caracteres).
        apellido (str): Apellido del usuario.
        correo (str): Correo electrónico único del usuario.
        contraseña (str): Contraseña del usuario (8-100 caracteres).

    Retorna:
        str: Mensaje que indica éxito o tipo de error en la creación.
    """
    if correo in db_mock.usuarios:
        return "Error: Correo ya registrado"
    if not nombre or len(nombre) > 50:
        return "Error: Nombre demasiado largo"
    if not apellido:
        return "Error: Apellido faltante"
    if len(contraseña) > 100:
        return "Error: Contraseña demasiado larga"
    if len(contraseña) < 8:
        return "Error: Contraseña demasiado débil"

    db_mock.usuarios[correo] = {
        "Nombre": nombre,
        "Apellido": apellido,
        "Correo": correo,
        "Contraseña": contraseña,
    }
    return "Usuario creado con éxito"

@pytest.fixture(autouse=True)
def limpiar_base_datos():
    """
    Fixture que limpia la base de datos mock antes de cada prueba.
    """
    db_mock.usuarios.clear()
    db_mock.usuario_actual = None

def test_crear_cuenta_correctamente():
    """
    Prueba que verifica la creación exitosa de una cuenta de usuario con datos válidos.
    """
    resultado = crear_usuario_mock("Juan", "Prueba", "usuario@example.com", "12345678")
    assert resultado == "Usuario creado con éxito"
    assert "usuario@example.com" in db_mock.usuarios

def test_crear_cuenta_y_iniciar_sesion():
    """
    Prueba que verifica la creación de una cuenta y el inicio de sesión posterior exitoso.
    """
    # Crear usuario
    resultado = crear_usuario_mock("Juan", "Prueba", "usuario@example.com", "12345678")
    assert resultado == "Usuario creado con éxito"
    assert "usuario@example.com" in db_mock.usuarios

    # Simular inicio de sesión en mock (simple)
    correo = "usuario@example.com"
    contraseña = "12345678"
    if correo in db_mock.usuarios and db_mock.usuarios[correo]["Contraseña"] == contraseña:
        db_mock.usuario_actual = correo
        resultado_login = f"Bienvenido {db_mock.usuarios[correo]['Nombre']}"
    else:
        resultado_login = "Error: Credenciales incorrectas"

    assert resultado_login == "Bienvenido Juan"
    assert db_mock.usuario_actual == "usuario@example.com"

def test_crear_cuenta_correo_alternativo():
    """
    Prueba que verifica la creación de una cuenta con un correo alternativo válido.
    """
    resultado = crear_usuario_mock("Juan", "Prueba", "alternativo@example.com", "12345678")
    assert resultado == "Usuario creado con éxito"
    assert "alternativo@example.com" in db_mock.usuarios

def test_crear_cuenta_contraseña_larga():
    """
    Prueba que verifica que la creación de una cuenta falle si la contraseña excede los 100 caracteres.
    """
    contraseña_larga = "A" * 101
    resultado = crear_usuario_mock("Juan", "Prueba", "usuario3@example.com", contraseña_larga)
    assert resultado == "Error: Contraseña demasiado larga"

def test_crear_cuenta_nombre_largo():
    """
    Prueba que verifica que la creación de una cuenta falle si el nombre excede los 50 caracteres.
    """
    nombre_largo = "A" * 51
    resultado = crear_usuario_mock(nombre_largo, "Prueba", "usuario2@example.com", "12345678")
    assert resultado == "Error: Nombre demasiado largo"

def test_crear_cuenta_conexion_inestable():
    """
    Prueba que simula una conexión estable y verifica creación correcta de usuario.
    En mock no simulamos falla, siempre es exitosa.
    """
    resultado = crear_usuario_mock("Juan", "Prueba", "usuario4@example.com", "12345678")
    assert resultado == "Usuario creado con éxito"
    assert "usuario4@example.com" in db_mock.usuarios

def test_crear_cuenta_correo_registrado():
    """
    Prueba que verifica que la creación de cuenta falle si el correo ya está registrado.
    """
    db_mock.usuarios["usuario@example.com"] = {
        "Nombre": "Juan",
        "Apellido": "Prueba",
        "Correo": "usuario@example.com",
        "Contraseña": "12345678"
    }
    resultado = crear_usuario_mock("Juan", "Prueba", "usuario@example.com", "12345678")
    assert resultado == "Error: Correo ya registrado"

def test_crear_cuenta_contraseña_debil():
    """
    Prueba que verifica que la creación de cuenta falle si la contraseña es demasiado débil (menos de 8 caracteres).
    """
    resultado = crear_usuario_mock("Juan", "Prueba", "usuario5@example.com", "123")
    assert resultado == "Error: Contraseña demasiado débil"

def test_crear_cuenta_datos_incompletos():
    """
    Prueba que verifica que la creación de cuenta falle si faltan datos obligatorios.
    """
    resultado = crear_usuario_mock("Juan", "", "usuario6@example.com", "12345678")
    assert resultado == "Error: Apellido faltante"
