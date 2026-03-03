import pandas as pd
from sqlalchemy import create_engine, text

# 1. Configurar las credenciales de PostgreSQL
USUARIO = 'postgres'          
CONTRASENA = 'Nacho6150&'  
HOST = 'localhost'            
PUERTO = '5432'               
BASE_DATOS = 'baloncesto_db'  

# 2. Crear el "Motor" de conexión (Engine)

cadena_conexion = f"postgresql://{USUARIO}:{CONTRASENA}@{HOST}:{PUERTO}/{BASE_DATOS}"
engine = create_engine(cadena_conexion)

# 3. Cargar y preparar los datos del Día 1
print("Cargando el CSV...")
df = pd.read_csv('datos_baloncesto_simulados.csv')

# Castear la columna fecha para asegurarnos el tipo de dato
df['Fecha'] = pd.to_datetime(df['Fecha'])

# 4. Ingesta de datos en PostgreSQL
nombre_tabla = 'registro_diario'
print(f"Subiendo datos a la tabla '{nombre_tabla}' en PostgreSQL...")

# PASO 1: Vaciamos la tabla antigua (sin romper las vistas)
# Usamos una conexión directa para ejecutar SQL puro
with engine.connect() as conn:
    # TRUNCATE es mucho más rápido que DELETE y respeta la estructura
    print("Vaciando datos antiguos...")
    conn.execute(text(f"TRUNCATE TABLE {nombre_tabla} RESTART IDENTITY;"))
    conn.commit() # Confirmamos la acción

# PASO 2: Llenamos con los datos nuevos
# OJO: Cambiamos 'replace' por 'append' porque la tabla ya existe (vacía)
df.to_sql(nombre_tabla, engine, if_exists='append', index=False)

print("¡Ingesta completada con éxito! Las vistas se han actualizado automáticamente.")