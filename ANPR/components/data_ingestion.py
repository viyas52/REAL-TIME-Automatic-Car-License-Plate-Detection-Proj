import os
import sys
from six.moves import urllib # type: ignore
import zipfile

from ANPR.logger import logging
from ANPR.exception import CustomException

from ANPR.entity.config_entity import DataIngestionConfig
from ANPR.entity.artifacts_entity import DataIngestionArtifact




class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
           raise CustomException(e, sys)
        
    

    def download_data(self)-> str:
        '''
        Fetch data from the url
        '''

        try: 
            dataset_url = self.data_ingestion_config.model_download_url
            zip_download_dir = self.data_ingestion_config.data_ingestion_dir
            os.makedirs(zip_download_dir, exist_ok=True)
            data_file_name = os.path.basename(dataset_url)
            zip_file_path = os.path.join(zip_download_dir, data_file_name)
            logging.info(f"Downloading data from {dataset_url} into file {zip_file_path}")
            urllib.request.urlretrieve(dataset_url, zip_file_path)
            logging.info(f"Downloaded data from {dataset_url} into file {zip_file_path}")
            return zip_file_path

        except Exception as e:
            raise CustomException(e, sys)
        
        
    def extract_zip_file(self,zip_file_path: str)-> str:
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        try:
            models_path = self.data_ingestion_config.pretrained_model_file_path
            os.makedirs(models_path, exist_ok=True)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(models_path)
            logging.info(f"Extracting zip file: {zip_file_path} into dir: {models_path}")

            return models_path

        except Exception as e:
            raise CustomException(e, sys)
        
        
        
    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")
        try: 
            zip_file_path = self.download_data()
            models_path = self.extract_zip_file(zip_file_path)

            data_ingestion_artifact = DataIngestionArtifact(
                pretrained_model_zip_path = zip_file_path,
                pretrained_model_path = models_path
            )

            logging.info("Exited initiate_data_ingestion method of Data_Ingestion class")
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact
        
        except Exception as e:
            raise CustomException(e, sys)     