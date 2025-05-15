## PROYECTO de Aula de Código Limpio
## Nota importante

### Prueba de interfaces
Para ejecutar el proyecto y ver las interfaces debes de estar en la carpeta inicial de proyecto y correr el siguiente comando

```sh
python main.py
```
Para ejecutar el proyecto y ver la terminal con el menu debes de estar en la carpeta inicial de proyecto y correr el siguiente comando

```sh
python start_menu_consola.py 
```


Esto verificará que corren correctamente las 54 pruebas.

### Pruebas
Para ejecutar las pruebas, debes estar en la carpeta del proyecto y ejecutar el siguiente comando:

```sh
pytest test
```

Esto verificará que corren correctamente las 54 pruebas.



# Pasos para ejecutar el menú del proyecto:
Ubícate en la carpeta del proyecto.

desde alli vas a ejecutar el siguiente comando en la terminal:

```sh
python start_menu_consola.py 
```



Si todo está configurado correctamente, el programa se ejecutará sin problemas. 🚀

## Nota:
Para este proyecto, inicialmente se requiere la implementación de pruebas unitarias que evalúen las diferentes clases vacías. Posteriormente, se implementarán las funcionalidades de la aplicación. A continuación, se presentan los requisitos del sistema.



## Objetivo del Proyecto:
 El objetivo de este proyecto es desarrollar una aplicación para la gestión de tareas personales y profesionales.

## Funcionalidades:

1. Crear una tarea: Permitir a los usuarios crear una tarea en el sistema.

2. Editar una tarea: Permitir a los usuarios editar una tarea existente.

3. Eliminar una tarea: Permitir a los usuarios eliminar una tarea existente.

4. Iniciar sesión: Permitir a los usuarios iniciar sesión con una cuenta existente.

5. Crear cuenta: Permitir a los usuarios registrarse en el sistema.

6. Cambiar contraseña: Permitir a los usuarios cambiar su contraseña cuando lo deseen.

## Datos de una tarea:

Una tarea debe contener los siguientes datos:

* Texto de la tarea.

* Usuario que la creó.

* Fecha de creación.

* Categoría de la tarea.

* Estado de la tarea (Completada, Por hacer, En progreso, etc.).

## Nota:
Cada usuario podrá ver y gestionar solo sus tareas.

## Casos de Prueba

A continuación, se presentan los casos de prueba para cada funcionalidad, cubriendo escenarios normales, extremos y de error.

### Crear una Tarea
| #  | Caso de Prueba                                | Entrada                                     | Resultado esperado                        | Tipo  |
|----|----------------------------------------------|---------------------------------------------|------------------------------------------|------|
| 1  | Crear tarea con texto válido y categoría    | "Comprar leche", Categoría: "Compras"      | Tarea creada correctamente              | Normal    |
| 2  | Crear tarea con estado "Por hacer"          | "Ir al gimnasio", Estado: "Por hacer"      | Tarea creada correctamente              | Normal    |
| 3  | Crear tarea con usuario registrado          | "Leer libro", Usuario: "usuario1"         | Tarea creada correctamente              | Normal    |
| 4  | Crear tarea con texto más largo permitido   | 255 caracteres, Categoría: "Trabajo"       | Tarea creada correctamente              | Extremos    |
| 5  | Crear tarea con estado inusual              | "Estudiar", Estado: "En pausa"            | Tarea creada correctamente              | Extremos    |
| 6  | Crear tarea con categoría desconocida       | "Viajar", Categoría: "Otro"               | Tarea creada correctamente              | Extremos    |
| 7  | Intentar crear tarea sin texto              | "", Categoría: "Personal"                 | Error: El texto no puede estar vacío    | Error    |
| 8  | Intentar crear tarea sin categoría          | "Hacer ejercicio", ""                     | Error: La categoría es requerida        | Error    |
| 9  | Intentar crear tarea sin estado             | "Revisar correo", Categoría: "Trabajo"    | Error: El estado es requerido           | Error    |

