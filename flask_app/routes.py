from flask import Blueprint, render_template, request, redirect, url_for, session
from src.model.Usuario import Usuario
from src.model.tarea import Tarea
from src.controller.sistema import Sistema
from src.model.conexion import obtener_conexion_bd  


# --------------------- Registro de Usuario ---------------------
crear_usuario = Blueprint('crear_usuario', __name__)

@crear_usuario.route('/registrar', methods=['GET', 'POST'])
def registrar_usuario():
    """
    Maneja el registro de nuevos usuarios.
    
    GET: Muestra el formulario de registro.
    POST: Procesa los datos del formulario para crear un nuevo usuario.
          Puede recibir datos tanto de formulario como JSON.
          
    Returns:
        Redirección a inicio de sesión si el registro es exitoso,
        o renderiza el template de registro con errores si falla.
    """
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            nombre = data.get('nombre_usuario')
            apellido = data.get('apellido')
            correo = data.get('correo')
            contraseña = data.get('contraseña')
        else:
            nombre = request.form['nombre_usuario']
            apellido = request.form['apellido']
            correo = request.form['correo']
            contraseña = request.form['contraseña']

        try:
            Usuario(nombre, apellido, correo, contraseña)
            conn = obtener_conexion_bd()
            cursor = conn.cursor()
            cursor.execute("SELECT id_usuario FROM usuario WHERE correo = %s;", (correo,))
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()

            if resultado:
                session['id_usuario'] = resultado[0]
                return redirect(url_for('iniciar_sesion.inicio_sesion'))
            else:
                raise Exception("No se pudo recuperar el ID del usuario.")
        except ValueError as ve:
            if request.is_json:
                return {"error": str(ve)}, 400
            return render_template('registro.html', error=str(ve))
        except Exception as e:
            if request.is_json:
                return {"error": "Error en el registro: " + str(e)}, 500
            return render_template('registro.html', error="Error en el registro")
    
    return render_template('registro.html')


# --------------------- Inicio de Sesión ---------------------
iniciar_sesion_usuario = Blueprint('iniciar_sesion', __name__)

@iniciar_sesion_usuario.route('/', methods=['GET', 'POST'])
def inicio_sesion():
    """
    Maneja el inicio de sesión de usuarios.
    
    GET: Muestra el formulario de inicio de sesión.
    POST: Valida las credenciales del usuario e inicia sesión.
          Puede recibir datos tanto de formulario como JSON.
          
    Returns:
        Redirección al dashboard si el inicio de sesión es exitoso,
        o renderiza el template de inicio de sesión con errores si falla.
    """
    sistema = Sistema()
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            correo = data.get('correo')
            contraseña = data.get('contraseña')
        else:
            correo = request.form['correo']
            contraseña = request.form['contraseña']
        
        try:
            mensaje = sistema.iniciar_sesion(correo, contraseña)
            if "Error" in mensaje:
                raise ValueError(mensaje)

            conn = obtener_conexion_bd()
            cursor = conn.cursor()
            cursor.execute("SELECT id_usuario FROM usuario WHERE correo = %s;", (correo,))
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()

            if resultado:
                session['id_usuario'] = resultado[0]
                return redirect(url_for('dashboard.dashboard_view'))
            else:
                raise Exception("No se pudo recuperar el ID del usuario.")
        except ValueError as ve:
            return render_template('iniciar_sesion.html', error=str(ve))
        except Exception as e:
            return render_template('iniciar_sesion.html', error="Error en el inicio de sesión: " + str(e))
    
    return render_template('iniciar_sesion.html')


# --------------------- Cambio de Contraseña ---------------------
cambiar_contraseña = Blueprint('cambiar_contraseña', __name__)

