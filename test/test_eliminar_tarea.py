import pytest

from src.model.bd_mock.base_datos_mock import Base_datos_mock
from unittest.mock import patch
from datetime import datetime
class Eliminar:
    """
    Clase para eliminar tareas de la base de datos mock.
    """

    def __init__(self):
        """
        Inicializa la clase Eliminar con la base de datos mock.
        """
        self.db = db_mock

    def eliminar_tarea(self, nombre_tarea):
        """
        Elimina una tarea asignada al usuario actual.

        Parámetros:
            nombre_tarea (str): Nombre de la tarea a eliminar.

        Retorna:
            str: Mensaje de éxito o error.
        """
        if self.db.usuario_actual is None:
            return "Error: Debe iniciar sesión"

        if not nombre_tarea:
            return "Error: Debe proporcionar un nombre de tarea"

        tareas_usuario = self.db.usuarios_tareas.get(self.db.usuario_actual, [])
        tarea = next((t for t in tareas_usuario if t["nombre"] == nombre_tarea), None)

        if not tarea:
            return "Error: La tarea no existe"

        if tarea["estado"] == "Completada":
            return "Error: No se puede eliminar una tarea completada"

        self.db.usuarios_tareas[self.db.usuario_actual] = [
            t for t in tareas_usuario if t["nombre"] != nombre_tarea
        ]

        return "Tarea eliminada correctamente"


# Instancia de la base de datos mock
db_mock = Base_datos_mock()

@pytest.fixture(autouse=True)
def limpiar_base_datos():
    """
    Fixture que limpia la base de datos antes de cada prueba.
    """
    db_mock.usuarios.clear()
    db_mock.usuarios_tareas.clear()
    db_mock.usuario_actual = "usuario1"
    db_mock.usuarios["usuario1"] = {
        "Nombre": "Juan",
        "Apellido": "Prueba",
        "Correo": "usuario1",
        "Contraseña": "123"
    }
    db_mock.usuarios_tareas["usuario1"] = [{
        "nombre": "Hacer ejercicio",
        "texto": "Hacer ejercicio",
        "fecha": "2025-04-05 19:21:11",
        "categoría": "Salud",
        "estado": "Por Hacer"
    }]

def test_eliminar_tarea_existente():
    """
    Prueba la eliminación de una tarea existente.

    Verifica que al eliminar una tarea existente, se elimine correctamente de la base de datos.
    """
    with patch('builtins.input', side_effect=["Hacer ejercicio"]):
        eliminar = Eliminar()
        resultado = eliminar.eliminar_tarea("Hacer ejercicio")
        assert resultado == "Tarea eliminada correctamente"
        assert len(db_mock.usuarios_tareas["usuario1"]) == 0

def test_eliminar_tarea_estado_completada():
    """
    Prueba la eliminación de una tarea con estado 'Completada'.

    Verifica que no se pueda eliminar una tarea que ya está completada.
    """
    db_mock.usuarios_tareas["usuario1"][0]["estado"] = "Completada"
    with patch('builtins.input', side_effect=["Hacer ejercicio"]):
        eliminar = Eliminar()
        resultado = eliminar.eliminar_tarea("Hacer ejercicio")
        assert resultado == "Error: No se puede eliminar una tarea completada"
        assert len(db_mock.usuarios_tareas["usuario1"]) == 1

def test_eliminar_tarea_estado_por_hacer():
    """
    Prueba la eliminación de una tarea con estado 'Por Hacer'.

    Verifica que al eliminar una tarea con estado 'Por Hacer', se elimine correctamente de la base de datos.
    """
    with patch('builtins.input', side_effect=["Hacer ejercicio"]):
        eliminar = Eliminar()
        resultado = eliminar.eliminar_tarea("Hacer ejercicio")
        assert resultado == "Tarea eliminada correctamente"
        assert len(db_mock.usuarios_tareas["usuario1"]) == 0

