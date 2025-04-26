import pytest
from unittest.mock import patch, MagicMock
from src.model.tarea import Tarea

@patch('src.model.conexion.obtener_conexion_bd')
def test_crear_tarea_texto_valido(mock_obtener_conexion_bd):
    """
    Prueba que valida la creación de una tarea con un texto válido.
    Se asegura de que la tarea se cree correctamente cuando los parámetros
    de entrada son correctos.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_obtener_conexion_bd.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.side_effect = [(1,), None]

    tarea = Tarea(1, "Comprar leche", "Comprar leche", "Compras", "Por hacer")
    assert tarea is not None

@patch('src.model.conexion.obtener_conexion_bd')
def test_crear_tarea_estado_por_hacer(mock_obtener_conexion_bd):
    """
    Prueba que valida la creación de una tarea con el estado "Por hacer".
    Asegura que la tarea sea creada correctamente cuando el estado es el esperado.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_obtener_conexion_bd.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.side_effect = [(1,), None]

    tarea = Tarea(1, "Ir al gimnasio", "Ir al gimnasio", "Salud", "Por hacer")
    assert tarea is not None

@patch('src.model.conexion.obtener_conexion_bd')
def test_crear_tarea_usuario_registrado(mock_obtener_conexion_bd):
    """
    Prueba que valida la creación de una tarea cuando el usuario está registrado.
    Verifica que la tarea se cree si el usuario existe en la base de datos.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_obtener_conexion_bd.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.side_effect = [(1,), None]

    tarea = Tarea(1, "Leer libro", "Leer libro", "Educación", "Por hacer")
    assert tarea is not None

@patch('src.model.conexion.obtener_conexion_bd')
def test_crear_tarea_texto_largo(mock_obtener_conexion_bd):
    """
    Prueba que valida la creación de una tarea con un texto largo.
    Se asegura de que la tarea se pueda crear correctamente si el texto no excede el límite.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_obtener_conexion_bd.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.side_effect = [(1,), None]

    tarea = Tarea(1, "Trabajo largo", "A" * 255, "Trabajo", "Por hacer")
    assert tarea is not None

@patch('src.model.conexion.obtener_conexion_bd')
def test_crear_tarea_estado_inusual(mock_obtener_conexion_bd):
    """
    Prueba que valida la creación de una tarea con un estado inusual.
    Verifica que la tarea se cree correctamente si el estado es válido pero no común.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_obtener_conexion_bd.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.side_effect = [(1,), None]

    tarea = Tarea(1, "Estudiar", "Estudiar", "Educación", "En pausa")
    assert tarea is not None

@patch('src.model.conexion.obtener_conexion_bd')
def test_crear_tarea_categoria_desconocida(mock_obtener_conexion_bd):
    """
    Prueba que valida la creación de una tarea con una categoría desconocida.
    Verifica que la tarea se cree correctamente incluso si la categoría no es estándar.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_obtener_conexion_bd.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.side_effect = [(1,), None]

    tarea = Tarea(1, "Viajar", "Viajar", "Otro", "Por hacer")
    assert tarea is not None

@patch('src.model.conexion.obtener_conexion_bd')
def test_crear_tarea_sin_texto(mock_obtener_conexion_bd):
    """
    Prueba que valida que se lance un error si el texto de la tarea está vacío.
    Se asegura de que se levante un ValueError con el mensaje adecuado.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_obtener_conexion_bd.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    with pytest.raises(ValueError, match="Error: El texto no puede estar vacío"):
        Tarea(1, "b", "", "Personal", "Por hacer")

@patch('src.model.conexion.obtener_conexion_bd')
def test_crear_tarea_sin_categoria(mock_obtener_conexion_bd):
    """
    Prueba que valida que se lance un error si no se proporciona una categoría.
    Se asegura de que se levante un ValueError con el mensaje adecuado.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_obtener_conexion_bd.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    with pytest.raises(ValueError, match="Error: La categoría es requerida"):
        Tarea(1, "Hacer ejercicio", "Hacer ejercicio", "", "Por hacer")

@patch('src.model.conexion.obtener_conexion_bd')
def test_crear_tarea_sin_estado(mock_obtener_conexion_bd):
    """
    Prueba que valida que se lance un error si no se proporciona un estado.
    Se asegura de que se levante un ValueError con el mensaje adecuado.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_obtener_conexion_bd.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    with pytest.raises(ValueError, match="Error: El estado es requerido"):
        Tarea(1, "Revisar correo", "Revisar correo", "Trabajo", "")

if __name__ == '__main__':
    pytest.main()
