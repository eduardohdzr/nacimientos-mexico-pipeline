from config.settings import API_ENDPOINT, QUERY, BRONZE_DIR
from src.dataset_search import CKANSearcher
from src.downloader import FileDownloader

from src.utils import setup_logger
logger = setup_logger("BronzePipeline")


def run_bronze_pipeline():
    logger.info("=== INICIANDO PIPELINE DE DESCARGA DE DATOS BRONZE ===")
    BRONZE_DIR.mkdir(parents=True, exist_ok=True)

    # Paso 1: Buscar y seleccionar
    searcher = CKANSearcher(API_ENDPOINT)
    target_files = searcher.search_datasets(QUERY)

    # Paso 2: Descargar los seleccionados
    downloader = FileDownloader(verify_ssl=False)
    logger.info(f"Verificando existencia de archivos...")
    for file_name, url in target_files.items():
        destination = BRONZE_DIR / file_name
        downloader.download(url=url, output_path=destination)

    logger.info("=== FASE 1 (CAPA BRONZE) COMPLETADA CON ÉXITO ===")