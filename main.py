from pathlib import Path
from config.settings import API_ENDPOINT, QUERY
from src.dataset_search import CKANSearcher
from src.downloader import FileDownloader
from src.utils import setup_logger
logger = setup_logger("BronzePipeline")

BRONZE_DIR = Path("data/bronze")

def run_bronze_pipeline():
    BRONZE_DIR.mkdir(parents=True, exist_ok=True)

    # Paso 1: Buscar y seleccionar
    searcher = CKANSearcher(API_ENDPOINT)
    target_files = searcher.search_datasets(QUERY)

    # Paso 2: Descargar los seleccionados
    downloader = FileDownloader(verify_ssl=False)
    for file_name, url in target_files.items():
        destination = BRONZE_DIR / file_name
        downloader.download(url=url, output_path=destination)

    logger.info("=== FASE 1 (CAPA BRONZE) COMPLETADA CON ÉXITO ===")

if __name__ == "__main__":
    logger.info("=== INICIANDO PIPELINE DE DESCARGA DE DATOS BRONZE ===")
    run_bronze_pipeline()