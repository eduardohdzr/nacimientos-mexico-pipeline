import os
from pathlib import Path

# Directorios base
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
BRONZE_DIR = DATA_DIR / "bronze"

# Configuración de la API
# URL base o endpoint CKAN de datos.gob.mx
API_ENDPOINT = "https://www.datos.gob.mx/api/3/action/package_search"
#params = {'q':'registro de nacimientos'}
# Parámetros de red
HTTP_TIMEOUT = 60.0  # segundos
CHUNK_SIZE = 8192    # 8 KB por bloque para streaming

# Configuración de SSL (True por defecto, permite cambiar mediante variables de entorno)
#VERIFY_SSL = os.getenv("VERIFY_SSL", "False").lower() in ("true", "1", "t")