### Editar tarea
| #  | Caso de Prueba                              | Entrada                                    | Resultado esperado                        | Tipo  |
|----|--------------------------------------------|--------------------------------------------|------------------------------------------|-------|
| 10 | Editar texto de tarea existente            | "Comprar leche" → "Comprar leche y pan"    | Tarea actualizada correctamente          | Normal    |
| 11 | Editar categoría de tarea existente        | "Ir al gimnasio", Categoría: "Deporte"     | Tarea actualizada correctamente          | Normal    |
| 12 | Editar estado de tarea existente           | "Leer libro", Estado: "Completada"         | Tarea actualizada correctamente          | Normal    |
| 13 | Editar tarea con estado límite válido      | "Estudiar", Estado: "Pendiente"            | Tarea actualizada correctamente          | Extremo   |
| 14 | Editar tarea con nueva categoría válida    | "Viajar", Categoría: "Placer"              | Tarea actualizada correctamente          | Extremo   |
| 15 | Editar tarea con estado inusual            | "Estudiar", Estado: "En pausa"             | Tarea actualizada correctamente          | Extremo   |
| 16 | Intentar editar tarea inexistente          | "Tarea inexistente", ID incorrecto         | Error: Tarea no encontrada               | Error    |
| 17 | Intentar editar tarea sin cambios          | ID válido, Sin modificaciones              | Error: No hay cambios registrados        | Error    |
| 18 | Intentar editar tarea cambiando usuario    | ID válido, Nuevo usuario                   | Error: No se puede cambiar usuario       | Error    |

### Eliminar una Tarea
| #  | Caso de Prueba                                | Entrada             | Resultado esperado                  | Tipo  |
|----|----------------------------------------------|---------------------|------------------------------------|------|
| 19 | Eliminar tarea existente                    | ID de tarea válido  | Tarea eliminada correctamente     | Normal    |
| 20 | Eliminar tarea en estado "Completada"       | ID válido           | Tarea eliminada correctamente     | Normal    |
| 21 | Eliminar tarea en estado "Por hacer"        | ID válido           | Tarea eliminada correctamente     | Normal    |
| 22 | Eliminar tarea con ID límite permitido      | ID más alto permitido | Tarea eliminada correctamente   | Extremo   |
| 23 | Eliminar tarea con muchas ediciones previas | ID válido           | Tarea eliminada correctamente     | Extremo   |
| 24 | Eliminar tarea con usuario con muchas tareas | ID válido           | Tarea eliminada correctamente     | Extremo   |
| 25 | Intentar eliminar tarea inexistente         | ID incorrecto       | Error: La tarea no existe         | Error   |
| 26 | Intentar eliminar tarea sin permisos        | ID de otro usuario  | Error: No tiene permisos          | Error   |
| 27 | Intentar eliminar tarea sin ID              | ""                  | Error: Debe proporcionar un ID    | Error   |

### Iniciar Sesión
| #  | Caso de Prueba                                | Entrada                                    | Resultado esperado                   | Tipo  |
|----|----------------------------------------------|--------------------------------------------|-------------------------------------|------|
| 28 | Usuario inicia sesión correctamente         | usuario@example.com, Contraseña correcta  | Inicio de sesión exitoso           | Normal    |
| 29 | Usuario inicia sesión con mayúsculas        | USUARIO@EXAMPLE.COM, Contraseña correcta  | Inicio de sesión exitoso           | Normal    |
| 30 | Usuario inicia sesión después de cerrar sesión | usuario@example.com, Contraseña correcta | Inicio de sesión exitoso          | Normal    |
| 31 | Usuario inicia sesión con contraseña larga | usuario@example.com, 128 caracteres       | Inicio de sesión exitoso           | Extremo    |
| 32 | Usuario inicia sesión con correo muy largo | 320 caracteres, Contraseña correcta       | Inicio de sesión exitoso           | Extremo    |
| 33 | Usuario inicia sesión con múltiples intentos | usuario@example.com, intentos repetidos   | Inicio de sesión exitoso           | Extremo    |
| 34 | Intentar iniciar sesión con correo incorrecto | usuario@incorrecto.com, Contraseña correcta | Error: Usuario no registrado     | Error    |
| 35 | Intentar iniciar sesión con contraseña incorrecta | usuario@example.com, Contraseña incorrecta | Error: Credenciales incorrectas | Error    |
| 36 | Intentar iniciar sesión con usuario inactivo | usuario@example.com, Contraseña correcta  | Error: Usuario inactivo           | Error    |

