from config.settings import TOTAL_FILES_EXPECTED, CURRENT_FILES
from src.utils import setup_logger
from src.run_bronze import run_bronze_pipeline
from src.transform import extract_bronze_headers, compare_schemas_names


logger = setup_logger("Main")

def main():

    # 1. ORQUESTACIÓN FASE 1 (BRONZE)
    if  CURRENT_FILES < TOTAL_FILES_EXPECTED:
        logger.info(f"Verificando existencia de datasets en el Data Lake Store...")
        logger.info(f"Archivos existentes: {CURRENT_FILES}/{TOTAL_FILES_EXPECTED}")
        run_bronze_pipeline()
    else:
        logger.info("Capa Bronze completa. Saltando búsqueda y descarga.")
        compare_schemas_names(extract_bronze_headers())

        
        
if __name__ == "__main__":
    main()