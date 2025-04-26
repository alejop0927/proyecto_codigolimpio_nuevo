from unittest.mock import patch, MagicMock, ANY
from src.controller.sistema import Sistema
import pytest

@pytest.fixture
def sistema_mockeado():
    """
    Fixture que crea un objeto Sistema simulado con una conexión a base de datos simulada.
    
    Esta fixture es utilizada para configurar el sistema de pruebas con la conexión y cursor 
    necesarios para ejecutar las pruebas de edición de tareas.
    """
    with patch('src.model.conexion.obtener_conexion_bd') as mock_obtener_conexion_bd:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_obtener_conexion_bd.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        sistema = Sistema()
        sistema.conn = mock_conn
        sistema.cursor = mock_cursor
        sistema.usuario_actual_id = 1

        yield sistema, mock_cursor, mock_conn

def preparar_mock_busqueda(mock_cursor, tarea_existente=True):
    """
    Configura el mock de la búsqueda en la base de datos para simular una tarea existente o no.

    :param mock_cursor: El cursor simulado de la base de datos.
    :param tarea_existente: Si es True, simula que la tarea existe, si es False, simula que no existe.
    """
    if tarea_existente:
        mock_cursor.fetchone.return_value = (1, "Texto", "Texto", "Categoría", "Estado")
    else:
        mock_cursor.fetchone.return_value = None

def test_editar_texto_tarea_existente(sistema_mockeado):
    """
    Prueba la edición del texto de una tarea existente.

    Verifica que al editar una tarea con un texto nuevo, se realice la llamada 
    adecuada al método de la base de datos.
    """
    sistema, mock_cursor, mock_conn = sistema_mockeado
    preparar_mock_busqueda(mock_cursor)

    resultado = sistema.editar_tarea("Comprar leche", "Comprar leche y pan", "Compras", "Por hacer")

    mock_cursor.execute.assert_any_call(
        ANY,
        ("Comprar leche y pan", "Compras", "Por hacer", ANY, 1)
    )

def test_editar_categoria_tarea_existente(sistema_mockeado):
    """
    Prueba la edición de la categoría de una tarea existente.

    Verifica que al cambiar la categoría de una tarea existente, se realice la 
    llamada adecuada al método de la base de datos.
    """
    sistema, mock_cursor, mock_conn = sistema_mockeado
    preparar_mock_busqueda(mock_cursor)

    resultado = sistema.editar_tarea("Ir al gimnasio", "Ir al gimnasio", "Deporte", "Por hacer")

    mock_cursor.execute.assert_any_call(
        ANY,
        ("Ir al gimnasio", "Deporte", "Por hacer", ANY, 1)
    )

def test_editar_estado_tarea_existente(sistema_mockeado):
    """
    Prueba la edición del estado de una tarea existente.

    Verifica que al cambiar el estado de una tarea existente, se realice la 
    llamada adecuada al método de la base de datos y que el resultado sea el esperado.
    """
    sistema, mock_cursor, mock_conn = sistema_mockeado
    preparar_mock_busqueda(mock_cursor)

    resultado = sistema.editar_tarea("Leer libro", "Leer libro", "Educación", "Completada")

    mock_cursor.execute.assert_any_call(
        ANY,
        ("Leer libro", "Educación", "Completada", ANY, 1)
    )
    assert resultado == "Tarea actualizada correctamente"

def test_editar_tarea_estado_limite(sistema_mockeado):
    """
    Prueba la edición de una tarea con un estado en el límite permitido.

    Verifica que el sistema permita la actualización con estados válidos, como "Pendiente".
    """
    sistema, mock_cursor, mock_conn = sistema_mockeado
    preparar_mock_busqueda(mock_cursor)

    resultado = sistema.editar_tarea("Estudiar", "Estudiar", "Educación", "Pendiente")
    assert resultado == "Tarea actualizada correctamente"

def test_editar_tarea_categoria_nueva(sistema_mockeado):
    """
    Prueba la edición de una tarea con una nueva categoría.

    Verifica que el sistema permita actualizar una tarea con una nueva categoría válida.
    """
    sistema, mock_cursor, mock_conn = sistema_mockeado
    preparar_mock_busqueda(mock_cursor)

    resultado = sistema.editar_tarea("Viajar", "Viajar", "Placer", "Por hacer")
    assert resultado == "Tarea actualizada correctamente"

def test_editar_tarea_inexistente(sistema_mockeado):
    """
    Prueba la edición de una tarea que no existe.

    Verifica que el sistema devuelva un mensaje adecuado cuando se intenta editar una tarea inexistente.
    """
    sistema, mock_cursor, _ = sistema_mockeado
    preparar_mock_busqueda(mock_cursor, tarea_existente=False)

    resultado = sistema.editar_tarea("Tarea inexistente", "Nuevo texto", "Nueva categoría", "Nuevo estado")
    assert resultado == "Tarea no encontrada"

def test_editar_tarea_combinacion_cambios(sistema_mockeado):
    """
    Prueba la edición de una tarea con múltiples cambios en texto, categoría y estado.

    Verifica que el sistema maneje correctamente la combinación de cambios en una tarea existente.
    """
    sistema, mock_cursor, _ = sistema_mockeado
    preparar_mock_busqueda(mock_cursor)

    resultado = sistema.editar_tarea("Leer libro", "Estudiar", "Educación", "Completada")
    assert resultado == "Tarea actualizada correctamente"

def test_editar_tarea_estado_inusual(sistema_mockeado):
    """
    Prueba la edición de una tarea con un estado inusual.

    Verifica que el sistema permita actualizar una tarea con un estado inusual como "En pausa".
    """
    sistema, mock_cursor, _ = sistema_mockeado
    preparar_mock_busqueda(mock_cursor)

    resultado = sistema.editar_tarea("Estudiar", "Estudiar", "Educación", "En pausa")
    assert resultado == "Tarea actualizada correctamente"

def test_editar_tarea_estado_completada(sistema_mockeado):
    """
    Prueba la edición de una tarea con estado "Completada".

    Verifica que el sistema permita actualizar una tarea con el estado "Completada" correctamente.
    """
    sistema, mock_cursor, _ = sistema_mockeado
    preparar_mock_busqueda(mock_cursor)

    resultado = sistema.editar_tarea("Comprar leche", "Comprar leche", "Compras", "Completada")
    assert resultado == "Tarea actualizada correctamente"
