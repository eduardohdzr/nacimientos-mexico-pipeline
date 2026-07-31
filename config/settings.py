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