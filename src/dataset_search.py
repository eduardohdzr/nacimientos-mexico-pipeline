import httpx
import re
from src.utils import setup_logger
from config.settings import HTTP_TIMEOUT, YEARS, FILE_NAME_EXTENSION
logger = setup_logger("DatasetSearch")

class CKANSearcher:
    """Módulo especializado en buscar paquetes y filtrar URLs objetivo."""

    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint

    def search_datasets(self, query_text: str) -> dict[str, str]:
        """Busca paquetes y extrae los recursos CSV relevantes."""
        params = {"q": query_text}
        logger.info(f"Consultando datasets desde {YEARS[0]} a {YEARS[-1]} en la API de Datos Abiertos...")

        try:
            with httpx.Client(timeout=HTTP_TIMEOUT, verify=False) as client:
                response = client.get(self.api_endpoint, params=params)
                response.raise_for_status()
                data = response.json()

            packages = data.get("result", {}).get("results", [])[0].get("resources", [])
            selected_resources = {}

            for pkg in packages:
                url = pkg.get("url", "")
                name = pkg.get("name", "sin_nombre").lower()
                # Regla de selección: Solo archivos CSV que contengan 'nacimientos' dentro del rango 2013 - 2023
                match = re.search(r"(\d{4})", pkg["name"])
                if match:
                    year = int(match.group(1))
                    if year in YEARS and url.endswith(FILE_NAME_EXTENSION) and "nacimiento" in name:
                        clean_name = f"{name.strip().replace(' ', '_')}{FILE_NAME_EXTENSION}"
                        selected_resources[clean_name] = url

            logger.info(f"Se encontraron {len(selected_resources)} datasets de la búsqueda.")
            #logger.info(f"Recursos seleccionados:")
            return selected_resources

        except Exception as e:
            logger.error(f"Error al buscar datasets: {e}")
            raise
