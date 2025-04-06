import pytest
from src.model.tarea import Eliminar
from src.model.db_global import db
from unittest.mock import patch
from datetime import datetime


@pytest.fixture(autouse=True)
def limpiar_base_datos():
    db.usuarios.clear()
    db.usuarios_tareas.clear()
    db.usuario_actual = "usuario1"
    db.usuarios["usuario1"] = {
        "Nombre": "Juan",
        "Apellido": "Prueba",
        "Correo": "usuario1",
        "Contraseña": "123"
    }
    db.usuarios_tareas["usuario1"] = [{
        "nombre": "Hacer ejercicio",
        "texto": "Hacer ejercicio",
        "fecha": "2025-04-05 19:21:11",
        "categoría": "Salud",
        "estado": "Por Hacer"
    }]

def test_eliminar_tarea_existente():
    with patch('builtins.input', side_effect=["Hacer ejercicio"]):
        eliminar = Eliminar()
        resultado = eliminar.eliminar_tarea()
        assert resultado == "Tarea eliminada."
        assert len(db.usuarios_tareas["usuario1"]) == 0


def test_eliminar_tarea_estado_completada():
    db.usuarios_tareas["usuario1"][0]["estado"] = "Completada"
    with patch('builtins.input', side_effect=["Hacer ejercicio"]):
        eliminar = Eliminar()
        resultado = eliminar.eliminar_tarea()
        assert resultado == "Tarea eliminada."
        assert len(db.usuarios_tareas["usuario1"]) == 0


def test_eliminar_tarea_estado_por_hacer():
    with patch('builtins.input', side_effect=["Hacer ejercicio"]):
        eliminar = Eliminar()
        resultado = eliminar.eliminar_tarea()
        assert resultado == "Tarea eliminada."
        assert len(db.usuarios_tareas["usuario1"]) == 0


def test_eliminar_tarea_id_limite():
    db.usuarios_tareas["usuario1"].append({
        "nombre": "Tarea límite",
        "texto": "Texto de la tarea límite",
        "fecha": "2025-04-05 19:21:11",
        "categoría": "Trabajo",
        "estado": "Por Hacer"
    })
    with patch('builtins.input', side_effect=["Tarea límite"]):
        eliminar = Eliminar()
        resultado = eliminar.eliminar_tarea()
        assert resultado == "Tarea eliminada."
        assert len(db.usuarios_tareas["usuario1"]) == 1


def test_eliminar_tarea_muchas_ediciones():
    db.usuarios_tareas["usuario1"][0]["texto"] = "Texto editado varias veces"
    with patch('builtins.input', side_effect=["Hacer ejercicio"]):
        eliminar = Eliminar()
        resultado = eliminar.eliminar_tarea()
        assert resultado == "Tarea eliminada."
        assert len(db.usuarios_tareas["usuario1"]) == 0


def test_eliminar_tarea_usuario_muchas_tareas():
    for i in range(100):
        db.usuarios_tareas["usuario1"].append({
            "nombre": f"Tarea {i}",
            "texto": f"Texto de la tarea {i}",
            "fecha": "2025-04-05 19:21:11",
            "categoría": "Trabajo",
            "estado": "Por Hacer"
        })
    with patch('builtins.input', side_effect=["Tarea 50"]):
        eliminar = Eliminar()
        resultado = eliminar.eliminar_tarea()
        assert resultado == "Tarea eliminada."
        assert len(db.usuarios_tareas["usuario1"]) == 100


def test_eliminar_tarea_inexistente():
    with patch('builtins.input', side_effect=["Tarea inexistente"]):
        eliminar = Eliminar()
        resultado = eliminar.eliminar_tarea()
        assert resultado == "Tarea no encontrada."


def test_eliminar_tarea_sin_permisos():
    db.usuario_actual = "usuario2"
    db.usuarios["usuario2"] = {
        "Nombre": "Ana",
        "Apellido": "Prueba",
        "Correo": "usuario2",
        "Contraseña": "123"
    }
    with patch('builtins.input', side_effect=["Hacer ejercicio"]):
        eliminar = Eliminar()
        resultado = eliminar.eliminar_tarea()
        assert resultado == "Tarea no encontrada."


def test_eliminar_tarea_sin_id():
    with patch('builtins.input', side_effect=[""]):
        eliminar = Eliminar()
        resultado = eliminar.eliminar_tarea()
        assert resultado == "Error: Debe proporcionar un ID"