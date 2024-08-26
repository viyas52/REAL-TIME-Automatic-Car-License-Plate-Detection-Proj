from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    pretrained_model_path:str
    pretrained_model_name: str
    
    
@dataclass
class DataValidationArtifact:
    validation_status: bool

