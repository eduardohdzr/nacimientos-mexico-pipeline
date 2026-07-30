import httpx
from src.utils import setup_logger
from config.settings import HTTP_TIMEOUT, CHUNK_SIZE

logger = setup_logger("DatasetSearch")

class CKANSearcher:
    """Módulo especializado en buscar paquetes y filtrar URLs objetivo."""

    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint

    def search_datasets(self) -> dict[str, str]:
        """Busca paquetes y extrae los recursos CSV relevantes."""
        params = {"q": "registro de nacimientos", "rows": 10}
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
                # Regla de selección: Solo archivos CSV que contengan 'nacimientos'
                if url.endswith(".csv") and "nacimiento" in name.lower():
                    clean_name = f"{name.strip().replace(' ', '_')}.csv"
                    selected_resources[clean_name] = url

            logger.info(f"Se seleccionaron {len(selected_resources)} datasets de la búsqueda.")
            logger.info(f"Recursos seleccionados:")
            for name in selected_resources:
                logger.info(f" - {name}")
            return selected_resources

        except Exception as e:
            logger.error(f"Error al buscar datasets: {e}")
            raise

def run_dataset_search(api_endpoint: str):
    """Función de conveniencia para ejecutar la búsqueda de datasets."""
    searcher = CKANSearcher(api_endpoint)
    return searcher.search_datasets()