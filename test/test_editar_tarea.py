import pytest
from src.model.bd_mock.base_datos_mock import Base_datos_mock
from unittest.mock import patch
from datetime import datetime
class Editar:
    """
    Clase para editar tareas y almacenarlas en la base de datos mock.
    """

    def __init__(self):
        """
        Inicializa la clase Editar con la base de datos mock.
        """
        self.db = db_mock

    def editar_tarea(self, nombre_tarea, nuevo_texto, nueva_categoria, nuevo_estado):
        """
        Permite al usuario editar una tarea existente.

        Parámetros:
            nombre_tarea (str): Nombre de la tarea a editar.
            nuevo_texto (str): Nuevo contenido de la tarea.
            nueva_categoria (str): Nueva categoría de la tarea.
            nuevo_estado (str): Nuevo estado de la tarea.

        Retorna:
            str: Mensaje de éxito o error.
        """
        if self.db.usuario_actual is None:
            return "Debes iniciar sesión"

        tareas_usuario = self.db.usuarios_tareas.get(self.db.usuario_actual, [])
        tarea = next((t for t in tareas_usuario if t["nombre"] == nombre_tarea), None)

        if not tarea:
            return "Tarea no encontrada"

        if not nuevo_texto and not nueva_categoria and not nuevo_estado:
            return "No hay cambios registrados"

        if nuevo_texto:
            tarea["texto"] = nuevo_texto
        if nueva_categoria:
            tarea["categoría"] = nueva_categoria
        if nuevo_estado:
            tarea["estado"] = nuevo_estado

        return "Tarea actualizada correctamente"


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

def test_editar_texto_tarea_existente():
    """
    Prueba la edición del texto de una tarea existente.

    Verifica que al editar una tarea con un texto nuevo, se actualice correctamente en la base de datos.
    """
    with patch('builtins.input', side_effect=["Hacer ejercicio", "Hacer cardio", "", ""]):
        editar = Editar()
        resultado = editar.editar_tarea("Hacer ejercicio", "Hacer cardio", "", "")
        assert resultado == "Tarea actualizada correctamente"
        assert db_mock.usuarios_tareas["usuario1"][0]["texto"] == "Hacer cardio"

def test_editar_categoria_tarea_existente():
    """
    Prueba la edición de la categoría de una tarea existente.

    Verifica que al cambiar la categoría de una tarea existente, se actualice correctamente en la base de datos.
    """
    with patch('builtins.input', side_effect=["Hacer ejercicio", "", "Educación", ""]):
        editar = Editar()
        resultado = editar.editar_tarea("Hacer ejercicio", "", "Educación", "")
        assert resultado == "Tarea actualizada correctamente"
        assert db_mock.usuarios_tareas["usuario1"][0]["categoría"] == "Educación"

def test_editar_estado_tarea_existente():
    """
    Prueba la edición del estado de una tarea existente.

    Verifica que al cambiar el estado de una tarea existente, se actualice correctamente en la base de datos.
    """
    with patch('builtins.input', side_effect=["Hacer ejercicio", "", "", "Completada"]):
        editar = Editar()
        resultado = editar.editar_tarea("Hacer ejercicio", "", "", "Completada")
        assert resultado == "Tarea actualizada correctamente"
        assert db_mock.usuarios_tareas["usuario1"][0]["estado"] == "Completada"

def test_editar_tarea_texto_maximo():
    """
    Prueba la edición del texto de una tarea con el máximo permitido de caracteres.

    Verifica que al actualizar el texto de una tarea con un texto largo, se actualice correctamente en la base de datos.
    """
    texto_largo = "A" * 255
    with patch('builtins.input', side_effect=["Hacer ejercicio", texto_largo, "", ""]):
        editar = Editar()
        resultado = editar.editar_tarea("Hacer ejercicio", texto_largo, "", "")
        assert resultado == "Tarea actualizada correctamente"
        assert db_mock.usuarios_tareas["usuario1"][0]["texto"] == texto_largo

def test_editar_tarea_estado_limite():
    """
    Prueba la edición del estado de una tarea con un estado en el límite permitido.

    Verifica que al actualizar el estado de una tarea con un estado válido, se actualice correctamente en la base de datos.
    """
    with patch('builtins.input', side_effect=["Hacer ejercicio", "", "", "Pendiente"]):
        editar = Editar()
        resultado = editar.editar_tarea("Hacer ejercicio", "", "", "Pendiente")
        assert resultado == "Tarea actualizada correctamente"
        assert db_mock.usuarios_tareas["usuario1"][0]["estado"] == "Pendiente"

def test_editar_tarea_nueva_categoria():
    """
    Prueba la edición de la categoría de una tarea con una nueva categoría.

    Verifica que al actualizar la categoría de una tarea con una nueva categoría válida, se actualice correctamente en la base de datos.
    """
    with patch('builtins.input', side_effect=["Hacer ejercicio", "", "Placer", ""]):
        editar = Editar()
        resultado = editar.editar_tarea("Hacer ejercicio", "", "Placer", "")
        assert resultado == "Tarea actualizada correctamente"
        assert db_mock.usuarios_tareas["usuario1"][0]["categoría"] == "Placer"

def test_editar_tarea_inexistente():
    """
    Prueba la edición de una tarea que no existe.

    Verifica que el sistema devuelva un mensaje adecuado cuando se intenta editar una tarea inexistente.
    """
    with patch('builtins.input', side_effect=["Tarea inexistente", "", "", ""]):
        editar = Editar()
        resultado = editar.editar_tarea("Tarea inexistente", "", "", "")
        assert resultado == "Tarea no encontrada"

def test_editar_tarea_sin_cambios():
    """
    Prueba la edición de una tarea sin realizar cambios.

    Verifica que el sistema devuelva un mensaje adecuado cuando no se registran cambios en la tarea.
    """
    with patch('builtins.input', side_effect=["Hacer ejercicio", "", "", ""]):
        editar = Editar()
        resultado = editar.editar_tarea("Hacer ejercicio", "", "", "")
        assert resultado == "No hay cambios registrados"

def test_editar_tarea_cambiando_usuario():
    """
    Prueba la edición de una tarea cambiando el usuario actual.

    Verifica que el sistema devuelva un mensaje adecuado cuando se intenta editar una tarea de otro usuario.
    """
    with patch('builtins.input', side_effect=["Hacer ejercicio", "Nuevo texto", "Nueva categoría", "Nuevo estado"]):
        db_mock.usuario_actual = "usuario2"
        db_mock.usuarios["usuario2"] = {
            "Nombre": "Ana",
            "Apellido": "Prueba",
            "Correo": "usuario2",
            "Contraseña": "123"
        }
        editar = Editar()
        resultado = editar.editar_tarea("Hacer ejercicio", "Nuevo texto", "Nueva categoría", "Nuevo estado")
        assert resultado == "Tarea no encontrada"
