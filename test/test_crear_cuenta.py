import pytest

@pytest.fixture
def usuarios_simulados():
    """
    Fixture que devuelve una lista vacía para simular una base de datos de usuarios.
    """
    return []

def crear_usuario(usuarios, id_usuario, nombre, apellido, email, contrasena):
    """
    Crea un nuevo usuario con la validación de datos de entrada.
    
    Verifica que los datos proporcionados sean válidos:
    - Datos obligatorios no deben estar vacíos
    - El nombre no debe exceder los 50 caracteres
    - La contraseña no debe exceder los 100 caracteres
    - El correo no debe estar ya registrado
    - La contraseña no debe contener "123" (considerada débil)

    Args:
        usuarios (list): La lista de usuarios existentes.
        id_usuario (int): El identificador único para el nuevo usuario.
        nombre (str): El nombre del usuario.
        apellido (str): El apellido del usuario.
        email (str): El correo electrónico del usuario.
        contrasena (str): La contraseña del usuario.

    Raises:
        ValueError: Si alguno de los datos no es válido.

    Returns:
        dict: Un diccionario con la información del usuario creado.
    """
    if not nombre or not apellido or not email or not contrasena:
        raise ValueError("Error: Datos obligatorios faltantes")
    
    if len(nombre) > 50:
        raise ValueError("Error: Nombre demasiado largo")
    if len(contrasena) > 100:
        raise ValueError("Error: Contraseña demasiado larga")
    
    if any(u["email"] == email for u in usuarios):
        raise ValueError("Error: Correo ya registrado")
    
    if "123" in contrasena.lower():
        raise ValueError("Error: Contraseña demasiado débil")

    usuario = {
        "id": id_usuario,
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "contrasena": contrasena
    }
    usuarios.append(usuario)
    return usuario

# ------------------------------
# Casos de prueba
# ------------------------------

def test_crear_usuario_datos_validos(usuarios_simulados):
    """
    Prueba que verifica la creación de un usuario con datos válidos.
    """
    usuario = crear_usuario(usuarios_simulados, 1, "Carlos", "Pérez", "carlos1@example.com", "ClaveSegura456")
    assert usuario in usuarios_simulados

def test_crear_usuario_y_login(usuarios_simulados):
    """
    Prueba que verifica la creación de un usuario y su posterior login (búsqueda por correo y contraseña).
    """
    crear_usuario(usuarios_simulados, 2, "Luisa", "Ramírez", "luisa2@example.com", "ContrasenaSegura789")
    login = next((u for u in usuarios_simulados if u["email"] == "luisa2@example.com" and u["contrasena"] == "ContrasenaSegura789"), None)
    assert login is not None

def test_crear_usuario_correo_alternativo(usuarios_simulados):
    """
    Prueba que verifica la creación de un usuario con un correo alternativo.
    """
    usuario = crear_usuario(usuarios_simulados, 3, "Ana", "Torres", "ana3.alterna@example.com", "AlternaClaveFuerte")
    assert usuario["email"] == "ana3.alterna@example.com"

def test_crear_usuario_contrasena_larga(usuarios_simulados):
    """
    Prueba que verifica que se genere un error si la contraseña es demasiado larga (> 100 caracteres).
    """
    contrasena = "A" * 101
    with pytest.raises(ValueError) as err:
        crear_usuario(usuarios_simulados, 4, "Largo", "Pass", "largo@example.com", contrasena)
    assert str(err.value) == "Error: Contraseña demasiado larga"

def test_crear_usuario_nombre_largo(usuarios_simulados):
    """
    Prueba que verifica que se genere un error si el nombre del usuario excede los 50 caracteres.
    """
    nombre = "A" * 51
    with pytest.raises(ValueError) as err:
        crear_usuario(usuarios_simulados, 5, nombre, "Apellido", "nombrelargo@example.com", "ClaveSegura")
    assert str(err.value) == "Error: Nombre demasiado largo"

def test_crear_usuario_conexion_inestable(usuarios_simulados):
    """
    Prueba que verifica que se genere un error si los datos requeridos no están completos (simulación de una conexión inestable).
    """
    with pytest.raises(ValueError) as err:
        crear_usuario(usuarios_simulados, 6, "", "Apellido", "ejemplo@correo.com", "clave")
    assert str(err.value) == "Error: Datos obligatorios faltantes"

def test_crear_usuario_correo_ya_registrado(usuarios_simulados):
    """
    Prueba que verifica que se genere un error si el correo ya está registrado en la base de datos.
    """
    crear_usuario(usuarios_simulados, 7, "Pedro", "Soto", "pedro@example.com", "Clave456")
    with pytest.raises(ValueError) as err:
        crear_usuario(usuarios_simulados, 8, "Pedro2", "Soto", "pedro@example.com", "Clave789")
    assert str(err.value) == "Error: Correo ya registrado"

def test_crear_usuario_contrasena_debil(usuarios_simulados):
    """
    Prueba que verifica que se genere un error si la contraseña es demasiado débil (contiene "123").
    """
    with pytest.raises(ValueError) as err:
        crear_usuario(usuarios_simulados, 9, "Mario", "Lopez", "mario@example.com", "abc123")
    assert str(err.value) == "Error: Contraseña demasiado débil"

def test_crear_usuario_datos_incompletos(usuarios_simulados):
    """
    Prueba que verifica que se genere un error si algún dato obligatorio está ausente al crear el usuario.
    """
    with pytest.raises(ValueError) as err1:
        crear_usuario(usuarios_simulados, 10, "", "Apellido", "email1@example.com", "Clave123")
    with pytest.raises(ValueError) as err2:
        crear_usuario(usuarios_simulados, 11, "Nombre", "", "email2@example.com", "Clave123")
    with pytest.raises(ValueError) as err3:
        crear_usuario(usuarios_simulados, 12, "Nombre", "Apellido", "", "Clave123")
    with pytest.raises(ValueError) as err4:
        crear_usuario(usuarios_simulados, 13, "Nombre", "Apellido", "email3@example.com", "")
    
    for err in [err1, err2, err3, err4]:
        assert str(err.value) == "Error: Datos obligatorios faltantes"
