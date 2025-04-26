import psycopg2
from src.model.conexion import obtener_conexion_bd

class Usuario:
    """
    Clase para representar a un usuario y encargarse de su registro en la base de datos.
    """

    def __init__(self, nombre_usuario, apellido, correo, contraseña):
        """
        Inicializa un nuevo usuario y lo agrega a la base de datos si los datos son válidos.

        Parámetros:
            nombre_usuario (str): Nombre del usuario (máx. 50 caracteres).
            apellido (str): Apellido del usuario.
            correo (str): Correo electrónico del usuario (único).
            contraseña (str): Contraseña del usuario (entre 8 y 100 caracteres).
        """
        self.conn = obtener_conexion_bd()
        self.cursor = self.conn.cursor()

        if self.usuario_existente(correo):
            raise ValueError("Error: Correo ya registrado")
        
        if not nombre_usuario or len(nombre_usuario) > 50:
            raise ValueError("Error: Nombre demasiado largo o faltante")
        
        if not apellido:
            raise ValueError("Error: Apellido faltante")
        
        if len(contraseña) > 100:
            raise ValueError("Error: Contraseña demasiado larga")
        
        if len(contraseña) < 8:
            raise ValueError("Error: Contraseña demasiado débil")
        
        try:
            self.cursor.execute(
                "INSERT INTO usuario (nombre_usuario, apellido, correo, contraseña) VALUES (%s, %s, %s, %s);",
                (nombre_usuario, apellido, correo, contraseña)
            )
            self.conn.commit()
        except Exception:
            raise Exception("Error de conexión")
        finally:
            self.cursor.close()
            self.conn.close()

    def usuario_existente(self, correo):
        """
        Verifica si el correo ya existe en la base de datos.

        Parámetros:
            correo (str): Correo electrónico a verificar.

        Retorna:
            bool: True si el correo ya está registrado, False en caso contrario.
        """
        self.cursor.execute("SELECT 1 FROM usuario WHERE correo = %s;", (correo,))
        return self.cursor.fetchone() is not None
