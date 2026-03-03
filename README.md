# 🏀 Injury Prediction & Prevention System: Casademont Zaragoza Edition

![Python](https://img.shields.io/badge/Python-3.11-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-elephant)
![Machine Learning](https://img.shields.io/badge/Scikit--Learn-RandomForest-orange)
![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-yellow)
![Status](https://img.shields.io/badge/Status-Completed-green)

> **"El dato más caro en el deporte profesional no es el salario de una estrella: es la lesión."**

## 📖 Descripción del Proyecto
Este proyecto es una solución **End-to-End de Data Science** diseñada para simular el entorno de alto rendimiento de un equipo de baloncesto profesional (basado en Casademont Zaragoza). 

El objetivo principal es **predecir el riesgo de lesión no traumática** (sobrecarga) en los jugadores utilizando datos de carga interna, externa y calidad del sueño. El sistema ingesta datos diarios, calcula métricas fisiológicas complejas en SQL, predice probabilidades con un modelo de Machine Learning y visualiza las alertas en un Dashboard interactivo para el cuerpo técnico.

---

## 🏗️ Arquitectura del Pipeline

El flujo de datos sigue una arquitectura ETL (Extract, Transform, Load) automatizada:

1.  **Generación de Datos (Python):** Script con `Faker` y `Numpy` que simula una temporada completa, introduciendo patrones realistas de carga y fatiga.
2.  **Ingeniería de Datos (PostgreSQL):** * Almacenamiento relacional.
    * Cálculo de métricas avanzadas mediante **Vistas SQL** y **Window Functions**:
        * *Carga Aguda* (Media móvil 7 días).
        * *Carga Crónica* (Media móvil 28 días).
        * **ACWR (Acute:Chronic Workload Ratio):** La métrica estándar de oro para medir el riesgo de lesión.
3.  **Machine Learning (Scikit-Learn):** Modelo de clasificación (Random Forest) para predecir la probabilidad de lesión.
4.  **Visualización (Power BI):** Dashboard de toma de decisiones en tiempo real.

---

## 🧠 El Desafío de ML: Superando la "Trampa de la Precisión"

Uno de los mayores retos técnicos fue el **desbalanceo de clases**. En el deporte, las lesiones son eventos raros (aprox. 0.5% de los días), lo que llevó a un primer modelo fallido.

### 📉 Evolución del Modelo

| Fase | Modelo | Accuracy | Recall (Sensibilidad) | Diagnóstico |
| :--- | :--- | :--- | :--- | :--- |
| **1** | Random Forest Base | 98% | **0.00** | *Modelo inútil.* Predecía que nadie se lesionaba nunca para maximizar la precisión. |
| **2** | Feature Engineering | 97% | **0.13** | Se inyectaron penalizaciones por sueño (<6.5h) y picos de carga (ACWR > 1.5). |
| **3** | **GridSearch + Class Weights** | 87% | **0.26** | Se penalizó el error en lesiones (ratio 1:20) frente a jugadores sanos. |
| **4** | **Threshold Moving** (Final) | **60%** | **0.74** | **ÉXITO.** Se ajustó el umbral de decisión probabilístico. |

> **Resultado Final:** El modelo sacrifica precisión (falsas alarmas) para lograr un **Recall del 74%**. Esto significa que **detectamos 3 de cada 4 lesiones potenciales**, priorizando la salud del jugador sobre la estadística pura.

---

## 📊 Dashboard Interactivo (Power BI)

El resultado final no es un código, es una herramienta para el entrenador.

![vista-general](https://github.com/Nachoide100/Analisis-Lesiones/blob/a7888a30e0d4be10f260f2a3bf42796ab31c6b46/visualizations/Captura%20de%20pantalla%202026-03-03%20173436.png)

### Funcionalidades Clave:
* **Semáforo de Riesgo:** Alertas visuales (Rojo/Verde) basadas en la probabilidad predicha.
* **Control de ACWR:** Gráfico de "Río Verde" (Zona segura entre 0.8 y 1.3) vs. Picos de peligro.
* **Drill-Through:** Navegación desde la vista de equipo al detalle individual del jugador.
* **Modo Oscuro:** Diseño UI optimizado para reducir fatiga visual en entornos de análisis deportivo.

![drillthough](https://github.com/Nachoide100/Analisis-Lesiones/blob/a7888a30e0d4be10f260f2a3bf42796ab31c6b46/visualizations/Captura%20de%20pantalla%202026-03-03%20174510.png)

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.10+
* **Librerías:** Pandas, SQLAlchemy, Scikit-learn, Numpy, Faker, Psycopg2.
* **Base de Datos:** PostgreSQL (Uso intensivo de Vistas y Window Functions).
* **BI:** Microsoft Power BI (DAX para medidas dinámicas y modelado de datos).
* **IDE:** Visual Studio Code.

---

## 🚀 Cómo ejecutar el proyecto

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/injury-prevention-analytics.git](https://github.com/tu-usuario/injury-prevention-analytics.git)
    ```
2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configurar Base de Datos:**
    * Asegúrate de tener PostgreSQL corriendo.
    * Modifica `database.py` con tus credenciales.
4.  **Ejecutar el Pipeline:**
    ```bash
    python main.py
    ```
    *(Esto generará los datos, los subirá a SQL, entrenará el modelo y exportará el CSV final).*

---

## 📩 Contacto

Si te interesa el Sports Analytics, la Ciencia de Datos aplicada o quieres discutir sobre métricas de carga interna, ¡hablemos!

* **LinkedIn:** [Nacho Rubio](https://www.linkedin.com/in/jose-ignacio-rubio-194471308/)
* **Email:** rongenrola111@gmail.com

