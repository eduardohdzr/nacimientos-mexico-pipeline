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
│   ├── bronze/                 # Datasets crudos (CSV) tal como se descargan de la API
│   ├── silver/                 # Datasets limpios (Parquet)
│   └── gold/                   # Dataset consolidado final listo para producción
├── config/
│   └── settings.py             # Configuración global (URLs, rutas locales, timeouts, etc)
├── src/
│   ├── __init__.py             # Paquete Python principal
│   ├── bronze/                 # 🥉 Módulos de la CAPA BRONZE (Ingesta)
│   │   ├── __init__.py
│   │   ├── dataset_search.py   # Consulta a la API y filtrado dinámico de recursos
│   │   ├── downloader.py       # Cliente HTTP para la descarga de archivos
│   │   ├── run_bronze.py       # Orquestador del pipeline de la Capa Bronze
│   ├── silver/                 # 🥈 Módulos de la CAPA SILVER (Limpieza y Transformación)
│   │   ├── __init__.py
│   │   ├── transform.py        # Extracción de nombres de columnas de datasets
│   └── utils.py                # Funciones auxiliares (manejo de logs, métricas, etc.)
├── .gitignore                  # Archivos omitidos en Git (data/, .venv/, .env, etc.)
├── main.py                     # Orquestador principal y punto de entrada de la aplicación
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Documentación del proyecto
```
---
## ⚙️ Funcionalidades Desarrolladas
### 🥉 BRONZE

En la **Capa Bronze**, se desarrolló la lógica de ingesta automatizada bajo el **principio de idempotencia**, enfocado en optimizar el uso de red, evitar descargas duplicadas y gestionar de forma eficiente la memoria:

* **🔄 Orquestación e Ingesta Idempotente (`main.py` y `src/run_bronze.py`):**

    * **Evaluación del estado local (`main.py`):** Antes de realizar conexiones o búsquedas en la API, el orquestador escanea el directorio local (`data/bronze/`) para verificar si los conjuntos de datos de los años objetivo (2013–2023) ya existen.

    * **Flujo condicional y toma de decisiones:** 
        * Si **todos** los archivos esperados están presentes, el orquestador omite la ejecución de la Capa Bronze y habilita el paso directo hacia la Capa Silver.

        * Si **faltan** datasets por descargar, `main.py` invoca la ejecución del pipeline de Bronze (`src/run_bronze.py`), el cual calcula exactamente cuántos y cuáles archivos faltan para procesar únicamente los pendientes.

* 🔍 **Búsqueda Dinámica en la API (`src/dataset_search.py`):**

    * **Consulta por catálogo:** Interacción con el endpoint de la API REST de CKAN (`datos.gob.mx`) para consultar recursos de *"registro de nacimientos"*.

    * **Filtrado dinámico:** Mapeo y extracción de URLs de descarga asociadas únicamente a los años pendientes por procesar.

* 📥 **Descarga Eficiente por Streaming (`src/downloader.py`):**

    * **Optimización de memoria I/O:** Procesamiento de descargas por bloques (`httpx.stream` en chunks de 8 KB), para prevenir la saturación de memoria RAM al descargar datasets de gran tamaño.

* 🛠️ **Configuración Centralizada y Trazabilidad (`config/settings.py` y `src/utils.py`):**

   * **Gestión de variables:** Parámetros del proyecto, rutas (`Path`), patrones de archivos y rangos de años centralizados en un solo punto.
   * **Sistema de Logging:** Registro estructurado de eventos a nivel `INFO`, `WARNING` y `ERROR` para facilitar la auditoría y monitoreo de la ejecución.

### Estado de la Ingesta (Capa Bronze)
> **Nota:** La API del portal de Datos Abiertos se encuentra temporalmente fuera de línea por mantenimiento/actualizaciones del portal gubernamental.

---
## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3.14+
* **Fuente de datos:** API de Datos Abiertos - Gobierno de México
---
## 📝 Licencia
Este proyecto se distribuye bajo la licencia MIT.