import polars as pl
from pathlib import Path
from src.utils import setup_logger
import config.settings as settings
import itertools
import json
import yaml
from google import genai
from google.genai import types

logger = setup_logger("GeminiSchemaMapper")

class GeminiSchemaMapper:
    """ Clase encargada de interactuar con la API de Gemini para construir y 
    actualizar contratos de datos (mapeo de nombres de columnas y estandarización 
    de valores categóricos) a partir de los datos crudos de la Capa Bronze."""
     
     
    def __init__(self, bronze_dir: Path = settings.BRONZE_DIR, model_name: str = settings.GEMINI_MODEL_NAME):
        self.bronze_dir = Path(bronze_dir)
        self.model_name = model_name
        #self.client = genai.Client() [8]

    def extract_column_names(self) -> list[str]:
            """
            Extrae el universo de columnas únicas encontradas en los CSVs de Bronze
            utilizando evaluación perezosa (Lazy Evaluation) para optimizar memoria.
            """
            names = []
            files = sorted(self.bronze_dir.glob(settings.FILE_NAME_PATTERN.format(num="*")), key=lambda x: x.stem)

            if not files:
                logger.info(f"No se encontraron archivos en {self.bronze_dir}." "Asegúrese de que la fase de ingesta se haya completado correctamente."
                )
                return []

            logger.info(f"Iniciando extracción de encabezados en {len(files)} archivos...")

            for file_path in files:
                try:
                    # scan_csv().collect_schema().names() accede solo al encabezado (Lazy Evaluation)
                    headers = pl.scan_csv(file_path).collect_schema().names()
                    names.append(headers)
                except Exception as e:
                    logger.error(f"Error al leer {file_path.name}: {e}")

            # Aplanamos la lista de listas de manera eficiente y deduplicamos
            list_names = list(itertools.chain.from_iterable(names))
            unique_names = list(set(list_names))

            logger.info(f"Cantidad de encabezados extraídos (totales): {len(list_names)}")
            logger.info(f"Cantidad de encabezados únicos: {len(unique_names)}")
            
            return unique_names