"""
The main function of this module is to: collect data from MongoDB, store it in feature store,
split train/test data, and return artifact
"""

import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.data_access.usvisa_data import USvisaData

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        """
        args:
            data_ingestion_config (DataIngestionConfig): The configuration for data ingestion
        """
        try:
            self.data_ingestion_config = data_ingestion_config # Gán bản thiết kế "config" vào biến instance để sử dụng trong các phương thức khác
        except Exception as e:
            raise USvisaException(e, sys)
        
    def export_data_into_feature_store(self) -> DataFrame:
        """
        Method Name :   export_data_into_feature_store
        Description :   This method exports data from mongodb to csv file locally
        
        Output      :   Dataframe containing the raw dataset
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logging.info("Exporting data from MongoDB to feature store")
            usvisa_data = USvisaData() # Create an instance of the USvisaData class to access the data from MongoDB
            dataframe = usvisa_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name) # Export the MongoDB collection as a DataFrame
            logging.info(f"Shape of exported dataframe: {dataframe.shape}")
            
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path # Get the file path for the feature store from the config
            
            os.makedirs(os.path.dirname(feature_store_file_path), exist_ok=True) # Create the directory for the feature store if it does not exist
            
            logging.info(f"Saving exported data to feature store at: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path, index=False, header=True) # index=False not write row index, header=True write column names
            
            return dataframe
        except Exception as e:
            raise USvisaException(e, sys)
        
    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Method Name :   split_data_as_train_test
        Description :   This method splits the dataframe into train set and test set based on split ratio 
            
        Output      :   Train and Test CSV files are created in local directory
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entering split_data_as_train_test method of DataIngestion class")
        
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performing train test split with test size: {}".format(self.data_ingestion_config.train_test_split_ratio))
            
            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path), exist_ok=True) # Create the directory for the training file if it does not exist
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            
            logging.info("Exported train and test files successfully.")
            logging.info("Exited split_data_as_train_test method of DataIngestion class")
        except Exception as e:
            raise USvisaException(e, sys)
        
    # Main method to be called from the pipeline
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Method Name :   initiate_data_ingestion
        Description :   This method initiates the data ingestion components of training pipeline 
        
        Output      :   DataIngestionArtifact containing paths to train and test sets
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Starting data ingestion process")
        
        try:
            dataframe = self.export_data_into_feature_store() # Export data from MongoDB to feature store and get the DataFrame
            self.split_data_as_train_test(dataframe) # Split the DataFrame into train and test sets and save them to local directory
            
            # Create artifact to return the paths to the train and test sets
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            
            logging.info(f"Data ingestion artifact created: {data_ingestion_artifact}")
            logging.info("--- COMPLETED DATA INGESTION ---")
            
            return data_ingestion_artifact
        except Exception as e:
            raise USvisaException(e, sys)