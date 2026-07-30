from config.settings import API_ENDPOINT
#from src.api_client import run_bronze_pipeline
from src.dataset_search import run_dataset_search

if __name__ == "__main__":
    print("Iniciando Pipeline de Datos de Nacimientos en México...")
    run_dataset_search(API_ENDPOINT)
    