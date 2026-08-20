from .mapper_generator import GeminiSchemaMapper
from src.utils import setup_logger

logger = setup_logger("SilverPipeline")

def run_silver_pipeline():
    """
    Función principal para ejecutar la fase Silver del pipeline.
    Esta función orquesta la extracción de nombres de columnas desde los archivos
    de la Capa Bronze y la interacción con la API de Gemini para construir contratos
    de datos.
    """
    logger.info("=== INICIANDO PIPELINE DE TRANSFORMACIÓN SILVER ===")
    
    # Instanciamos el mapeador de esquemas Gemini
    mapper = GeminiSchemaMapper()
    
    # Extraemos los nombres de columnas únicos desde los archivos Bronze
    extracted_columns = mapper.extract_column_names()
    
    if extracted_columns:
        logger.info(f"Encabezados extraídos: {extracted_columns}")
        # Aquí podrías agregar lógica adicional para enviar estos encabezados a Gemini
        # o realizar otras transformaciones según sea necesario.
    else:
        logger.warning("No se extrajeron encabezados. Verifica los archivos en la Capa Bronze.")
    
    logger.info("=== FASE 2 (CAPA SILVER) COMPLETADA CON ÉXITO ===")