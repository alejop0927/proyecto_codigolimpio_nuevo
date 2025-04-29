CREATE DATABASE Proyecto_postgres_codigolimpio;



CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(150) NOT NULL,
    apellido VARCHAR(250) NULL,
    correo VARCHAR(250) NOT NULL,
    contraseña VARCHAR(250) NOT NULL
);

CREATE TABLE Tarea (
    id_tarea SERIAL PRIMARY KEY,
    nombre_tarea VARCHAR(250) NULL,
    texto_tarea VARCHAR(250) NULL,
    fecha_creacion TIMESTAMP, 
    categoria VARCHAR(150) NULL,
    estado VARCHAR(100) NULL
);

CREATE TABLE Tarea_usuario (
    id_tareausu SERIAL PRIMARY KEY,
    id_usuario INT,
    id_tarea INT,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_tarea) REFERENCES Tarea(id_tarea)
);

INSERT INTO usuario (nombre_usuario, apellido, correo, contraseña, activo) VALUES
('Laura', 'Gómez', 'laura.gomez@email.com', 'pass123', true),
('Carlos', 'Ramírez', 'carlos.ramirez@email.com', 'qwerty', true),
('Ana', 'Martínez', 'ana.martinez@email.com', 'abc123', false),
('Pedro', 'López', 'pedro.lopez@email.com', 'password', true),
('Lucía', 'Hernández', 'lucia.hernandez@email.com', 'lucia2023', true);

INSERT INTO tarea (nombre_tarea, texto_tarea, fecha_creacion, categoria, estado) VALUES
('Informe mensual', 'Redactar el informe del mes', '2024-09-01 10:00:00', 'Reportes', 'pendiente'),
('Actualizar sistema', 'Instalar actualizaciones de seguridad', '2024-09-02 14:00:00', 'TI', 'en progreso'),
('Reunión equipo', 'Planificación mensual del equipo', '2024-09-03 09:00:00', 'Reuniones', 'pendiente'),
('Diseño campaña', 'Crear diseño gráfico para campaña', '2024-09-04 11:30:00', 'Marketing', 'completada'),
('Validar encuestas', 'Revisar resultados de encuestas', '2024-09-05 16:00:00', 'Investigación', 'pendiente');

INSERT INTO tarea_usuario (id_usuario, id_tarea) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(1, 2),  
(2, 3);  