### Cambiar Contraseña
| #  | Caso de Prueba                                  | Entrada                                               | Resultado Esperado                   | Tipo   |
|----|----------------------------------------------|------------------------------------------------------|-------------------------------------|--------|
| 37 | Usuario cambia la contraseña con éxito       | usuario@example.com, contraseña_actual, nueva_contraseña | Contraseña cambiada correctamente  | Normal |
| 38 | Usuario cambia la contraseña con mayúsculas  | usuario@example.com, CONTRASEÑA_ACTUAL, NUEVA_CONTRASEÑA | Contraseña cambiada correctamente  | Normal |
| 39 | Usuario cambia la contraseña después de haberla restablecido | usuario@example.com, contraseña_actual, nueva_contraseña | Contraseña cambiada correctamente  | Normal |
| 40 | Usuario intenta cambiar contraseña con clave muy larga | usuario@example.com, contraseña_actual, 320 caracteres | Error: Contraseña demasiado larga | Extremo |
| 41 | Usuario intenta cambiar contraseña varias veces seguidas | usuario@example.com, contraseña_actual, nueva_contraseña repetida varias veces | Contraseña cambiada correctamente  | Extremo |
| 42 | Usuario cambia la contraseña desde otro dispositivo | usuario@example.com, contraseña_actual, nueva_contraseña | Contraseña cambiada correctamente  | Extremo |
| 43 | Intentar cambiar la contraseña con correo incorrecto | usuario@incorrecto.com, contraseña_actual, nueva_contraseña | Error: Usuario no registrado      | Error  |
| 44 | Intentar cambiar la contraseña sin proporcionar correo | "", contraseña_actual, nueva_contraseña | Error: Debe proporcionar un correo | Error  |
| 45 | Intentar cambiar la contraseña de un usuario inactivo | usuario@example.com, contraseña_actual, nueva_contraseña | Error: Usuario inactivo           | Error  |

### Crear Cuenta
| #  | Caso de Prueba                                | Entrada                               | Resultado Esperado                  | Tipo   |
|----|----------------------------------------------|--------------------------------------|-------------------------------------|--------|
| 46 | Usuario crea cuenta correctamente           | Datos válidos                        | Cuenta creada exitosamente         | Normal |
| 47 | Usuario crea cuenta y luego inicia sesión   | Datos válidos, luego login           | Registro e inicio exitoso          | Normal |
| 48 | Usuario crea cuenta con correo alternativo  | Correo válido y diferente            | Cuenta creada exitosamente         | Normal |
| 49 | Usuario crea cuenta con contraseña muy larga | Contraseña > 100 caracteres          | Error: Contraseña demasiado larga  | Extremo |
| 50 | Usuario crea cuenta con nombre muy largo    | Nombre > 50 caracteres               | Error: Nombre demasiado largo      | Extremo |
| 51 | Usuario crea cuenta con conexión inestable  | Internet intermitente                | Error: No se pudo completar el registro | Extremo |
| 52 | Usuario crea cuenta con correo ya registrado | Correo en uso                        | Error: Correo ya registrado        | Error  |
| 53 | Usuario crea cuenta con contraseña débil    | Contraseña insegura                  | Error: Contraseña demasiado débil  | Error  |
| 54 | Usuario crea cuenta con datos incompletos   | Campos vacíos o incompletos          | Error: Datos obligatorios faltantes | Error  |