def test_eliminar_tarea_id_limite():
    """
    Prueba la eliminación de una tarea en el límite del diccionario.

    Verifica que al eliminar una tarea en el límite del diccionario, se elimine correctamente de la base de datos.
    """
    db_mock.usuarios_tareas["usuario1"].append({
        "nombre": "Tarea límite",
        "texto": "Texto de la tarea límite",
        "fecha": "2025-04-05 19:21:11",
        "categoría": "Trabajo",
        "estado": "Por Hacer"
    })
    with patch('builtins.input', side_effect=["Tarea límite"]):
        eliminar = Eliminar()
        resultado = eliminar.eliminar_tarea("Tarea límite")
        assert resultado == "Tarea eliminada correctamente"
        assert len(db_mock.usuarios_tareas["usuario1"]) == 1

def test_eliminar_tarea_muchas_ediciones():
    """
    Prueba la eliminación de una tarea con múltiples ediciones.

    Verifica que al eliminar una tarea con múltiples ediciones, se elimine correctamente de la base de datos.
    """
    db_mock.usuarios_tareas["usuario1"][0]["texto"] = "Texto editado varias veces"
    with patch('builtins.input', side_effect=["Hacer ejercicio"]):
        eliminar = Eliminar()
        resultado = eliminar.eliminar_tarea("Hacer ejercicio")
        assert resultado == "Tarea eliminada correctamente"
        assert len(db_mock.usuarios_tareas["usuario1"]) == 0

def test_eliminar_tarea_usuario_muchas_tareas():
    """
    Prueba la eliminación de una tarea cuando el usuario tiene muchas tareas.

    Verifica que al eliminar una tarea cuando el usuario tiene muchas tareas, se elimine correctamente de la base de datos.
    """
    for i in range(100):
        db_mock.usuarios_tareas["usuario1"].append({
            "nombre": f"Tarea {i}",
            "texto": f"Texto de la tarea {i}",
            "fecha": "2025-04-05 19:21:11",
            "categoría": "Trabajo",
            "estado": "Por Hacer"
        })
    with patch('builtins.input', side_effect=["Tarea 50"]):
        eliminar = Eliminar()
        resultado = eliminar.eliminar_tarea("Tarea 50")
        assert resultado == "Tarea eliminada correctamente"
        assert len(db_mock.usuarios_tareas["usuario1"]) == 100

def test_eliminar_tarea_inexistente():
    """
    Prueba la eliminación de una tarea que no existe.

    Verifica que el sistema devuelva un mensaje adecuado cuando se intenta eliminar una tarea inexistente.
    """
    with patch('builtins.input', side_effect=["Tarea inexistente"]):
        eliminar = Eliminar()
        resultado = eliminar.eliminar_tarea("Tarea inexistente")
        assert resultado == "Error: La tarea no existe"

def test_eliminar_tarea_sin_permisos():
    """
    Prueba la eliminación de una tarea sin permisos.

    Verifica que el sistema devuelva un mensaje adecuado cuando se intenta eliminar una tarea sin tener permisos.
    """
    db_mock.usuario_actual = "usuario2"
    db_mock.usuarios["usuario2"] = {
        "Nombre": "Ana",
        "Apellido": "Prueba",
        "Correo": "usuario2",
        "Contraseña": "123"
    }
    with patch('builtins.input', side_effect=["Hacer ejercicio"]):
        eliminar = Eliminar()
        resultado = eliminar.eliminar_tarea("Hacer ejercicio")
        assert resultado == "Error: La tarea no existe"

def test_eliminar_tarea_sin_id():
    """
    Prueba la eliminación de una tarea sin proporcionar un nombre de tarea.

    Verifica que el sistema devuelva un mensaje adecuado cuando no se proporciona un nombre de tarea.
    """
    with patch('builtins.input', side_effect=[""]):
        eliminar = Eliminar()
        resultado = eliminar.eliminar_tarea("")
        assert resultado == "Error: Debe proporcionar un nombre de tarea"
