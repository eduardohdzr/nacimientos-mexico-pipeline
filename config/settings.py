import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Definición de Ruta Base del Proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Configuración de Directorios de Datos (Arquitectura Medallón)
DATA_DIR = BASE_DIR / "data"
BRONZE_DIR = DATA_DIR / "bronze"
CONFIG_DIR = BASE_DIR / "config"

# 3. Carga automática del archivo .env desde la raíz del proyecto
load_dotenv(dotenv_path=BASE_DIR / ".env")

# 4. Acceso seguro a credenciales
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 5. Rutas de contratos de datos estáticos
SCHEMA_MAP_PATH = CONFIG_DIR / "schema_map.yaml" # YAML con mapeo de nombres de columnas históricas a nombres canónicos
HISTORIC_DICC_PATH = CONFIG_DIR / "diccionario_historico.csv" # CSV con metadatos descriptivos

# 6. Configuración de la API datos.gob.mx
API_ENDPOINT = "https://www.datos.gob.mx/api/3/action/package_search"
QUERY = "registro de nacimientos"

# 7. Parámetros de red
HTTP_TIMEOUT = 60.0  # segundos
CHUNK_SIZE = 8192    # 8 KB por bloque para streaming

# 8. Esquema de archivos
FILE_NAME_PATTERN = "registro_de_nacimientos_({num}).csv"
FILE_NAME_EXTENSION = ".csv"
first_year = 2013
last_year = 2023
YEARS = tuple(range(first_year, last_year + 1))  # Años de interés: 2013-2023
TOTAL_FILES_EXPECTED = len(YEARS)  # Número total de archivos esperados
CURRENT_FILES = sum(1 for year in YEARS
                    if (BRONZE_DIR / FILE_NAME_PATTERN.format(num=year)).is_file())  # Archivos CSV existentes


# 9. Configuración de API Gemini
GEMINI_MODEL_NAME = "gemini-2.5-flash" #Parámetro de modelo para la API Gemini
PROMPT_SCHEMA_MAPPING = """
Actúa como un Senior Data Engineer. Mapea las siguientes columnas extraídas de datasets históricos
de nacimientos en México hacia variables canónicas en snake_case.

REGLAS ESTRICTAS:
1. Toma obligatoriamente como estándar o nombre de referencia la nomenclatura de variables del periodo 2020 al 2023.
2. Transforma cada variable canónica a snake_case estricto (minúsculas, sin espacios ni caracteres especiales).
3. Agrupa los nombres históricos (2013-2019) bajo su correspondiente clave canónica.

Columnas crudas encontradas:
{input_data}

Descripción histórica de variables y cambios:
{context_data}

Formato de salida obligatorio: Devuelve ÚNICAMENTE un objeto JSON bien formado sin texto adicional, donde la clave sea la variable canónica y el valor sea la lista de alias.
""" # Prompt para la API Gemini que mapea nombres de columnas históricas a nombres canónicos en snake_case.


