import pytest

# ------------------------------
# Simulación del sistema original
# ------------------------------

class SistemaSimulado:
    def __init__(self):
        """
        Inicializa el sistema simulado con un usuario predefinido.
        """
        self.usuarios = {
            "usuario@example.com": {
                "contraseña": "contraseña_actual",
                "activo": True
            }
        }

    def cambiar_contraseña_usuario(self, correo, contraseña_actual, nueva_contraseña, confirmar_contraseña):
        """
        Cambia la contraseña de un usuario registrado, realizando diversas validaciones.

        Args:
            correo (str): El correo electrónico del usuario.
            contraseña_actual (str): La contraseña actual del usuario.
            nueva_contraseña (str): La nueva contraseña deseada.
            confirmar_contraseña (str): La nueva contraseña confirmada.

        Returns:
            str: El resultado de la operación, ya sea un mensaje de éxito o un error.

        Errores posibles:
            - Error: Debe proporcionar un correo
            - Error: Usuario no registrado
            - Error: Usuario inactivo
            - Error: Contraseña actual incorrecta
            - Error: Contraseña demasiado larga
            - Error: Las contraseñas no coinciden
        """
        if not correo:
            return "Error: Debe proporcionar un correo"

        if correo not in self.usuarios:
            return "Error: Usuario no registrado"

        usuario = self.usuarios[correo]

        if not usuario["activo"]:
            return "Error: Usuario inactivo"

        if contraseña_actual != usuario["contraseña"]:
            return "Error: Contraseña actual incorrecta"

        if len(nueva_contraseña) > 256:
            return "Error: Contraseña demasiado larga"

        if nueva_contraseña != confirmar_contraseña:
            return "Error: Las contraseñas no coinciden"

        usuario["contraseña"] = nueva_contraseña
        return "Contraseña cambiada correctamente"

# ------------------------------
# Casos de prueba
# ------------------------------

@pytest.fixture
def sistema():
    """
    Fixture que crea y devuelve una instancia de SistemaSimulado.
    
    Returns:
        SistemaSimulado: Instancia del sistema simulado para las pruebas.
    """
    return SistemaSimulado()

def test_cambio_exitoso(sistema):
    """
    Prueba que verifica el cambio exitoso de la contraseña del usuario.

    Args:
        sistema (SistemaSimulado): El sistema simulado a probar.

    Asserts:
        Verifica que el mensaje de resultado sea "Contraseña cambiada correctamente".
    """
    resultado = sistema.cambiar_contraseña_usuario("usuario@example.com", "contraseña_actual", "nueva_contraseña", "nueva_contraseña")
    assert resultado == "Contraseña cambiada correctamente"

def test_mayusculas(sistema):
    """
    Prueba que verifica el cambio de contraseña con mayúsculas en la contraseña.

    Args:
        sistema (SistemaSimulado): El sistema simulado a probar.

    Asserts:
        Verifica que el cambio de contraseña sea exitoso incluso con mayúsculas.
    """
    sistema.usuarios["usuario@example.com"]["contraseña"] = "CONTRASEÑA_ACTUAL"
    resultado = sistema.cambiar_contraseña_usuario("usuario@example.com", "CONTRASEÑA_ACTUAL", "NUEVA_CONTRASEÑA", "NUEVA_CONTRASEÑA")
    assert resultado == "Contraseña cambiada correctamente"

def test_39_post_restablecimiento(sistema):
    """
    Prueba de cambio de contraseña después de restablecerla a una contraseña temporal.

    Args:
        sistema (SistemaSimulado): El sistema simulado a probar.

    Asserts:
        Verifica que el cambio de contraseña funcione después de haber restablecido la contraseña.
    """
    sistema.usuarios["usuario@example.com"]["contraseña"] = "temporal123"
    resultado = sistema.cambiar_contraseña_usuario("usuario@example.com", "temporal123", "nueva_segura", "nueva_segura")
    assert resultado == "Contraseña cambiada correctamente"

def test_contraseña_muy_larga(sistema):
    """
    Prueba que verifica que se genera un error si la nueva contraseña es demasiado larga.

    Args:
        sistema (SistemaSimulado): El sistema simulado a probar.

    Asserts:
        Verifica que se muestre un error si la contraseña excede los 256 caracteres.
    """
    contraseña_larga = "x" * 320
    resultado = sistema.cambiar_contraseña_usuario("usuario@example.com", "contraseña_actual", contraseña_larga, contraseña_larga)
    assert resultado == "Error: Contraseña demasiado larga"

def test_cambios_repetidos(sistema):
    """
    Prueba que verifica que se puede cambiar la contraseña varias veces de forma exitosa.

    Args:
        sistema (SistemaSimulado): El sistema simulado a probar.

    Asserts:
        Verifica que los cambios de contraseña repetidos sean exitosos.
    """
    contraseña_actual = "contraseña_actual"
    for i in range(3):
        nueva_contraseña = f"repetida_{i}"
        resultado = sistema.cambiar_contraseña_usuario("usuario@example.com", contraseña_actual, nueva_contraseña, nueva_contraseña)
        assert resultado == "Contraseña cambiada correctamente"
        contraseña_actual = nueva_contraseña

def test_otro_dispositivo(sistema):
    """
    Prueba que verifica que se puede cambiar la contraseña desde otro dispositivo.

    Args:
        sistema (SistemaSimulado): El sistema simulado a probar.

    Asserts:
        Verifica que el cambio de contraseña sea exitoso desde otro dispositivo.
    """
    resultado = sistema.cambiar_contraseña_usuario("usuario@example.com", "contraseña_actual", "desde_otro", "desde_otro")
    assert resultado == "Contraseña cambiada correctamente"

def test_correo_incorrecto(sistema):
    """
    Prueba que verifica que se muestra un error si el correo proporcionado no está registrado.

    Args:
        sistema (SistemaSimulado): El sistema simulado a probar.

    Asserts:
        Verifica que el error "Usuario no registrado" se muestre si el correo es incorrecto.
    """
    resultado = sistema.cambiar_contraseña_usuario("usuario@incorrecto.com", "contraseña_actual", "nueva", "nueva")
    assert resultado == "Error: Usuario no registrado"

def test_correo_vacio(sistema):
    """
    Prueba que verifica que se muestra un error si el correo está vacío.

    Args:
        sistema (SistemaSimulado): El sistema simulado a probar.

    Asserts:
        Verifica que el error "Debe proporcionar un correo" se muestre si el correo está vacío.
    """
    resultado = sistema.cambiar_contraseña_usuario("", "contraseña_actual", "nueva", "nueva")
    assert resultado == "Error: Debe proporcionar un correo"

def test_usuario_inactivo(sistema):
    """
    Prueba que verifica que se muestra un error si el usuario está inactivo.

    Args:
        sistema (SistemaSimulado): El sistema simulado a probar.

    Asserts:
        Verifica que el error "Usuario inactivo" se muestre si el usuario está inactivo.
    """
    sistema.usuarios["usuario@example.com"]["activo"] = False
    resultado = sistema.cambiar_contraseña_usuario("usuario@example.com", "contraseña_actual", "nueva", "nueva")
    assert resultado == "Error: Usuario inactivo"
