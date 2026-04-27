import sys
from us_visa.exception import USvisaException
from us_visa.logger import logging

from us_visa.components.data_ingestion import DataIngestion
from us_visa.components.data_validation import DataValidation

from us_visa.entity.config_entity import (DataIngestionConfig,
                                         DataValidationConfig)
from us_visa.entity.artifact_entity import (DataIngestionArtifact,
                                           DataValidationArtifact)

class TrainingPipeline:
    def __init__(self): # Không cần truyền tham số vào vì đã có config sẵn trong class DataIngestionConfig
        self.data_ingestion_config = DataIngestionConfig() # Create an instance of the DataIngestionConfig class to get the configuration for data ingestion
        self.data_validation_config = DataValidationConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        This method of TrainPipeline class is responsible for starting data ingestion component
        """
        logging.info("Starting data ingestion component")
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config) # Create an instance of the DataIngestion class with the data ingestion configuration
            
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion() # Call the method to start data ingestion and get the artifact
            
            logging.info("Exited the start_data_ingestion method of TrainPipeline class")
            
            return data_ingestion_artifact
        
        except Exception as e:
            raise USvisaException(e, sys) from e
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        """
        This method of TrainPipeline class is responsible for starting data validation component
        """
        logging.info("Starting data validation component")
        try:
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                             data_validation_config=self.data_validation_config
                                             )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Exited the start_data_validation method of TrainPipeline class")

            return data_validation_artifact

        except Exception as e:
            raise USvisaException(e, sys) from e
        
    # Main method to run the training pipeline
    def run_pipeline(self) -> None:
        """
        This method of TrainPipeline class is responsible for running complete pipeline
        """
        try:
            data_ingestion_artifact = self.start_data_ingestion() # Start data ingestion and get the artifact
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact) # Start data validation and get the artifact
        except Exception as e:
            raise USvisaException(e, sys)