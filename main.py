from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from src.model.Usuario import Usuario_kv
from src.model.tarea import Tarea_kv
from src.controller.sistema import Sistema_KV


sistema = Sistema_KV()


class CrearUsuarioScreen(Screen):
    def crear_cuenta_kv(self):
        nombre = self.ids.nombre_input.text
        apellido = self.ids.apellido_input.text
        correo = self.ids.correo_input.text
        contraseña = self.ids.contraseña_input.text

        
        Usuario_kv(nombre, apellido, correo, contraseña, sistema.usuarios)

class CrearTareacreen(Screen):
    def crear_tarea_kv(self):
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




class CambiarContraseñaScreen(Screen):
    def cambiar_contraseña_kv(self):
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



class Inicio_de_sesion(Screen):
    def iniciar_sesion_kv(self):
        correo = self.ids.correo_input.text
        contraseña = self.ids.contraseña_input.text

        resultado = sistema.iniciar_sesion(
            correo=correo,
            contraseña=contraseña
        )
        print(resultado)



class EditarTareaScreen(Screen):
    def editar_tarea_kv(self):
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

class EliminarTareaScreen(Screen):
    def eliminar_tarea_kv(self):
        nombre_tarea = self.ids.nombre_tarea_input.text
        resultado = sistema.eliminar_tarea(
            nombre_tarea=nombre_tarea
        )
        print(resultado)
        
class MostrarTareaScreen(Screen):
    def Mostrar_tareas_usuarios_kv(self):
        sistema.mostrar_tareas_usuario()

class MyApp(App):
    def build(self):
        Builder.load_file("src/view/kv/iniciar_sesion.kv")  
        Builder.load_file("src/view/kv/crear_usuario.kv")
        Builder.load_file("src/view/kv/cambiar_contraseña.kv")
        sm = ScreenManager()
        sm.add_widget(Inicio_de_sesion(name="inicio_sesion"))
        sm.add_widget(CrearUsuarioScreen(name="crear_usuario"))
        sm.add_widget(CambiarContraseñaScreen(name="cambiar_contraseña"))
        sm.add_widget(EditarTareaScreen(name="editar_tarea"))
        return sm


if __name__ == "__main__":
    MyApp().run()
