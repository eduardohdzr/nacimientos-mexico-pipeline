from config.settings import BRONZE_DIR, TOTAL_FILES_EXPECTED, FILE_NAME_EXTENSION
from src.utils import setup_logger
from src.run_bronze import run_bronze_pipeline


logger = setup_logger("Main")

def main():

    # 1. ORQUESTACIÓN FASE 1 (BRONZE)
    if len(list(BRONZE_DIR.glob(f"*{FILE_NAME_EXTENSION}"))) < TOTAL_FILES_EXPECTED:
        run_bronze_pipeline()
    else:
        logger.info("Capa Bronze completa. Saltando búsqueda y descarga.")
        
        
if __name__ == "__main__":
    main()