import pytest
from src.model.tarea import Crear
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


def crear_tareas(nombre, texto, categoria, estado):
    tarea = Crear(nombre, texto, "", categoria, estado)
    return tarea.crear_tareas()


def test_crear_tareas_valida_con_categoria():
    with patch('builtins.input', side_effect=["Comprar leche", "Comprar leche", "Compras", "Por hacer"]):
        tarea = Crear("Comprar leche", "Comprar leche", datetime.now(), "Compras", "Por hacer")
        tarea.crear_tareas()
        assert len(db.usuarios_tareas["usuario1"]) == 1
        assert db.usuarios_tareas["usuario1"][0]["nombre"] == "Comprar leche"


def test_crear_tareas_con_estado_por_hacer():
    with patch('builtins.input', side_effect=["Ir al gimnasio", "Ir al gimnasio", "Salud", "Por hacer"]):
        tarea = Crear("Ir al gimnasio", "Ir al gimnasio", datetime.now(), "Salud", "Por hacer")
        tarea.crear_tareas()
        assert len(db.usuarios_tareas["usuario1"]) == 1
        assert db.usuarios_tareas["usuario1"][0]["nombre"] == "Ir al gimnasio"


def test_crear_tareas_usuario_registrado():
    with patch('builtins.input', side_effect=["Leer libro", "Leer libro", "Lectura", "Por hacer"]):
        tarea = Crear("Leer libro", "Leer libro", datetime.now(), "Lectura", "Por hacer")
        tarea.crear_tareas()
        assert len(db.usuarios_tareas["usuario1"]) == 1
        assert db.usuarios_tareas["usuario1"][0]["nombre"] == "Leer libro"


def test_crear_tareas_texto_largo():
    texto_largo = "A" * 255
    with patch('builtins.input', side_effect=["Tarea larga", texto_largo, "Trabajo", "Por hacer"]):
        tarea = Crear("Tarea larga", texto_largo, datetime.now(), "Trabajo", "Por hacer")
        tarea.crear_tareas()
        assert len(db.usuarios_tareas["usuario1"]) == 1
        assert db.usuarios_tareas["usuario1"][0]["texto"] == texto_largo


def test_crear_tareas_estado_inusual():
    with patch('builtins.input', side_effect=["Estudiar", "Estudiar", "Estudio", "En pausa"]):
        tarea = Crear("Estudiar", "Estudiar", datetime.now(), "Estudio", "En pausa")
        tarea.crear_tareas()
        assert len(db.usuarios_tareas["usuario1"]) == 1
        assert db.usuarios_tareas["usuario1"][0]["estado"] == "En pausa"


def test_crear_tareas_categoria_desconocida():
    with patch('builtins.input', side_effect=["Viajar", "Viajar", "Otro", "Por hacer"]):
        tarea = Crear("Viajar", "Viajar", datetime.now(), "Otro", "Por hacer")
        tarea.crear_tareas()
        assert len(db.usuarios_tareas["usuario1"]) == 1
        assert db.usuarios_tareas["usuario1"][0]["categoría"] == "Otro"


def test_error_tarea_sin_texto():
    with patch('builtins.input', side_effect=["Tarea sin texto", "", "Personal", "Por hacer"]):
        tarea = Crear("Tarea sin texto", "", datetime.now(), "Personal", "Por hacer")
        resultado = tarea.crear_tareas()
        assert resultado == "Error: El texto no puede estar vacío"


def test_error_tarea_sin_categoria():
    with patch('builtins.input', side_effect=["Hacer ejercicio", "Hacer ejercicio", "", "Por hacer"]):
        tarea = Crear("Hacer ejercicio", "Hacer ejercicio", datetime.now(), "", "Por hacer")
        resultado = tarea.crear_tareas()
        assert resultado == "Error: La categoría es requerida"


def test_error_tarea_sin_estado():
    with patch('builtins.input', side_effect=["Revisar correo", "Revisar correo", "Trabajo", ""]):
        tarea = Crear("Revisar correo", "Revisar correo", datetime.now(), "Trabajo", "")
        resultado = tarea.crear_tareas()
        assert resultado == "Error: El estado es requerido"

