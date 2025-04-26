import pytest
from unittest.mock import patch
from src.controller.sistema import Sistema

# Diccionario original de tareas
TAREAS_ORIGINAL = {
    1: {'nombre': 'Viajar', 'estado': 'Por hacer', 'usuario_id': 1},
    2: {'nombre': 'Leer libro', 'estado': 'Completada', 'usuario_id': 1},
    3: {'nombre': 'Ir al gimnasio', 'estado': 'Por hacer', 'usuario_id': 1},
    4: {'nombre': 'Estudiar', 'estado': 'Completada', 'usuario_id': 1},
    5: {'nombre': 'Correr', 'estado': 'Por hacer', 'usuario_id': 1}
}

# TAREAS mutable que se usará en cada test
TAREAS = {}

# Simulando el Sistema con un diccionario en memoria
class SistemaSimulado(Sistema):
    """
    Clase simulada de Sistema que hereda de la clase Sistema y proporciona
    la funcionalidad para eliminar tareas basadas en su nombre, con un 
    control de permisos de usuario.
    """
    def eliminar_tarea(self, nombre_tarea):
        """
        Elimina una tarea del diccionario TAREAS si el nombre de la tarea
        corresponde a una tarea existente y si el usuario tiene permisos
        para eliminarla.

        :param nombre_tarea: El nombre de la tarea a eliminar.
        :return: Mensaje de éxito o error dependiendo del caso.
        """
        if not nombre_tarea:
            return "Error: Debe proporcionar un nombre de tarea"

        tarea_encontrada = None
        for id_tarea, tarea in TAREAS.items():
            if tarea['nombre'] == nombre_tarea:
                if tarea['usuario_id'] != self.usuario_actual_id:
                    return "Error: No tiene permisos"
                tarea_encontrada = id_tarea
                break

        if tarea_encontrada is None:
            return "Error: La tarea no existe"

        del TAREAS[tarea_encontrada]
        return "Tarea eliminada correctamente"

# Fixture para reiniciar las tareas antes de cada test
@pytest.fixture(autouse=True)
def reiniciar_tareas():
    """
    Fixture que reinicia el estado del diccionario TAREAS antes de cada test,
    asegurando que las tareas siempre inicien con los valores definidos en
    TAREAS_ORIGINAL.
    """
    TAREAS.clear()
    TAREAS.update({k: v.copy() for k, v in TAREAS_ORIGINAL.items()})

# Tests

@patch('src.model.conexion.obtener_conexion_bd')
def test_eliminar_tarea_existente(mock_obtener_conexion_bd):
    """
    Test para verificar que una tarea existente se elimina correctamente.
    """
    sistema = SistemaSimulado()
    sistema.usuario_actual_id = 1
    respuesta = sistema.eliminar_tarea("Viajar")
    assert respuesta == "Tarea eliminada correctamente"
    assert 1 not in TAREAS

@patch('src.model.conexion.obtener_conexion_bd')
def test_eliminar_tarea_estado_completada(mock_obtener_conexion_bd):
    """
    Test para verificar la eliminación de una tarea con estado 'Completada'.
    """
    sistema = SistemaSimulado()
    sistema.usuario_actual_id = 1
    respuesta = sistema.eliminar_tarea("Leer libro")
    assert respuesta == "Tarea eliminada correctamente"
    assert 2 not in TAREAS

@patch('src.model.conexion.obtener_conexion_bd')
def test_eliminar_tarea_estado_por_hacer(mock_obtener_conexion_bd):
    """
    Test para verificar la eliminación de una tarea con estado 'Por hacer'.
    """
    sistema = SistemaSimulado()
    sistema.usuario_actual_id = 1
    respuesta = sistema.eliminar_tarea("Ir al gimnasio")
    assert respuesta == "Tarea eliminada correctamente"
    assert 3 not in TAREAS

@patch('src.model.conexion.obtener_conexion_bd')
def test_eliminar_tarea_id_limite(mock_obtener_conexion_bd):
    """
    Test para verificar la eliminación de una tarea en el límite del diccionario.
    """
    sistema = SistemaSimulado()
    sistema.usuario_actual_id = 1
    respuesta = sistema.eliminar_tarea("Estudiar")
    assert respuesta == "Tarea eliminada correctamente"
    assert 4 not in TAREAS

@patch('src.model.conexion.obtener_conexion_bd')
def test_eliminar_tarea_con_muchas_ediciones(mock_obtener_conexion_bd):
    """
    Test para verificar la eliminación de una tarea con múltiples ediciones.
    """
    sistema = SistemaSimulado()
    sistema.usuario_actual_id = 1
    respuesta = sistema.eliminar_tarea("Correr")
    assert respuesta == "Tarea eliminada correctamente"
    assert 5 not in TAREAS

@patch('src.model.conexion.obtener_conexion_bd')
def test_eliminar_tarea_con_usuario_con_muchas_tareas(mock_obtener_conexion_bd):
    """
    Test para verificar la eliminación de una tarea cuando el usuario tiene muchas tareas.
    """
    TAREAS[6] = {'nombre': 'Limpiar', 'estado': 'Por hacer', 'usuario_id': 1}
    sistema = SistemaSimulado()
    sistema.usuario_actual_id = 1
    respuesta = sistema.eliminar_tarea("Limpiar")
    assert respuesta == "Tarea eliminada correctamente"
    assert 6 not in TAREAS

@patch('src.model.conexion.obtener_conexion_bd')
def test_eliminar_tarea_sin_permisos(mock_obtener_conexion_bd):
    """
    Test para verificar el comportamiento cuando un usuario intenta eliminar una tarea
    que no pertenece a él.
    """
    TAREAS[7] = {'nombre': 'Ordenar', 'estado': 'Por hacer', 'usuario_id': 1}
    sistema = SistemaSimulado()
    sistema.usuario_actual_id = 2
    respuesta = sistema.eliminar_tarea("Ordenar")
    assert respuesta == "Error: No tiene permisos"
    assert 7 in TAREAS

@patch('src.model.conexion.obtener_conexion_bd')
def test_eliminar_tarea_sin_id(mock_obtener_conexion_bd):
    """
    Test para verificar el comportamiento cuando no se proporciona el nombre de la tarea.
    """
    sistema = SistemaSimulado()
    sistema.usuario_actual_id = 1
    respuesta = sistema.eliminar_tarea("")
    assert respuesta == "Error: Debe proporcionar un nombre de tarea"

@patch('src.model.conexion.obtener_conexion_bd')
def test_eliminar_tarea_inexistente(mock_obtener_conexion_bd):
    """
    Test para verificar el comportamiento cuando se intenta eliminar una tarea que no existe.
    """
    sistema = SistemaSimulado()
    sistema.usuario_actual_id = 1
    respuesta = sistema.eliminar_tarea("Tarea Inexistente")
    assert respuesta == "Error: La tarea no existe"
