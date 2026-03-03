import pandas as pd
import numpy as np
from datetime import timedelta

# 1. Configuración Inicial
np.random.seed(42) # Para que los resultados sean reproducibles
num_jugadores = 15
dias_temporada = 240 # Aprox 8 meses
fecha_inicio = pd.to_datetime('2025-09-01')

# Crear el esqueleto del dataset (Producto cartesiano de fechas y jugadores)
fechas = [fecha_inicio + timedelta(days=i) for i in range(dias_temporada)]
jugadores = [f'JUG_{str(i).zfill(2)}' for i in range(1, num_jugadores + 1)]

df = pd.DataFrame(
    [(f, j) for f in fechas for j in jugadores], 
    columns=['Fecha', 'ID_Jugador']
)

# 2. Generación de Variables Base
# Días de partido: Supongamos que juegan Miércoles (2) y Domingos (6)
df['Dia_Semana'] = df['Fecha'].dt.dayofweek
df['Es_Partido'] = df['Dia_Semana'].isin([2, 6]).astype(int)

# Viajes: Solo en días de partido, 50% de probabilidad de jugar fuera (1)
df['Viaje'] = df.apply(lambda row: np.random.choice([0, 1]) if row['Es_Partido'] == 1 else 0, axis=1)

# Minutos y RPE
def simular_actividad(row):
    if row['Es_Partido'] == 1:
        min_partido = np.clip(np.random.normal(15, 10), 0, 40) # Media 20 min, max 40
        min_entreno = 0
        rpe = np.clip(np.random.normal(8, 1.5), 6, 10) # RPE alto en partido
    elif row['Dia_Semana'] == 0: # Lunes descanso
        min_partido = 0
        min_entreno = 0
        rpe = 0
    else:
        min_partido = 0
        min_entreno = np.clip(np.random.normal(90, 20), 45, 120) # Entrenos de 45 a 120 min
        rpe = np.clip(np.random.normal(6, 2.5), 4, 9) # RPE moderado, aunque con mucha variabilidad porque puede haber entrenos muy duros (si son muy largos)
        
    return pd.Series([min_entreno, min_partido, rpe])

df[['Minutos_Entrenamiento', 'Minutos_Partido', 'RPE']] = df.apply(simular_actividad, axis=1)

# Sueño: Afectado por los viajes
df['Horas_Sueño'] = df.apply(
    lambda row: np.clip(np.random.normal(6.0, 1.2), 4, 8) if row['Viaje'] == 1 
    else np.clip(np.random.normal(8.0, 1.0), 5, 10), 
    axis=1
)

# 3. Cálculo de la Carga Diaria
df['Minutos_Totales'] = df['Minutos_Entrenamiento'] + df['Minutos_Partido']
df['Carga_Diaria'] = df['Minutos_Totales'] * df['RPE']

# 4. Lógica de Lesiones 
# Necesitamos iterar por jugador para mantener el estado (si se lesiona, no juega unos días)
datos_finales = []

for jugador in jugadores:
    df_jug = df[df['ID_Jugador'] == jugador].copy()
    df_jug = df_jug.sort_values('Fecha')
    
    # Variables rodantes (Rolling)
    df_jug['Sueño_Medio_3D'] = df_jug['Horas_Sueño'].rolling(window=3, min_periods=1).mean()
    df_jug['Carga_Media_7D'] = df_jug['Carga_Diaria'].rolling(window=7, min_periods=1).mean()
    
    lesion_array = np.zeros(len(df_jug))
    dias_baja = 0
    
    for i in range(len(df_jug)):
        if dias_baja > 0:
            # Si está lesionado, reseteamos su actividad física a 0 ese día
            df_jug.iat[i, df_jug.columns.get_loc('Minutos_Entrenamiento')] = 0
            df_jug.iat[i, df_jug.columns.get_loc('Minutos_Partido')] = 0
            df_jug.iat[i, df_jug.columns.get_loc('RPE')] = 0
            df_jug.iat[i, df_jug.columns.get_loc('Carga_Diaria')] = 0
            df_jug.iat[i, df_jug.columns.get_loc('Minutos_Totales')] = 0
            dias_baja -= 1
            continue
            
        # Calcular probabilidad de lesión hoy
        prob_lesion = 0.01 # Probabilidad base muy baja (0.5%)
        
        # Factor 1: Privación de sueño
        if df_jug.iat[i, df_jug.columns.get_loc('Sueño_Medio_3D')] < 6.5:
            prob_lesion += 0.45 # Sube un 25%
            
        # Factor 2: Pico de carga (Carga de hoy vs media de los últimos 7 días)
        carga_hoy = df_jug.iat[i, df_jug.columns.get_loc('Carga_Diaria')]
        carga_media = df_jug.iat[i, df_jug.columns.get_loc('Carga_Media_7D')]
        
        if carga_media > 0 and (carga_hoy / carga_media) > 1.5:
            prob_lesion += 0.55 # Sube un 35% si la carga de hoy es un 50% mayor a la media aguda
            
        # Lanzar los dados
        if np.random.random() < prob_lesion:
            lesion_array[i] = 1
            dias_baja = np.random.randint(7, 21) # Se pierde entre 1 y 3 semanas
            
    df_jug['Lesion'] = lesion_array
    datos_finales.append(df_jug)

# 5. Unir y Limpiar
df_final = pd.concat(datos_finales)
df_final = df_final.drop(columns=['Dia_Semana', 'Es_Partido', 'Sueño_Medio_3D', 'Carga_Media_7D', 'Minutos_Totales'])

# Redondear para que quede más limpio
df_final[['Minutos_Entrenamiento', 'Minutos_Partido', 'RPE', 'Horas_Sueño', 'Carga_Diaria']] = df_final[['Minutos_Entrenamiento', 'Minutos_Partido', 'RPE', 'Horas_Sueño', 'Carga_Diaria']].round(1)

# Exportar a CSV
df_final.to_csv('datos_baloncesto_simulados.csv', index=False)
print("¡Dataset 'datos_baloncesto_simulados.csv' generado con éxito!")
print(f"Total de lesiones simuladas: {df_final['Lesion'].sum()}")