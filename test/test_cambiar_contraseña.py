import pytest
from unittest.mock import patch
from src.model.bd_mock.db_global_mock import db_mock

class Cambiar_contraseña:
    """
    Clase que permite cambiar la contraseña de un usuario mediante inputs simulados.

    Método:
        cambiar_contraseña_usuario(): Solicita datos por input y realiza validaciones para cambiar la contraseña.
    """

    def cambiar_contraseña_usuario(self):
        correo = input("Correo: ").lower()
        contraseña_actual = input("Contraseña actual: ")
        nueva_contraseña = input("Nueva contraseña: ")
        confirmar_contraseña = input("Confirmar contraseña: ")

        if correo not in db_mock.usuarios:
            return "Error: Usuario no registrado"

        usuario = db_mock.usuarios[correo]

        if not usuario.get("Activo", True):
            return "Error: Usuario inactivo"

        if contraseña_actual != usuario["Contraseña"]:
            return "Error: Contraseña actual incorrecta"

        if len(nueva_contraseña) > 320:
            return "Error: Contraseña demasiado larga"

        if nueva_contraseña != confirmar_contraseña:
            return "Error: Las contraseñas no coinciden"

        usuario["Contraseña"] = nueva_contraseña
        return "Contraseña actualizada con éxito"

@pytest.fixture(autouse=True)
def limpiar_base_datos():
    """
    Fixture que limpia y prepara la base de datos simulada antes de cada prueba.
    Resetea la lista de usuarios y agrega un usuario de prueba activo.
    """
    db_mock.usuarios.clear()
    db_mock.usuarios["usuario@example.com"] = {
        "Nombre": "Juan",
        "Apellido": "Prueba",
        "Correo": "usuario@example.com",
        "Contraseña": "123456",
        "Activo": True
    }

def test_cambiar_contraseña_exito():
    """
    Caso 37: Usuario cambia la contraseña con éxito.
    Verifica que la contraseña se actualice correctamente con datos válidos.
    """
    with patch('builtins.input', side_effect=["usuario@example.com", "123456", "nueva_contraseña", "nueva_contraseña"]):
        cambiar = Cambiar_contraseña()
        resultado = cambiar.cambiar_contraseña_usuario()
        assert resultado == "Contraseña actualizada con éxito"
        assert db_mock.usuarios["usuario@example.com"]["Contraseña"] == "nueva_contraseña"

def test_cambiar_contraseña_mayusculas():
    """
    Caso 38: Usuario cambia la contraseña con mayúsculas.
    Asegura que se acepten contraseñas con letras mayúsculas.
    """
    with patch('builtins.input', side_effect=["usuario@example.com", "123456", "NUEVA_CONTRASEÑA", "NUEVA_CONTRASEÑA"]):
        cambiar = Cambiar_contraseña()
        resultado = cambiar.cambiar_contraseña_usuario()
        assert resultado == "Contraseña actualizada con éxito"
        assert db_mock.usuarios["usuario@example.com"]["Contraseña"] == "NUEVA_CONTRASEÑA"

def test_cambiar_contraseña_despues_de_restablecer():
    """
    Caso 39: Usuario cambia la contraseña después de haberla restablecido.
    Cambia la contraseña temporal a una nueva y verifica el éxito.
    """
    db_mock.usuarios["usuario@example.com"]["Contraseña"] = "restablecida"
    with patch('builtins.input', side_effect=["usuario@example.com", "restablecida", "nueva_contraseña", "nueva_contraseña"]):
        cambiar = Cambiar_contraseña()
        resultado = cambiar.cambiar_contraseña_usuario()
        assert resultado == "Contraseña actualizada con éxito"
        assert db_mock.usuarios["usuario@example.com"]["Contraseña"] == "nueva_contraseña"

def test_cambiar_contraseña_clave_larga():
    """
    Caso 40: Usuario intenta cambiar contraseña con clave muy larga.
    Verifica que se genera un error cuando la nueva contraseña excede 320 caracteres.
    """
    contraseña_larga = "A" * 321
    with patch('builtins.input', side_effect=["usuario@example.com", "123456", contraseña_larga, contraseña_larga]):
        cambiar = Cambiar_contraseña()
        resultado = cambiar.cambiar_contraseña_usuario()
        assert resultado == "Error: Contraseña demasiado larga"

def test_cambiar_contraseña_varias_veces():
    """
    Caso 41: Usuario intenta cambiar contraseña varias veces seguidas.
    Cambia la contraseña dos veces consecutivas con éxito.
    """
    with patch('builtins.input', side_effect=["usuario@example.com", "123456", "nueva_contraseña", "nueva_contraseña"]):
        cambiar = Cambiar_contraseña()
        resultado = cambiar.cambiar_contraseña_usuario()
        assert resultado == "Contraseña actualizada con éxito"
        assert db_mock.usuarios["usuario@example.com"]["Contraseña"] == "nueva_contraseña"

    with patch('builtins.input', side_effect=["usuario@example.com", "nueva_contraseña", "otra_contraseña", "otra_contraseña"]):
        resultado = cambiar.cambiar_contraseña_usuario()
        assert resultado == "Contraseña actualizada con éxito"
        assert db_mock.usuarios["usuario@example.com"]["Contraseña"] == "otra_contraseña"

def test_cambiar_contraseña_otro_dispositivo():
    """
    Caso 42: Usuario cambia la contraseña desde otro dispositivo.
    Simula cambio exitoso desde un dispositivo diferente.
    """
    with patch('builtins.input', side_effect=["usuario@example.com", "123456", "nueva_contraseña", "nueva_contraseña"]):
        cambiar = Cambiar_contraseña()
        resultado = cambiar.cambiar_contraseña_usuario()
        assert resultado == "Contraseña actualizada con éxito"
        assert db_mock.usuarios["usuario@example.com"]["Contraseña"] == "nueva_contraseña"

def test_cambiar_contraseña_correo_incorrecto():
    """
    Caso 43: Intentar cambiar la contraseña con correo incorrecto.
    Verifica que se muestre error si el correo no está registrado.
    """
    with patch('builtins.input', side_effect=["usuario@incorrecto.com", "123456", "nueva_contraseña", "nueva_contraseña"]):
        cambiar = Cambiar_contraseña()
        resultado = cambiar.cambiar_contraseña_usuario()
        assert resultado == "Error: Usuario no registrado"

def test_cambiar_contraseña_sin_correo():
    """
    Caso 44: Intentar cambiar la contraseña sin proporcionar correo.
    Verifica que se muestre error si el correo está vacío.
    """
    with patch('builtins.input', side_effect=["", "123456", "nueva_contraseña", "nueva_contraseña"]):
        cambiar = Cambiar_contraseña()
        resultado = cambiar.cambiar_contraseña_usuario()
        assert resultado == "Error: Usuario no registrado"

def test_cambiar_contraseña_usuario_inactivo():
    """
    Caso 45: Intentar cambiar la contraseña de un usuario inactivo.
    Cambia el estado a inactivo y verifica que el cambio sea rechazado.
    """
    db_mock.usuarios["usuario@example.com"]["Activo"] = False
    with patch('builtins.input', side_effect=["usuario@example.com", "123456", "nueva_contraseña", "nueva_contraseña"]):
        cambiar = Cambiar_contraseña()
        resultado = cambiar.cambiar_contraseña_usuario()
        assert resultado == "Error: Usuario inactivo"