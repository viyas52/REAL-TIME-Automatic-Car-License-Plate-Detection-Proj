import os
from dataclasses import dataclass
from datetime import datetime

from ANPR.constant.training_pipeline import *

TIMESTAMP:str = datetime.now().strftime("%d_%m_%y-%I_%M_%p")

@dataclass
class TrainingPipelineConfig:
    artifacts_dir: str = os.path.join(ARTIFACTS_DIR, TIMESTAMP)
    
training_pipeline_config:TrainingPipelineConfig = TrainingPipelineConfig()

@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(training_pipeline_config.artifacts_dir, DATA_INGESTION_DIR_NAME)

    pretrained_model_file_path: str = os.path.join(data_ingestion_dir, PRE_TRAINED_MODEL)

    model_download_url: str = MODEL_DOWNLOAD_URL
    
    
    

@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(training_pipeline_config.artifacts_dir, DATA_VALIDATION_DIR_NAME)

    valid_status_file_dir: str = os.path.join(data_validation_dir, DATA_VALIDATION_STATUS_FILE)

    required_file_list = DATA_VALIDATION_ALL_REQUIRED_FILES
    