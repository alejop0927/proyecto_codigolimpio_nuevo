from src.model.bd_mock.base_datos_mock import Base_datos_mock
class DB:
    def __init__(self):
      self.usuarios={}
      self.tareas={}
      self.usuarios_tareas={}
      self.usuario_actual=None

db_mock = Base_datos_mock()
