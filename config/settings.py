import os
from pathlib import Path

# Directorios base
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
BRONZE_DIR = DATA_DIR / "bronze"

# Configuración de la API
API_ENDPOINT = "https://www.datos.gob.mx/api/3/action/package_search"
QUERY = "registro de nacimientos"

# Parámetros de red
HTTP_TIMEOUT = 60.0  # segundos
CHUNK_SIZE = 8192    # 8 KB por bloque para streaming

#Esquema de archivos
first_year = 2013
last_year = 2023
YEARS = tuple(range(first_year, last_year + 1))  # Años de interés: 2013-2023
TOTAL_FILES_EXPECTED = len(YEARS)  # Número total de archivos esperados
FILE_NAME_PATTERN = "nacimientos_*.csv"
FILE_NAME_EXTENSION = ".csv"
