import polars as pl
from pathlib import Path
from src.utils import setup_logger
from config.settings import BRONZE_DIR, FILE_NAME_PATTERN

logger = setup_logger("Transformer")

def extract_bronze_headers(input_path: str = BRONZE_DIR):
    """
    Recorre los archivos en la capa Bronze y extrae los nombres de las 
    columnas utilizando Lazy Evaluation para optimizar la memoria.
    """
    path = Path(input_path)
    # Diccionario para almacenar el esquema de cada año [Conversation History]
    schemas = {}

    # Buscamos archivos con el patrón estandarizado en la fase de ingesta
    files = sorted(path.glob(FILE_NAME_PATTERN.format(num="*")), key=lambda x: x.stem)

    if not files:
        logger.info(f"No se encontraron archivos en {input_path}. Asegúrese de que la fase de ingesta se haya completado correctamente.")
        return

    logger.info(f"Iniciando extracción de encabezados en {len(files)} archivos...")

    for file_path in files:
        # Extraemos el año del nombre del archivo (ej. nacimientos_2013.csv)
        year = file_path.stem.split('_')[-1]
        
        try:
            # scan_csv().columns accede solo al encabezado (Lazy Evaluation) [1, 2]
            headers = pl.scan_csv(file_path).collect_schema().names()
            schemas[year] = headers
            #logger.info(f'Nombre del archivo: {file_path.name}')
            #logger.info(schemas)
            logger.info(f"Año {year}: {len(headers)} columnas detectadas.")
            logger.info(f"Encabezados: {headers}")
        except Exception as e:
            logger.error(f"Error al leer {file_path.name}: {e}")

    return schemas

def compare_schemas_names(schemas: dict):
    """
    Compara los nombres de las columnas entre los diferentes años y reporta
    cualquier discrepancia.
    """
    if not schemas:
        logger.info("No hay esquemas para comparar.")
        return

    # Tomamos el primer esquema como referencia
    current_year, reference_headers = next(iter(schemas.items()))
    
    for year, headers in schemas.items():
        if year == current_year:
            continue  # Saltamos la comparación con el mismo año
        
        if set(reference_headers) != set(headers):
            added_cols = set(headers) - set(reference_headers)
            removed_cols = set(reference_headers) - set(headers)
            logger.info(f"Diferencias detectadas entre {current_year} y {year}:")
            logger.info(f"Existen {len(removed_cols)} Columnas en {current_year} pero no en {year}: {removed_cols}")
            logger.info(f"Existen {len(added_cols)} Columnas en {year} pero no en {current_year}: {added_cols}")

            current_year, reference_headers = year, headers

        else:
            logger.info(f"Los encabezados de {current_year} y {year} son iguales.")
