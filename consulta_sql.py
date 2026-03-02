import pandas as pd
from sqlalchemy import create_engine

# 1. Creamos la misma conexión a tu base de datos que el Día 2
cadena_conexion = "postgresql://postgres:Nacho6150&@localhost:5432/baloncesto_db"
engine = create_engine(cadena_conexion)

# 2. Guardamos tu consulta SQL (ya corregida) en una variable de texto
# Usamos triple comilla (""") para poder escribir en varias líneas
consulta_sql = """
    SELECT 
        rd."ID_Jugador", 
        rd."Fecha", 
        rd."Lesion",
        ac.carga_aguda, 
        ac.carga_cronica, 
        ac.acwr,
        ds.media_sueno_3d, 
        ds.es_visitante, 
        ds.alerta_sueno
    FROM registro_diario rd
    JOIN vw_acwr ac 
        ON rd."ID_Jugador" = ac."ID_Jugador" AND rd."Fecha" = ac."Fecha"
    JOIN deuda_sueno ds 
        ON rd."ID_Jugador" = ds."ID_Jugador" AND rd."Fecha" = ds."Fecha"
    ORDER BY rd."Fecha", rd."ID_Jugador";
"""

# 3. ¡La Magia! Ejecutamos la consulta y la metemos en un DataFrame
print("Extrayendo datos de PostgreSQL...")
df_ml = pd.read_sql_query(consulta_sql, engine)

print(f"¡Dataset listo! Filas extraídas: {len(df_ml)}")
print(df_ml.head())