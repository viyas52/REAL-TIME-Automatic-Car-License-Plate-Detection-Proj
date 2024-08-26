import os

ARTIFACTS_DIR:str = "artifacts"


"""
Data Ingestion
"""

DATA_INGESTION_DIR_NAME:str = "data_ingestion"

PRE_TRAINED_MODEL:str = "pretrained_model"

MODEL_DOWNLOAD_URL:str = "https://github.com/viyas52/data_dump_repo/raw/main/license_models.zip"



"""
Data Validation 
"""

DATA_VALIDATION_DIR_NAME: str = "data_validation"

DATA_VALIDATION_STATUS_FILE: str = 'status.txt'

DATA_VALIDATION_ALL_REQUIRED_FILES = ["BLPDM.pt","yolov10n.pt"]


"""
MODEL RUNNER 
"""



