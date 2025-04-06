import pytest
from src.model.tarea import Editar
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


def test_editar_texto_tarea_existente():
    with patch('builtins.input', side_effect=["Hacer ejercicio", "Hacer cardio", "", ""]):
        editar = Editar()
        resultado = editar.editar_tarea()
        assert resultado == "Tarea actualizada con éxito."
        assert db.usuarios_tareas["usuario1"][0]["texto"] == "Hacer cardio"


def test_editar_categoria_tarea_existente():
    with patch('builtins.input', side_effect=["Hacer ejercicio", "", "Educación", ""]):
        editar = Editar()
        resultado = editar.editar_tarea()
        assert resultado == "Tarea actualizada con éxito."
        assert db.usuarios_tareas["usuario1"][0]["categoría"] == "Educación"


def test_editar_estado_tarea_existente():
    with patch('builtins.input', side_effect=["Hacer ejercicio", "", "", "Completada"]):
        editar = Editar()
        resultado = editar.editar_tarea()
        assert resultado == "Tarea actualizada con éxito."
        assert db.usuarios_tareas["usuario1"][0]["estado"] == "Completada"


def test_editar_tarea_texto_maximo():
    texto_largo = "A" * 255
    with patch('builtins.input', side_effect=["Hacer ejercicio", texto_largo, "", ""]):
        editar = Editar()
        resultado = editar.editar_tarea()
        assert resultado == "Tarea actualizada con éxito."
        assert db.usuarios_tareas["usuario1"][0]["texto"] == texto_largo


def test_editar_tarea_estado_limite():
    with patch('builtins.input', side_effect=["Hacer ejercicio", "", "", "Pendiente"]):
        editar = Editar()
        resultado = editar.editar_tarea()
        assert resultado == "Tarea actualizada con éxito."
        assert db.usuarios_tareas["usuario1"][0]["estado"] == "Pendiente"


def test_editar_tarea_nueva_categoria():
    with patch('builtins.input', side_effect=["Hacer ejercicio", "", "Placer", ""]):
        editar = Editar()
        resultado = editar.editar_tarea()
        assert resultado == "Tarea actualizada con éxito."
        assert db.usuarios_tareas["usuario1"][0]["categoría"] == "Placer"


def test_editar_tarea_inexistente():
    with patch('builtins.input', side_effect=["Tarea inexistente", "", "", ""]):
        editar = Editar()
        resultado = editar.editar_tarea()
        assert resultado == "La tarea no existe."

def test_editar_tarea_sin_cambios():
    with patch('builtins.input', side_effect=["Hacer ejercicio", "", "", ""]):
        editar = Editar()
        resultado = editar.editar_tarea()
        assert resultado == "Error: No hay cambios registrados"


def test_editar_tarea_cambiando_usuario():
    with patch('builtins.input', side_effect=["Hacer ejercicio", "Nuevo texto", "Nueva categoría", "Nuevo estado"]):
        db.usuario_actual = "usuario2"
        db.usuarios["usuario2"] = {
            "Nombre": "Ana",
            "Apellido": "Prueba",
            "Correo": "usuario2",
            "Contraseña": "123"
        }
        editar = Editar()
        resultado = editar.editar_tarea()
        assert resultado == "La tarea no existe."
