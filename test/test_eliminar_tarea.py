import pytest
from src.controller.sistema import Sistema
from unittest.mock import patch
from datetime import datetime

# Fixture para limpiar la base de datos antes de cada prueba
@pytest.fixture(autouse=True)
def limpiar_base_datos():
    """
    Fixture para limpiar la base de datos antes de cada prueba.
    Inicializa el sistema con un usuario y una tarea predeterminados.
    """
    sistema = Sistema()
    sistema.usuarios.clear()
    sistema.usuarios_tareas.clear()
    sistema.usuario_actual = "usuario1"
    sistema.usuarios["usuario1"] = {
        "Nombre": "Juan",
        "Apellido": "Prueba",
        "Correo": "usuario1",
        "Contraseña": "123",
        "Activo": True
    }
    sistema.usuarios_tareas["usuario1"] = [{
        "nombre": "Hacer ejercicio",
        "texto": "Hacer ejercicio",
        "fecha": "2025-04-05 19:21:11",
        "categoría": "Salud",
        "estado": "Por Hacer"
    }]
    return sistema

def test_eliminar_tarea_existente(limpiar_base_datos):
    """
    Prueba que elimina una tarea existente de la base de datos.
    Verifica que la tarea se haya eliminado correctamente.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Hacer ejercicio"]):
        resultado = sistema.eliminar_tarea()
        assert resultado == "Tarea eliminada."
        assert len(sistema.usuarios_tareas["usuario1"]) == 0

def test_eliminar_tarea_estado_completada(limpiar_base_datos):
    """
    Prueba que elimina una tarea con estado 'Completada'.
    Verifica que la tarea se haya eliminado correctamente.
    """
    sistema = limpiar_base_datos
    sistema.usuarios_tareas["usuario1"][0]["estado"] = "Completada"
    with patch('builtins.input', side_effect=["Hacer ejercicio"]):
        resultado = sistema.eliminar_tarea()
        assert resultado == "Tarea eliminada."
        assert len(sistema.usuarios_tareas["usuario1"]) == 0

def test_eliminar_tarea_estado_por_hacer(limpiar_base_datos):
    """
    Prueba que elimina una tarea con estado 'Por Hacer'.
    Verifica que la tarea se haya eliminado correctamente.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Hacer ejercicio"]):
        resultado = sistema.eliminar_tarea()
        assert resultado == "Tarea eliminada."
        assert len(sistema.usuarios_tareas["usuario1"]) == 0

def test_eliminar_tarea_id_limite(limpiar_base_datos):
    """
    Prueba que elimina una tarea cuando se alcanza el límite de tareas.
    Verifica que la tarea se haya eliminado correctamente.
    """
    sistema = limpiar_base_datos
    sistema.usuarios_tareas["usuario1"].append({
        "nombre": "Tarea límite",
        "texto": "Texto de la tarea límite",
        "fecha": "2025-04-05 19:21:11",
        "categoría": "Trabajo",
        "estado": "Por Hacer"
    })
    with patch('builtins.input', side_effect=["Tarea límite"]):
        resultado = sistema.eliminar_tarea()
        assert resultado == "Tarea eliminada."
        assert len(sistema.usuarios_tareas["usuario1"]) == 1

def test_eliminar_tarea_muchas_ediciones(limpiar_base_datos):
    """
    Prueba que elimina una tarea que ha sido editada varias veces.
    Verifica que la tarea se haya eliminado correctamente.
    """
    sistema = limpiar_base_datos
    sistema.usuarios_tareas["usuario1"][0]["texto"] = "Texto editado varias veces"
    with patch('builtins.input', side_effect=["Hacer ejercicio"]):
        resultado = sistema.eliminar_tarea()
        assert resultado == "Tarea eliminada."
        assert len(sistema.usuarios_tareas["usuario1"]) == 0

def test_eliminar_tarea_usuario_muchas_tareas(limpiar_base_datos):
    """
    Prueba que elimina una tarea de un usuario con muchas tareas en su lista.
    Verifica que la tarea se haya eliminado correctamente.
    """
    sistema = limpiar_base_datos
    for i in range(100):
        sistema.usuarios_tareas["usuario1"].append({
            "nombre": f"Tarea {i}",
            "texto": f"Texto de la tarea {i}",
            "fecha": "2025-04-05 19:21:11",
            "categoría": "Trabajo",
            "estado": "Por Hacer"
        })
    with patch('builtins.input', side_effect=["Tarea 50"]):
        resultado = sistema.eliminar_tarea()
        assert resultado == "Tarea eliminada."
        assert len(sistema.usuarios_tareas["usuario1"]) == 100

def test_eliminar_tarea_inexistente(limpiar_base_datos):
    """
    Prueba que intenta eliminar una tarea que no existe.
    Verifica que se reciba un mensaje de error adecuado.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Tarea inexistente"]):
        resultado = sistema.eliminar_tarea()
        assert resultado == "Tarea no encontrada."

def test_eliminar_tarea_sin_permisos(limpiar_base_datos):
    """
    Prueba que intenta eliminar una tarea cuando el usuario no tiene permisos.
    Verifica que se reciba un mensaje de error adecuado.
    """
    sistema = limpiar_base_datos
    sistema.usuario_actual = "usuario2"
    sistema.usuarios["usuario2"] = {
        "Nombre": "Ana",
        "Apellido": "Prueba",
        "Correo": "usuario2",
        "Contraseña": "123",
        "Activo": True
    }
    with patch('builtins.input', side_effect=["Hacer ejercicio"]):
        resultado = sistema.eliminar_tarea()
        assert resultado == "Tarea no encontrada."

def test_eliminar_tarea_sin_id(limpiar_base_datos):
    """
    Prueba que intenta eliminar una tarea sin proporcionar un ID.
    Verifica que se reciba un mensaje de error adecuado.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=[""]):
        resultado = sistema.eliminar_tarea()
        assert resultado == "Error: Debe proporcionar un ID"
