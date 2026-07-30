# Pipeline de Datos: Nacimientos en México (Mujeres menores de 18 años, 2013–2023)

## 📌 Descripción del Proyecto

Este proyecto implementa un pipeline analítico de datos tipo **ELT** utilizando **Python** y aplicando la **Arquitectura Medallón** (Bronze, Silver y Gold).

El objetivo principal es extraer, transformar y estructurar los registros de nacimientos en adolescentes y niñas (menores de 18 años) reportados durante el periodo 2013–2023 en el portal de **Datos Abiertos del Gobierno de México**. Los datos procesados quedan optimizados para su posterior análisis exploratorio, modelado y visualización.

> 💡 **Evolución del proyecto:** Esta implementación representa la evolución técnica (Ingeniería de Datos) de un análisis exploratorio realizado previamente en Power BI ([ver repositorio original](https://github.com/eduardohdzr/analisis-maternidad-adolescente-mx)).

---

## 📐 Arquitectura del Pipeline

El proyecto implementa un flujo **ELT (Extract, Load, Transform)** estructurado en 3 capas principales para maximizar el rendimiento y la mantenibilidad:

```text
🥉 BRONZE (Ingesta)
 └─ Extracción automatizada y almacenamiento en crudo
       │
       ▼
🥈 SILVER (Limpieza y Tipado)
 └─ Limpieza, validación y estandarización de los datos.
       │
       ▼
🥇 GOLD (Consolidación)
 └─ Consolidación y preparación para análisis/visualización
```
---
## 📂 Estructura del Proyecto

```text
nacimientos-mexico/
├── data/
│   ├── bronze/             # Datasets crudos (CSV) tal como se descargan de la API
│   ├── silver/             # Datasets limpios y filtrados por año (Parquet)
│   └── gold/               # Dataset consolidado final listo para producción
├── config/
│   └── settings.py         # Configuración global (URLs, rutas locales, timeouts)
├── src/
│   ├── dataset_search.py   # Consulta a la API y filtrado dinámico de recursos
│   └── utils.py            # Funciones auxiliares (manejo de logs, métricas, etc.)
├── .gitignore              # Archivos omitidos en Git (data/, .venv/, .env, etc.)
├── main.py                 # Orquestador y punto de entrada del pipeline
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación del proyecto
```
---
## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3.14+
* **Fuente de datos:** API de Datos Abiertos - Gobierno de México
---
## 📝 Licencia
Este proyecto se distribuye bajo la licencia MIT.