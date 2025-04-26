from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from src.model.Usuario import Usuario
from src.model.tarea import Tarea
from src.controller.sistema import Sistema
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

# Instancia global del sistema
sistema = Sistema()

def salir_app(self):
    """
    Detiene la aplicación Kivy.
    Llama al método stop() de la aplicación Kivy para cerrar la ventana.
    """
    App.get_running_app().stop()

class CrearUsuarioScreen(Screen):
    """
    Pantalla para crear un nuevo usuario.
    Permite ingresar el nombre, apellido, correo y contraseña para crear una nueva cuenta de usuario.
    """
    def crear_cuenta_kv(self):
        """
        Crea una nueva cuenta de usuario utilizando los datos ingresados en la interfaz.
        Recoge los valores de los campos del formulario y los pasa al constructor de la clase Usuario.
        Si los datos son válidos, el usuario se crea correctamente; si no, se muestra un mensaje de error.
        """
        nombre = self.ids.nombre_input.text
        apellido = self.ids.apellido_input.text
        correo = self.ids.correo_input.text
        contraseña = self.ids.contraseña_input.text

        try:
            Usuario(nombre, apellido, correo, contraseña)
            print("Usuario creado con éxito")
            self.manager.current = "inicio_sesion"
        except ValueError as e:
            print(e)

class CrearTareaScreen(Screen):
    """
    Pantalla para crear una nueva tarea.
    Permite ingresar los detalles de una nueva tarea, como nombre, descripción, categoría y estado.
    """
    def crear_tarea_kv(self):
        """
        Crea una nueva tarea utilizando los datos ingresados en la interfaz.
        Los datos del formulario se pasan al constructor de la clase Tarea para crear una tarea.
        Si los datos son válidos, la tarea se crea correctamente; si no, se muestra un mensaje de error.
        """
        nombre_tarea = self.ids.nombre_tarea_input.text
        texto_tarea = self.ids.texto_tarea_input.text
        categoria_tarea = self.ids.categoria_tarea_input.text
        estado_tarea = self.ids.estado_tarea_input.text

        try:
            Tarea(
                sistema.usuario_actual_id,
                nombre_tarea,
                texto_tarea,
                categoria_tarea,
                estado_tarea
            )
            print("Tarea creada con éxito")
            self.manager.current = "dashboard"
        except ValueError as e:
            print(e)

class CambiarContraseñaScreen(Screen):
    """
    Pantalla para cambiar la contraseña de un usuario.
    Permite al usuario cambiar su contraseña proporcionada ingresando su correo, la contraseña actual,
    la nueva contraseña y repitiendo la nueva contraseña.
    """
    def cambiar_contraseña_kv(self):
        """
        Cambia la contraseña de un usuario utilizando los datos ingresados en la interfaz.
        Se valida que la contraseña actual coincida con la registrada y que las contraseñas nuevas sean iguales.
        Si todo es correcto, se actualiza la contraseña y se muestra un mensaje de éxito.
        """
        correo = self.ids.correo_input.text
        contraseña_actual = self.ids.contraseña_actual_input.text
        nueva_contraseña = self.ids.nueva_contraseña_input.text
        repetir_nueva_contraseña = self.ids.repetir_nueva_contraseña_input.text

        resultado = sistema.cambiar_contraseña_usuario(
            correo,
            contraseña_actual,
            nueva_contraseña,
            repetir_nueva_contraseña
        )

        print(resultado)
        if resultado == 'Contraseña actualizada correctamente':
            self.manager.current = "inicio_sesion"

class Inicio_de_sesion(Screen):
    """
    Pantalla para iniciar sesión en la aplicación.
    Permite ingresar el correo y la contraseña para autenticar al usuario.
    """
    def iniciar_sesion_kv(self):
        """
        Inicia sesión utilizando los datos ingresados en la interfaz.
        Recoge el correo y la contraseña, y los pasa al método de iniciar sesión del sistema.
        Si el inicio de sesión es exitoso, el usuario es redirigido al dashboard.
        """
        correo = self.ids.correo_input.text
        contraseña = self.ids.contraseña_input.text

        resultado = sistema.iniciar_sesion(correo, contraseña)
        print(resultado)

        if resultado.startswith("Bienvenido"):
            self.manager.current = "dashboard"
            
    def salir_app(self):
        """
        Detiene la aplicación Kivy.
        Llama al método stop() de la aplicación Kivy para cerrar la ventana.
        """
        App.get_running_app().stop()

