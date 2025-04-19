import pytest
from src.controller.sistema import Sistema
from unittest.mock import patch
from datetime import datetime

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

def test_editar_texto_tarea_existente(limpiar_base_datos):
    """
    Prueba que edita el texto de una tarea existente.
    Verifica que el texto de la tarea se actualice correctamente.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Hacer ejercicio", "Hacer cardio", "", ""]):
        resultado = sistema.editar_tarea()
        assert resultado == "Tarea actualizada con éxito."
        assert sistema.usuarios_tareas["usuario1"][0]["texto"] == "Hacer cardio"

def test_editar_categoria_tarea_existente(limpiar_base_datos):
    """
    Prueba que edita la categoría de una tarea existente.
    Verifica que la categoría de la tarea se actualice correctamente.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Hacer ejercicio", "", "Educación", ""]):
        resultado = sistema.editar_tarea()
        assert resultado == "Tarea actualizada con éxito."
        assert sistema.usuarios_tareas["usuario1"][0]["categoría"] == "Educación"

def test_editar_estado_tarea_existente(limpiar_base_datos):
    """
    Prueba que edita el estado de una tarea existente.
    Verifica que el estado de la tarea se actualice correctamente.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Hacer ejercicio", "", "", "Completada"]):
        resultado = sistema.editar_tarea()
        assert resultado == "Tarea actualizada con éxito."
        assert sistema.usuarios_tareas["usuario1"][0]["estado"] == "Completada"

def test_editar_tarea_texto_maximo(limpiar_base_datos):
    """
    Prueba que edita el texto de una tarea con un texto largo (máximo 255 caracteres).
    Verifica que el texto de la tarea se actualice correctamente.
    """
    sistema = limpiar_base_datos
    texto_largo = "A" * 255
    with patch('builtins.input', side_effect=["Hacer ejercicio", texto_largo, "", ""]):
        resultado = sistema.editar_tarea()
        assert resultado == "Tarea actualizada con éxito."
        assert sistema.usuarios_tareas["usuario1"][0]["texto"] == texto_largo

def test_editar_tarea_estado_limite(limpiar_base_datos):
    """
    Prueba que edita el estado de una tarea existente con el valor 'Pendiente'.
    Verifica que el estado de la tarea se actualice correctamente.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Hacer ejercicio", "", "", "Pendiente"]):
        resultado = sistema.editar_tarea()
        assert resultado == "Tarea actualizada con éxito."
        assert sistema.usuarios_tareas["usuario1"][0]["estado"] == "Pendiente"

def test_editar_tarea_nueva_categoria(limpiar_base_datos):
    """
    Prueba que edita la categoría de una tarea existente.
    Verifica que la categoría de la tarea se actualice correctamente con un valor nuevo.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Hacer ejercicio", "", "Placer", ""]):
        resultado = sistema.editar_tarea()
        assert resultado == "Tarea actualizada con éxito."
        assert sistema.usuarios_tareas["usuario1"][0]["categoría"] == "Placer"

def test_editar_tarea_inexistente(limpiar_base_datos):
    """
    Prueba que intenta editar una tarea inexistente.
    Verifica que se reciba un mensaje de error adecuado.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Tarea inexistente", "", "", ""]):
        resultado = sistema.editar_tarea()
        assert resultado == "La tarea no existe."

def test_editar_tarea_sin_cambios(limpiar_base_datos):
    """
    Prueba que intenta editar una tarea sin realizar cambios.
    Verifica que se reciba un mensaje de error adecuado.
    """
    sistema = limpiar_base_datos
    with patch('builtins.input', side_effect=["Hacer ejercicio", "", "", ""]):
        resultado = sistema.editar_tarea()
        assert resultado == "Error: No hay cambios registrados"

def test_editar_tarea_cambiando_usuario(limpiar_base_datos):
    """
    Prueba que intenta editar una tarea con un usuario diferente.
    Verifica que se reciba un mensaje de error indicando que la tarea no existe para ese usuario.
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
    with patch('builtins.input', side_effect=["Hacer ejercicio", "Nuevo texto", "Nueva categoría", "Nuevo estado"]):
        resultado = sistema.editar_tarea()
        assert resultado == "La tarea no existe."