@cambiar_contraseña.route('/cambiar_contraseña', methods=['GET', 'POST'])
def cambiar_contraseña_view():
    """
    Maneja el cambio de contraseña de usuarios.
    
    GET: Muestra el formulario para cambiar contraseña.
    POST: Valida y procesa el cambio de contraseña.
          Puede recibir datos tanto de formulario como JSON.
          
    Returns:
        Redirección a inicio de sesión si el cambio es exitoso,
        o renderiza el template con errores si falla.
    """
    sistema = Sistema()
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            correo = data.get('correo')
            contraseña_actual = data.get('contraseña_actual')
            nueva_contraseña = data.get('nueva_contraseña')
            confirmar_contraseña = data.get('confirmar_contraseña')
        else:
            correo = request.form['correo']
            contraseña_actual = request.form['contraseña_actual']
            nueva_contraseña = request.form['nueva_contraseña']
            confirmar_contraseña = request.form['confirmar_contraseña']
        
        try:
            mensaje = sistema.cambiar_contraseña_usuario(correo, contraseña_actual, nueva_contraseña, confirmar_contraseña)
            if "Error" in mensaje:
                raise ValueError(mensaje)
            if request.is_json:
                return {"mensaje": mensaje}, 200
            return redirect(url_for('iniciar_sesion.inicio_sesion'))
        except ValueError as ve:
            if request.is_json:
                return {"error": str(ve)}, 400
            return render_template('cambiar_contraseña.html', error=str(ve))
        except Exception:
            if request.is_json:
                return {"error": "Error en el cambio de contraseña"}, 500
            return render_template('cambiar_contraseña.html', error="Error en el cambio de contraseña")
    
    return render_template('cambiar_contraseña.html')


# --------------------- Crear Tarea ---------------------
crear_tarea_usuario = Blueprint('crear_tarea', __name__)

@crear_tarea_usuario.route('/crear_tarea', methods=['GET', 'POST'])
def crear_tarea():
    """
    Maneja la creación de nuevas tareas.
    
    GET: Muestra el formulario para crear tareas.
    POST: Procesa los datos para crear una nueva tarea.
          Puede recibir datos tanto de formulario como JSON.
          
    Returns:
        Redirección al dashboard si la creación es exitosa,
        o renderiza el template con errores si falla.
    """
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            nombre_tarea = data.get('nombre_tarea')
            texto_tarea = data.get('texto_tarea')
            categoria = data.get('categoria')
            estado = data.get('estado')
        else:
            nombre_tarea = request.form['nombre_tarea']
            texto_tarea = request.form['texto_tarea']
            categoria = request.form['categoria']
            estado = request.form['estado']

        id_usuario = session.get('id_usuario')  

        try:
            if id_usuario is None:
                raise ValueError("Usuario no autenticado")
            Tarea(id_usuario, nombre_tarea, texto_tarea, categoria, estado)  
            if request.is_json:
                return {"mensaje": "Tarea creada exitosamente"}, 200
            return redirect(url_for('dashboard.dashboard_view'))
        except ValueError as ve:
            if request.is_json:
                return {"error": str(ve)}, 400
            return render_template('crear_tarea.html', error=str(ve))
        except Exception as e:
            if request.is_json:
                return {"error": "Error en la creación de la tarea: " + str(e)}, 500
            return render_template('crear_tarea.html', error="Error en la creación de la tarea")
    
    return render_template('crear_tarea.html')


# --------------------- Editar Tarea ---------------------
editar_tarea_usuario = Blueprint('editar_tarea', __name__)

@editar_tarea_usuario.route('/editar_tarea', methods=['GET', 'POST'])
def editar_tarea():
    """
    Maneja la edición de tareas existentes.
    
    GET: Muestra el formulario para editar tareas.
    POST: Procesa los datos para actualizar una tarea existente.
          Puede recibir datos tanto de formulario como JSON.
          
    Returns:
        Redirección al dashboard si la edición es exitosa,
        o renderiza el template con errores si falla.
    """
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            nombre_tarea = data.get('nombre_tarea')
            nuevo_texto = data.get('nuevo_texto_tarea')
            nueva_categoria = data.get('nueva_categoria')
            nuevo_estado = data.get('nuevo_estado')
        else:
            nombre_tarea = request.form.get('nombre_tarea')
            nuevo_texto = request.form.get('nuevo_texto_tarea')
            nueva_categoria = request.form.get('nueva_categoria')
            nuevo_estado = request.form.get('nuevo_estado')

        usuario_id = session.get('id_usuario')
        if not usuario_id:
            error = "Debes iniciar sesión para editar una tarea"
            if request.is_json:
                return {"error": error}, 401
            return render_template('editar_tarea.html', error=error)

        sistema = Sistema()
        sistema.usuario_actual_id = usuario_id

        resultado = sistema.editar_tarea(nombre_tarea, nuevo_texto, nueva_categoria, nuevo_estado)

        if resultado == "Tarea actualizada correctamente":
            if request.is_json:
                return {"mensaje": resultado}, 200
            return redirect(url_for('dashboard.dashboard_view'))
        else:
            if request.is_json:
                return {"error": resultado}, 400
            return render_template('editar_tarea.html', error=resultado)

    return render_template('editar_tarea.html')