class EditarTareaScreen(Screen):
    """
    Pantalla para editar una tarea existente.
    Permite modificar los detalles de una tarea ya creada, como su nombre, descripción, categoría y estado.
    """
    def editar_tarea_kv(self):
        """
        Edita una tarea existente utilizando los datos ingresados en la interfaz.
        Los datos del formulario se pasan al método de editar tarea del sistema.
        Si los datos son válidos, la tarea se edita correctamente.
        """
        nombre_tarea = self.ids.nombre_tarea_input.text
        nuevo_texto = self.ids.nuevo_texto_input.text
        nueva_categoria = self.ids.nueva_categoria_input.text
        nuevo_estado = self.ids.nuevo_estado_input.text

        resultado = sistema.editar_tarea(
            nombre_tarea,
            nuevo_texto,
            nueva_categoria,
            nuevo_estado
        )

        print(resultado)
        self.manager.current = "dashboard"

class EliminarTareaScreen(Screen):
    """
    Pantalla para eliminar una tarea existente.
    Permite al usuario eliminar una tarea ya creada proporcionando el nombre de la tarea.
    """
    def eliminar_tarea_kv(self):
        """
        Elimina una tarea utilizando los datos ingresados en la interfaz.
        Se pasa el nombre de la tarea al método de eliminar tarea del sistema.
        Si la tarea es eliminada correctamente, el sistema lo notifica y se redirige al dashboard.
        """
        nombre_tarea = self.ids.nombre_tarea_input.text
        resultado = sistema.eliminar_tarea(nombre_tarea)
        print(resultado)
        self.manager.current = "dashboard"
        
class MostrarTareaScreen(Screen):
    """
    Pantalla para mostrar las tareas del usuario actual.
    Al entrar en la pantalla, se recuperan todas las tareas del usuario y se muestran en la interfaz.
    """
    def on_enter(self, *args):
        """
        Método que se ejecuta al ingresar a la pantalla. Muestra las tareas del usuario.
        Llama al método de mostrar tareas del sistema para obtener las tareas del usuario actual.
        """
        self.mostrar_tareas_usuario()

    def mostrar_tareas_usuario(self):
        """
        Muestra las tareas del usuario actual.
        Recupera las tareas asociadas al usuario actual desde el sistema y las muestra en la interfaz.
        """
        tareas = sistema.mostrar_tareas_usuario()
        if isinstance(tareas, str):
            print(tareas)
        else:
            tareas_layout = self.ids.tareas_layout
            tareas_layout.clear_widgets()

            for tarea in tareas:
                tarea_box = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
                tarea_box.add_widget(Label(text=f"Nombre: {tarea[0]}"))
                tarea_box.add_widget(Label(text=f"Texto: {tarea[1]}"))
                tarea_box.add_widget(Label(text=f"Fecha: {tarea[4]}"))
                tarea_box.add_widget(Label(text=f"Categoría: {tarea[2]}"))
                tarea_box.add_widget(Label(text=f"Estado: {tarea[3]}"))
                tareas_layout.add_widget(tarea_box)
            
class DashboardScreen(Screen):
    """
    Pantalla principal del usuario.
    Se muestra el panel de control con las opciones disponibles para el usuario después de iniciar sesión.
    """
    def salir_app(self):
        """
        Detiene la aplicación Kivy.
        Llama al método stop() de la aplicación Kivy para cerrar la ventana.
        """
        App.get_running_app().stop()

class MyApp(App):
    """
    Aplicación principal de Kivy.
    Gestor principal que construye la interfaz gráfica de la aplicación y carga todas las pantallas.
    """
    def build(self):
        """
        Construye la interfaz de la aplicación.
        Carga los archivos KV correspondientes y crea el ScreenManager con las pantallas necesarias.
        """
        Builder.load_file("src/view/kv/iniciar_sesion.kv")  
        Builder.load_file("src/view/kv/crear_usuario.kv")
        Builder.load_file("src/view/kv/cambiar_contraseña.kv")
        Builder.load_file("src/view/kv/crear_tarea.kv")
        Builder.load_file("src/view/kv/eliminar_tarea.kv")
        Builder.load_file("src/view/kv/editar_tarea.kv")
        Builder.load_file("src/view/kv/mostrar_tarea.kv")  
        Builder.load_file("src/view/kv/dashboard.kv")
        
        sm = ScreenManager()
        sm.add_widget(Inicio_de_sesion(name="inicio_sesion")) 
        sm.add_widget(CrearUsuarioScreen(name="crear_usuario"))
        sm.add_widget(CambiarContraseñaScreen(name="cambiar_contraseña"))
        sm.add_widget(CrearTareaScreen(name="crear_tarea"))
        sm.add_widget(EliminarTareaScreen(name="eliminar_tarea"))
        sm.add_widget(EditarTareaScreen(name="editar_tarea"))
        sm.add_widget(MostrarTareaScreen(name="mostrar_tarea"))
        sm.add_widget(DashboardScreen(name="dashboard"))  

        return sm

if __name__ == "__main__":
    MyApp().run()
