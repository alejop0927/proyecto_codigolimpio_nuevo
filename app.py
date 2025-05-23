from flask import Flask
from flask_app.routes import (
    crear_usuario,
    iniciar_sesion_usuario,
    cambiar_contraseña,
    crear_tarea_usuario,
    editar_tarea_usuario,
    eliminar_tarea_usuario,
    mostrar_tareas_usuario,
    salir, dashboard
)

app = Flask(
    __name__,
    template_folder='flask_app/templates',
    static_folder='flask_app/static'
)
app.secret_key = 's3cr3t_k3y_1234567890!@#$%^&*()'

# Registrar los blueprints
app.register_blueprint(crear_usuario)
app.register_blueprint(iniciar_sesion_usuario)
app.register_blueprint(cambiar_contraseña)
app.register_blueprint(crear_tarea_usuario)
app.register_blueprint(editar_tarea_usuario)
app.register_blueprint(eliminar_tarea_usuario)
app.register_blueprint(mostrar_tareas_usuario)
app.register_blueprint(salir)
app.register_blueprint(dashboard)

if __name__ == '__main__':
    """
    Punto de entrada principal de la aplicación Flask.
    
    Configura y ejecuta la aplicación web con las siguientes características:
    - Configuración de carpetas para templates y archivos estáticos
    - Clave secreta para manejo de sesiones
    - Registro de todos los blueprints que componen las rutas de la aplicación
    - Ejecución en modo debug cuando se corre directamente
    
    Blueprints registrados:
    - crear_usuario: Manejo de registro de nuevos usuarios
    - iniciar_sesion_usuario: Manejo de inicio de sesión
    - cambiar_contraseña: Manejo de cambio de contraseñas
    - crear_tarea_usuario: Creación de nuevas tareas
    - editar_tarea_usuario: Edición de tareas existentes
    - eliminar_tarea_usuario: Eliminación de tareas
    - mostrar_tareas_usuario: Visualización de tareas
    - salir: Cierre de sesión
    - dashboard: Página principal del usuario autenticado
    
    Ejecución:
    - El servidor se inicia en modo debug cuando el script se ejecuta directamente
    - Escucha en el puerto predeterminado (5000) en localhost
    """
    app.run(debug=True)