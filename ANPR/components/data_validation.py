import os, sys
import shutil

from ANPR.logger import logging
from ANPR.exception import CustomException

from ANPR.entity.config_entity import DataValidationConfig
from ANPR.entity.artifacts_entity import (DataIngestionArtifact,
                                                  DataValidationArtifact)



class DataValidation:
    def __init__(self,data_ingestion_artifact: DataIngestionArtifact,data_validation_config: DataValidationConfig,):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config

        except Exception as e:
            raise CustomException(e, sys) 
        

    
    def validate_all_files_exist(self) -> bool:
        try:
            
            validation_status = None
            all_files = os.listdir(self.data_ingestion_artifact.pretrained_model_path)

            for file in all_files:
                if file not in self.data_validation_config.required_file_list:
                    validation_status = False
                    os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)
                    with open(self.data_validation_config.valid_status_file_dir, 'w') as f:
                        f.write(f"Validation status: {validation_status}")

                else:
                    validation_status = True
                    os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)
                    with open(self.data_validation_config.valid_status_file_dir, 'w') as f:
                        f.write(f"Validation status: {validation_status}")
            
            return validation_status

        except Exception as e:
            raise CustomException(e, sys)
        

    
    def initiate_data_validation(self) -> DataValidationArtifact: 
        logging.info("Entered initiate_data_validation method of DataValidation class")
        try:
            status = self.validate_all_files_exist()
            data_validation_artifact = DataValidationArtifact(
                validation_status=status)

            logging.info("Exited initiate_data_validation method of DataValidation class")
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            
            os.makedirs("models_used",exist_ok=True)
            copy_file_path = os.path.join(self.data_ingestion_artifact.pretrained_model_path,self.data_ingestion_artifact.pretrained_model_name)
            if status:
                shutil.copy(copy_file_path, "models_used")

            return data_validation_artifact

        except Exception as e:
            raise CustomException(e, sys)