# --------------------- Eliminar Tarea ---------------------
eliminar_tarea_usuario = Blueprint('eliminar_tarea', __name__)

@eliminar_tarea_usuario.route('/eliminar_tarea', methods=['GET', 'POST'])
def eliminar_tarea():
    """
    Maneja la eliminación de tareas existentes.
    
    GET: Muestra el formulario para eliminar tareas.
    POST: Procesa la solicitud para eliminar una tarea.
          Puede recibir datos tanto de formulario como JSON.
          
    Returns:
        Redirección al dashboard si la eliminación es exitosa,
        o renderiza el template con errores si falla.
    """
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            nombre_tarea = data.get('nombre_tarea')
        else:
            nombre_tarea = request.form.get('nombre_tarea')

        usuario_id = session.get('id_usuario')
        if not usuario_id:
            error = "Debes iniciar sesión para eliminar una tarea"
            if request.is_json:
                return {"error": error}, 401
            return render_template('eliminar_tarea.html', error=error)

        sistema = Sistema()
        sistema.usuario_actual_id = usuario_id
        resultado = sistema.eliminar_tarea(nombre_tarea)

        if resultado == "Tarea eliminada correctamente":
            if request.is_json:
                return {"mensaje": resultado}, 200
            return redirect(url_for('dashboard.dashboard_view'))
        else:
            if request.is_json:
                return {"error": resultado}, 400
            return render_template('eliminar_tarea.html', error=resultado)

    return render_template('eliminar_tarea.html')


# --------------------- Mostrar Tareas ---------------------
mostrar_tareas_usuario = Blueprint('mostrar_tareas', __name__)

@mostrar_tareas_usuario.route('/tareas', methods=['GET'])
def tareas():
    """
    Muestra todas las tareas del usuario actual.
    
    GET: Recupera y muestra las tareas del usuario autenticado.
    
    Returns:
        Renderiza el template de tareas con la lista de tareas,
        o un mensaje de error si el usuario no está autenticado o no hay tareas.
    """
    usuario_id = session.get('id_usuario')

    if not usuario_id:
        return render_template('tareas.html', error="Debes iniciar sesión para ver tus tareas", tareas=[])

    sistema = Sistema()
    sistema.usuario_actual_id = usuario_id

    try:
        tareas = sistema.mostrar_tareas_usuario()
    except Exception as e:
        return render_template('tareas.html', error=str(e), tareas=[])

    if isinstance(tareas, str):  # mensaje de error
        return render_template('tareas.html', error=tareas, tareas=[])

    if not tareas:
        return render_template('tareas.html', error="No tienes tareas registradas.", tareas=[])

    # Convertir a diccionario para facilitar uso en el template
    tareas_dict = []
    for tarea in tareas:
        tareas_dict.append({
            'nombre': tarea[0],
            'descripcion': tarea[1],
            'categoria': tarea[2],
            'estado': tarea[3],
            'fecha': tarea[4],
        })

    return render_template('tareas.html', tareas=tareas_dict, error=None)

# --------------------- Logout ---------------------
salir = Blueprint('logout_bp', __name__)

@salir.route('/logout')
def logout():
    """
    Maneja el cierre de sesión del usuario.
    
    Returns:
        Redirección a la página de inicio de sesión.
    """
    session.pop('id_usuario', None)
    return redirect(url_for('iniciar_sesion.inicio_sesion'))


# --------------------- Dashboard ---------------------
dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
def dashboard_view():
    """
    Muestra el dashboard del usuario.
    
    Returns:
        Renderiza el template del dashboard si el usuario está autenticado,
        o redirección a inicio de sesión si no lo está.
    """
    if 'id_usuario' not in session:
        return redirect(url_for('iniciar_sesion.inicio_sesion'))
    return render_template('dashboard.html')