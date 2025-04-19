from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from src.model.Usuario import Usuario_kv
from src.model.tarea import Tarea_kv
from src.controller.sistema import Sistema_KV
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

sistema = Sistema_KV()

def salir_app(self):
    """
    Detiene la aplicación Kivy.
    """
    App.get_running_app().stop()

class CrearUsuarioScreen(Screen):
    """
    Pantalla para crear un nuevo usuario.
    """
    def crear_cuenta_kv(self):
        """
        Crea una nueva cuenta de usuario utilizando los datos ingresados en la interfaz.
        """
        nombre = self.ids.nombre_input.text
        apellido = self.ids.apellido_input.text
        correo = self.ids.correo_input.text
        contraseña = self.ids.contraseña_input.text

        Usuario_kv(nombre, apellido, correo, contraseña, sistema.usuarios)
        print("Usuario creado con éxito")
        self.manager.current = "inicio_sesion"

class CrearTareaScreen(Screen):
    """
    Pantalla para crear una nueva tarea.
    """
    def crear_tarea_kv(self):
        """
        Crea una nueva tarea utilizando los datos ingresados en la interfaz.
        """
        nombre_tarea = self.ids.nombre_tarea_input.text
        texto_tarea = self.ids.texto_tarea_input.text
        categoria_tarea = self.ids.categoria_tarea_input.text
        estado_tarea = self.ids.estado_tarea_input.text

        Tarea_kv(
            nombre_tarea=nombre_tarea,
            texto_tarea=texto_tarea,
            categoria_tarea=categoria_tarea,
            estado_tarea=estado_tarea,
            usuarios_tareas=sistema.usuarios_tareas,
            usuario_actual=sistema.usuario_actual
        )
        self.manager.current = "dashboard"

class CambiarContraseñaScreen(Screen):
    """
    Pantalla para cambiar la contraseña de un usuario.
    """
    def cambiar_contraseña_kv(self):
        """
        Cambia la contraseña de un usuario utilizando los datos ingresados en la interfaz.
        """
        correo = self.ids.correo_input.text
        contraseña_actual = self.ids.contraseña_actual_input.text
        nueva_contraseña = self.ids.nueva_contraseña_input.text
        repetir_nueva_contraseña = self.ids.repetir_nueva_contraseña_input.text

        resultado = sistema.cambiar_contraseña_usuario(
            correo=correo,
            contraseña_actual=contraseña_actual,
            nueva_contraseña=nueva_contraseña,
            confirmar_contraseña=repetir_nueva_contraseña
        )

        print(resultado)
        if resultado == 'Contraseña actualizada con éxito':
            self.manager.current = "inicio_sesion"

class Inicio_de_sesion(Screen):
    """
    Pantalla para iniciar sesión en la aplicación.
    """
    def iniciar_sesion_kv(self):
        """
        Inicia sesión utilizando los datos ingresados en la interfaz.
        """
        correo = self.ids.correo_input.text
        contraseña = self.ids.contraseña_input.text

        resultado = sistema.iniciar_sesion(correo, contraseña)
        print(resultado)

        if resultado.startswith("Bienvenido"):
            nombre_usuario = sistema.usuarios[sistema.usuario_actual]["Nombre"]
            mensaje_bienvenida = f"Bienvenido {nombre_usuario}"
            print(mensaje_bienvenida)
            self.manager.current = "dashboard"
            
    def salir_app():
        """
        Detiene la aplicación Kivy.
        """
        App.get_running_app().stop()

class EditarTareaScreen(Screen):
    """
    Pantalla para editar una tarea existente.
    """
    def editar_tarea_kv(self):
        """
        Edita una tarea utilizando los datos ingresados en la interfaz.
        """
        nombre_tarea = self.ids.nombre_tarea_input.text
        nuevo_texto = self.ids.nuevo_texto_input.text
        nueva_categoria = self.ids.nueva_categoria_input.text
        nuevo_estado = self.ids.nuevo_estado_input.text

        resultado = sistema.editar_tarea(
            nombre_tarea=nombre_tarea,
            nuevo_texto=nuevo_texto,
            nueva_categoria=nueva_categoria,
            nuevo_estado=nuevo_estado
        )

        print(resultado)
        self.manager.current = "dashboard"

class EliminarTareaScreen(Screen):
    """
    Pantalla para eliminar una tarea existente.
    """
    def eliminar_tarea_kv(self):
        """
        Elimina una tarea utilizando los datos ingresados en la interfaz.
        """
        nombre_tarea = self.ids.nombre_tarea_input.text
        resultado = sistema.eliminar_tarea(
            nombre_tarea=nombre_tarea
        )
        print(resultado)
        self.manager.current = "dashboard"
        
class MostrarTareaScreen(Screen):
    """
    Pantalla para mostrar las tareas del usuario actual.
    """
    def on_enter(self, *args):
        """
        Método que se ejecuta al entrar en la pantalla. Muestra las tareas del usuario.
        """
        self.mostrar_tareas_usuario()

    def mostrar_tareas_usuario(self):
        """
        Muestra las tareas del usuario actual.
        """
        correo = sistema.usuario_actual
        if correo is None:
            print("No hay usuario logueado.")
            return

        tareas = sistema.usuarios_tareas.get(correo, [])
        if not tareas:
            print("No tienes tareas.")
            return

        tareas_layout = self.ids.tareas_layout
        tareas_layout.clear_widgets()

        for tarea in tareas:
            tarea_box = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
            tarea_box.add_widget(Label(text=f"Nombre: {tarea['nombre']}"))
            tarea_box.add_widget(Label(text=f"Texto: {tarea['texto']}"))
            tarea_box.add_widget(Label(text=f"Fecha: {tarea['fecha']}"))
            tarea_box.add_widget(Label(text=f"Categoría: {tarea['categoría']}"))
            tarea_box.add_widget(Label(text=f"Estado: {tarea['estado']}"))
            tareas_layout.add_widget(tarea_box)
            
class DashboardScreen(Screen):
    """
    Pantalla principal del usuario.
    """
    def salir_app():
        """
        Detiene la aplicación Kivy.
        """
        App.get_running_app().stop()

class MyApp(App):
    """
    Aplicación principal de Kivy.
    """
    def build(self):
        """
        Construye la interfaz de la aplicación.
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

