import httpx
import re
from src.utils import setup_logger
from config.settings import HTTP_TIMEOUT
logger = setup_logger("DatasetSearch")

class CKANSearcher:
    """Módulo especializado en buscar paquetes y filtrar URLs objetivo."""

    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint

    def search_datasets(self, query_text: str) -> dict[str, str]:
        """Busca paquetes y extrae los recursos CSV relevantes."""
        params = {"q": query_text}
        logger.info("Consultando metadatos en la API de Datos Abiertos...")

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
                    if 2013 <= year <= 2023 and url.endswith(".csv") and "nacimiento" in name:
                        clean_name = f"{name.strip().replace(' ', '_')}.csv"
                        selected_resources[clean_name] = url

            logger.info(f"Se seleccionaron {len(selected_resources)} datasets de la búsqueda.")
            logger.info(f"Recursos seleccionados:")
            for name in selected_resources:
                logger.info(f" {name}")
            return selected_resources

        except Exception as e:
            logger.error(f"Error al buscar datasets: {e}")
            raise
