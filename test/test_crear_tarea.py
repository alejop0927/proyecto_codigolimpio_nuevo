import pytest
from src.controller.sistema import Sistema
from src.model.tarea import Tarea
from unittest.mock import patch

@pytest.fixture(autouse=True)
def limpiar_base_datos():
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
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Comprar leche", "Comprar leche", "Compras", "Por hacer"]):
        Tarea(sistema.usuarios_tareas, sistema.usuario_actual)
        assert len(sistema.usuarios_tareas["usuario1"]) == 1
        assert sistema.usuarios_tareas["usuario1"][0]["nombre"] == "Comprar leche"

def test_crear_tareas_con_estado_por_hacer(limpiar_base_datos):
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Ir al gimnasio", "Ir al gimnasio", "Salud", "Por hacer"]):
        Tarea(sistema.usuarios_tareas, sistema.usuario_actual)
        assert len(sistema.usuarios_tareas["usuario1"]) == 1
        assert sistema.usuarios_tareas["usuario1"][0]["estado"] == "Por hacer"

def test_crear_tareas_usuario_registrado(limpiar_base_datos):
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Leer libro", "Leer libro", "Lectura", "Por hacer"]):
        Tarea(sistema.usuarios_tareas, sistema.usuario_actual)
        assert len(sistema.usuarios_tareas["usuario1"]) == 1

def test_crear_tareas_texto_largo(limpiar_base_datos):
    sistema = limpiar_base_datos
    texto_largo = "A" * 255
    with patch('builtins.input', side_effect=["Tarea larga", texto_largo, "Trabajo", "Por hacer"]):
        Tarea(sistema.usuarios_tareas, sistema.usuario_actual)
        assert sistema.usuarios_tareas["usuario1"][0]["texto"] == texto_largo

def test_crear_tareas_estado_inusual(limpiar_base_datos):
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Estudiar", "Estudiar", "Estudio", "En pausa"]):
        Tarea(sistema.usuarios_tareas, sistema.usuario_actual)
        assert sistema.usuarios_tareas["usuario1"][0]["estado"] == "En pausa"

def test_crear_tareas_categoria_desconocida(limpiar_base_datos):
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Viajar", "Viajar", "Otro", "Por hacer"]):
        Tarea(sistema.usuarios_tareas, sistema.usuario_actual)
        assert sistema.usuarios_tareas["usuario1"][0]["categoría"] == "Otro"

def test_error_tarea_sin_texto(limpiar_base_datos, capfd):
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Tarea sin texto", "", "Personal", "Por hacer"]):
        Tarea(sistema.usuarios_tareas, sistema.usuario_actual)
        out, _ = capfd.readouterr()
        assert "Error: El texto no puede estar vacío" in out
        assert "usuario1" not in sistema.usuarios_tareas or len(sistema.usuarios_tareas["usuario1"]) == 0

def test_error_tarea_sin_categoria(limpiar_base_datos, capfd):
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Hacer ejercicio", "Hacer ejercicio", "", "Por hacer"]):
        Tarea(sistema.usuarios_tareas, sistema.usuario_actual)
        out, _ = capfd.readouterr()
        assert "Error: La categoría es requerida" in out
        assert "usuario1" not in sistema.usuarios_tareas or len(sistema.usuarios_tareas["usuario1"]) == 0

def test_error_tarea_sin_estado(limpiar_base_datos, capfd):
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Revisar correo", "Revisar correo", "Trabajo", ""]):
        Tarea(sistema.usuarios_tareas, sistema.usuario_actual)
        out, _ = capfd.readouterr()
        assert "Error: El estado es requerido" in out
        assert "usuario1" not in sistema.usuarios_tareas or len(sistema.usuarios_tareas["usuario1"]) == 0
