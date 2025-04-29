import psycopg2

def obtener_conexion_bd():
 conexion = psycopg2.connect(
    host="localhost",          
    database="proyecto_postgres_codigolimpio",
    user="postgres",
    password="A0927lejop#",
    port=5432                  
 )
 return conexion
