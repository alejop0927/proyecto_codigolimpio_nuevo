import pytest
from src.model.bd_mock.db_global_mock import db_mock
from src.model.bd_mock.base_datos_mock import Base_datos_mock
from unittest.mock import patch
from datetime import datetime

class Crear:
    """
    Clase para crear tareas y almacenarlas en la base de datos mock.
    """

    def __init__(self, nombre, texto, fecha, categoria, estado):
        """
        Inicializa una nueva tarea con los datos proporcionados.

        Parámetros:
            nombre (str): Nombre de la tarea.
            texto (str): Descripción de la tarea.
            fecha (datetime): Fecha de creación de la tarea.
            categoria (str): Categoría de la tarea.
            estado (str): Estado de la tarea.
        """
        self.nombre = nombre
        self.texto = texto
        self.fecha = fecha
        self.categoria = categoria
        self.estado = estado

    def crear_tareas(self):
        """
        Crea una nueva tarea y la almacena en la base de datos mock.

        Retorna:
            str: Mensaje de éxito o error.
        """
        if not self.texto:
            return "Error: El texto no puede estar vacío"
        if not self.categoria:
            return "Error: La categoría es requerida"
        if not self.estado:
            return "Error: El estado es requerido"

        tarea = {
            "nombre": self.nombre,
            "texto": self.texto,
            "fecha": self.fecha,
            "categoria": self.categoria,
            "estado": self.estado
        }

        if db_mock.usuario_actual not in db_mock.usuarios_tareas:
            db_mock.usuarios_tareas[db_mock.usuario_actual] = []

        db_mock.usuarios_tareas[db_mock.usuario_actual].append(tarea)
        return "Tarea creada exitosamente"


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


def crear_tareas(nombre, texto, categoria, estado):
    """
    Función auxiliar para crear tareas.
    """
    tarea = Crear(nombre, texto, "", categoria, estado)
    return tarea.crear_tareas()


def test_crear_tareas_valida_con_categoria():
    """
    Prueba que valida la creación de una tarea con una categoría válida.
    """
    with patch('builtins.input', side_effect=["Comprar leche", "Comprar leche", "Compras", "Por hacer"]):
        tarea = Crear("Comprar leche", "Comprar leche", datetime.now(), "Compras", "Por hacer")
        tarea.crear_tareas()
        assert len(db_mock.usuarios_tareas["usuario1"]) == 1
        assert db_mock.usuarios_tareas["usuario1"][0]["nombre"] == "Comprar leche"


def test_crear_tareas_con_estado_por_hacer():
    """
    Prueba que valida la creación de una tarea con el estado "Por hacer".
    """
    with patch('builtins.input', side_effect=["Ir al gimnasio", "Ir al gimnasio", "Salud", "Por hacer"]):
        tarea = Crear("Ir al gimnasio", "Ir al gimnasio", datetime.now(), "Salud", "Por hacer")
        tarea.crear_tareas()
        assert len(db_mock.usuarios_tareas["usuario1"]) == 1
        assert db_mock.usuarios_tareas["usuario1"][0]["nombre"] == "Ir al gimnasio"


def test_crear_tareas_usuario_registrado():
    """
    Prueba que valida la creación de una tarea cuando el usuario está registrado.
    """
    with patch('builtins.input', side_effect=["Leer libro", "Leer libro", "Lectura", "Por hacer"]):
        tarea = Crear("Leer libro", "Leer libro", datetime.now(), "Lectura", "Por hacer")
        tarea.crear_tareas()
        assert len(db_mock.usuarios_tareas["usuario1"]) == 1
        assert db_mock.usuarios_tareas["usuario1"][0]["nombre"] == "Leer libro"


def test_crear_tareas_texto_largo():
    """
    Prueba que valida la creación de una tarea con un texto largo.
    """
    texto_largo = "A" * 255
    with patch('builtins.input', side_effect=["Tarea larga", texto_largo, "Trabajo", "Por hacer"]):
        tarea = Crear("Tarea larga", texto_largo, datetime.now(), "Trabajo", "Por hacer")
        tarea.crear_tareas()
        assert len(db_mock.usuarios_tareas["usuario1"]) == 1
        assert db_mock.usuarios_tareas["usuario1"][0]["texto"] == texto_largo


def test_crear_tareas_estado_inusual():
    """
    Prueba que valida la creación de una tarea con un estado inusual.
    """
    with patch('builtins.input', side_effect=["Estudiar", "Estudiar", "Estudio", "En pausa"]):
        tarea = Crear("Estudiar", "Estudiar", datetime.now(), "Estudio", "En pausa")
        tarea.crear_tareas()
        assert len(db_mock.usuarios_tareas["usuario1"]) == 1
        assert db_mock.usuarios_tareas["usuario1"][0]["estado"] == "En pausa"


def test_crear_tareas_categoria_desconocida():
    """
    Prueba que valida la creación de una tarea con una categoría desconocida.
    """
    with patch('builtins.input', side_effect=["Viajar", "Viajar", "Otro", "Por hacer"]):
        tarea = Crear("Viajar", "Viajar", datetime.now(), "Otro", "Por hacer")
        tarea.crear_tareas()
        assert len(db_mock.usuarios_tareas["usuario1"]) == 1
        assert db_mock.usuarios_tareas["usuario1"][0]["categoria"] == "Otro"


def test_error_tarea_sin_texto():
    """
    Prueba que valida que se lance un error si el texto de la tarea está vacío.
    """
    with patch('builtins.input', side_effect=["Tarea sin texto", "", "Personal", "Por hacer"]):
        tarea = Crear("Tarea sin texto", "", datetime.now(), "Personal", "Por hacer")
        resultado = tarea.crear_tareas()
        assert resultado == "Error: El texto no puede estar vacío"


def test_error_tarea_sin_categoria():
    """
    Prueba que valida que se lance un error si no se proporciona una categoría.
    """
    with patch('builtins.input', side_effect=["Hacer ejercicio", "Hacer ejercicio", "", "Por hacer"]):
        tarea = Crear("Hacer ejercicio", "Hacer ejercicio", datetime.now(), "", "Por hacer")
        resultado = tarea.crear_tareas()
        assert resultado == "Error: La categoría es requerida"


def test_error_tarea_sin_estado():
    """
    Prueba que valida que se lance un error si no se proporciona un estado.
    """
    with patch('builtins.input', side_effect=["Revisar correo", "Revisar correo", "Trabajo", ""]):
        tarea = Crear("Revisar correo", "Revisar correo", datetime.now(), "Trabajo", "")
        resultado = tarea.crear_tareas()
        assert resultado == "Error: El estado es requerido"
