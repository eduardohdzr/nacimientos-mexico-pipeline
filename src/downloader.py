from pathlib import Path
import httpx
from config.settings import CHUNK_SIZE
from src.utils import setup_logger

logger = setup_logger("Downloader")

class FileDownloader:
    """Módulo especializado en descargar archivos a disco."""
    def __init__(self, chunk_size: int = CHUNK_SIZE, verify_ssl: bool = False):
        self.chunk_size = chunk_size
        self.verify_ssl = verify_ssl

    def download(self, url: str, output_path: Path) -> None:
        """Descarga un archivo por bloques (Streaming). Idempotente."""

        #logger.info(f"Verificando existencia de archivos...")
        if not output_path.exists():
            logger.info(f"El archivo '{output_path.name}' no existe. Iniciando descarga.")
            try:
                        with httpx.stream("GET", url, verify=self.verify_ssl, follow_redirects=True, timeout=60.0) as resp:
                            resp.raise_for_status()
                            with open(output_path, "wb") as f:
                                for chunk in resp.iter_bytes(chunk_size=self.chunk_size):
                                    f.write(chunk)
                        logger.info(f"Descarga finalizada: {output_path.name}")
            
            except Exception as e:
                        logger.error(f"Error al descargar {output_path.name}: {e}")
                        if output_path.exists():
                            output_path.unlink()  # Limpiar archivo corrupto si falla
                        raise
        else:
            #logger.info(f"El archivo '{output_path.name}' ya existe. Omitiendo.")
            return