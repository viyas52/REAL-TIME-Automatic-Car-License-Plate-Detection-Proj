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
       
       
    def download_model(self)-> str:
        try:
            model_url = self.data_ingestion_config.model_download_url
            data_dir = self.data_ingestion_config.data_ingestion_dir
            model_file_dir = self.data_ingestion_config.pretrained_model_file_path
            os.makedirs(data_dir,exist_ok=True)
            os.makedirs(model_file_dir,exist_ok=True)
            model_file_name = os.path.basename(model_url)
            model_file_path = os.path.join(model_file_dir,model_file_name)
            logging.info(f"Downloading data from {model_url} into {model_file_path} directory")
            urllib.request.urlretrieve(model_url, model_file_path)
            logging.info(f"Downloaded data from {model_url} into {model_file_path} directory")        
            
            return model_file_path
            
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")
        try:
            model_file_path = self.download_model()
            
            data_ingestion_artifact = DataIngestionArtifact(pretrained_model_path=model_file_path)
            
            logging.info("Exited initiate_data_ingestion method of Data_Ingestion class")
            
            return data_ingestion_artifact

        except Exception as e:
            raise CustomException(e, sys)     