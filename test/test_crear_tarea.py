import pytest
from src.controller.sistema import Sistema
from src.model.tarea import Tarea
from unittest.mock import patch

@pytest.fixture(autouse=True)
def limpiar_base_datos():
    """
    Fixture para limpiar y configurar la base de datos de usuarios antes de cada prueba.

    Este fixture inicializa un sistema de usuarios, limpia las listas de tareas
    y establece un usuario predeterminado para las pruebas. Los datos del usuario
    se configuran con un nombre, apellido, correo y contraseña.

    Returns:
        sistema (Sistema): Una instancia del sistema con los usuarios inicializados.
    """
    sistema = Sistema()
    sistema.usuarios.clear()
    sistema.usuarios_tareas.clear()
    sistema.usuario_actual = "usuario1"
    sistema.usuarios["usuario1"] = {
        "Nombre": "Juan",
        "Apellido": "Prueba",
        "Correo": "usuario1",
        "Contraseña": "123"
    }
    return sistema

def test_crear_tareas_valida_con_categoria(limpiar_base_datos):
    """
    Test para verificar que una tarea se crea correctamente con una categoría válida.

    Verifica que al crear una tarea con un nombre y categoría válida, la tarea
    sea añadida a la lista de tareas del usuario actual y que el nombre de la tarea
    coincida con el esperado.

    Args:
        limpiar_base_datos (fixture): Fixture que inicializa el sistema y limpia la base de datos.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Comprar leche", "Comprar leche", "Compras", "Por hacer"]):
        Tarea(sistema.usuarios_tareas, sistema.usuario_actual)
        assert len(sistema.usuarios_tareas["usuario1"]) == 1
        assert sistema.usuarios_tareas["usuario1"][0]["nombre"] == "Comprar leche"

def test_crear_tareas_con_estado_por_hacer(limpiar_base_datos):
    """
    Test para verificar que una tarea se crea con el estado "Por hacer".

    Verifica que al crear una tarea con el estado "Por hacer", la tarea se
    añade correctamente con el estado esperado.

    Args:
        limpiar_base_datos (fixture): Fixture que inicializa el sistema y limpia la base de datos.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Ir al gimnasio", "Ir al gimnasio", "Salud", "Por hacer"]):
        Tarea(sistema.usuarios_tareas, sistema.usuario_actual)
        assert len(sistema.usuarios_tareas["usuario1"]) == 1
        assert sistema.usuarios_tareas["usuario1"][0]["estado"] == "Por hacer"

def test_crear_tareas_usuario_registrado(limpiar_base_datos):
    """
    Test para verificar que una tarea se crea correctamente para un usuario registrado.

    Verifica que un usuario registrado pueda crear tareas y que la tarea se
    añada correctamente a la lista de tareas del usuario.

    Args:
        limpiar_base_datos (fixture): Fixture que inicializa el sistema y limpia la base de datos.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Leer libro", "Leer libro", "Lectura", "Por hacer"]):
        Tarea(sistema.usuarios_tareas, sistema.usuario_actual)
        assert len(sistema.usuarios_tareas["usuario1"]) == 1

def test_crear_tareas_texto_largo(limpiar_base_datos):
    """
    Test para verificar que una tarea con un texto largo se crea correctamente.

    Verifica que el texto de la tarea no se trunque y se almacene correctamente
    incluso si es un texto largo.

    Args:
        limpiar_base_datos (fixture): Fixture que inicializa el sistema y limpia la base de datos.
    """
    sistema = limpiar_base_datos
    texto_largo = "A" * 255
    with patch('builtins.input', side_effect=["Tarea larga", texto_largo, "Trabajo", "Por hacer"]):
        Tarea(sistema.usuarios_tareas, sistema.usuario_actual)
        assert sistema.usuarios_tareas["usuario1"][0]["texto"] == texto_largo

def test_crear_tareas_estado_inusual(limpiar_base_datos):
    """
    Test para verificar que una tarea se puede crear con un estado inusual.

    Verifica que el sistema permita el estado "En pausa" como valor válido
    para el estado de una tarea.

    Args:
        limpiar_base_datos (fixture): Fixture que inicializa el sistema y limpia la base de datos.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Estudiar", "Estudiar", "Estudio", "En pausa"]):
        Tarea(sistema.usuarios_tareas, sistema.usuario_actual)
        assert sistema.usuarios_tareas["usuario1"][0]["estado"] == "En pausa"

def test_crear_tareas_categoria_desconocida(limpiar_base_datos):
    """
    Test para verificar que una tarea se crea con una categoría desconocida.

    Verifica que el sistema permita el uso de una categoría no predefinida,
    como "Otro", sin generar errores.

    Args:
        limpiar_base_datos (fixture): Fixture que inicializa el sistema y limpia la base de datos.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Viajar", "Viajar", "Otro", "Por hacer"]):
        Tarea(sistema.usuarios_tareas, sistema.usuario_actual)
        assert sistema.usuarios_tareas["usuario1"][0]["categoría"] == "Otro"

def test_error_tarea_sin_texto(limpiar_base_datos, capfd):
    """
    Test para verificar el manejo de error cuando no se ingresa texto para la tarea.

    Verifica que el sistema arroje un error cuando se intenta crear una tarea
    sin texto y que el mensaje de error adecuado se imprima en la salida estándar.

    Args:
        limpiar_base_datos (fixture): Fixture que inicializa el sistema y limpia la base de datos.
        capfd (pytest fixture): Fixture para capturar la salida estándar y verificar errores.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Tarea sin texto", "", "Personal", "Por hacer"]):
        Tarea(sistema.usuarios_tareas, sistema.usuario_actual)
        out, _ = capfd.readouterr()
        assert "Error: El texto no puede estar vacío" in out
        assert "usuario1" not in sistema.usuarios_tareas or len(sistema.usuarios_tareas["usuario1"]) == 0

def test_error_tarea_sin_categoria(limpiar_base_datos, capfd):
    """
    Test para verificar el manejo de error cuando no se ingresa categoría para la tarea.

    Verifica que el sistema arroje un error cuando no se ingresa una categoría
    para la tarea y que el mensaje de error adecuado se imprima en la salida estándar.

    Args:
        limpiar_base_datos (fixture): Fixture que inicializa el sistema y limpia la base de datos.
        capfd (pytest fixture): Fixture para capturar la salida estándar y verificar errores.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Hacer ejercicio", "Hacer ejercicio", "", "Por hacer"]):
        Tarea(sistema.usuarios_tareas, sistema.usuario_actual)
        out, _ = capfd.readouterr()
        assert "Error: La categoría es requerida" in out
        assert "usuario1" not in sistema.usuarios_tareas or len(sistema.usuarios_tareas["usuario1"]) == 0

def test_error_tarea_sin_estado(limpiar_base_datos, capfd):
    """
    Test para verificar el manejo de error cuando no se ingresa estado para la tarea.

    Verifica que el sistema arroje un error cuando no se ingresa un estado
    para la tarea y que el mensaje de error adecuado se imprima en la salida estándar.

    Args:
        limpiar_base_datos (fixture): Fixture que inicializa el sistema y limpia la base de datos.
        capfd (pytest fixture): Fixture para capturar la salida estándar y verificar errores.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Revisar correo", "Revisar correo", "Trabajo", ""]):
        Tarea(sistema.usuarios_tareas, sistema.usuario_actual)
        out, _ = capfd.readouterr()
        assert "Error: El estado es requerido" in out
        assert "usuario1" not in sistema.usuarios_tareas or len(sistema.usuarios_tareas["usuario1"]) == 0
