from src.model.base_datos import Base_datos
class DB:
    def __init__(self):
      self.usuarios={}
      self.tareas={}
      self.usuarios_tareas={}
      self.usuario_actual=None

db = Base_datos()
