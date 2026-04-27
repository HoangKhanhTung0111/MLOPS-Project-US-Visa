"""
The main function of this module is to: validate the data fetch by data ingestion,
check if there is data drift between train and test data, and return artifact
"""

import sys
import json

import pandas as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection

from pandas import DataFrame

from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.utils.main_utils import read_yaml_file, write_yaml_file
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from us_visa.entity.config_entity import DataValidationConfig
from us_visa.constants import SCHEMA_FILE_PATH

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_validation_config: configuration for data validation
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact # Gán artifact của data ingestion vào biến instance để sử dụng trong các phương thức khác
            self.data_validation_config = data_validation_config # Gán bản thiết kế "config" vào biến instance để sử dụng trong các phương thức khác
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise USvisaException(e,sys)
        
    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        """
        Method Name :   validate_number_of_columns
        Description :   This method validates the number of columns
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logging.info(f"Number of columns validation status: {status}")
            return status
        except Exception as e:
            raise USvisaException(e, sys)
    
    def is_column_exist(self, df: DataFrame) -> bool:
        """
        Method Name :   is_column_exist
        Description :   This method validates the existence of a numerical and categorical columns
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            dataframe_columns = df.columns
            missing_numerical_columns = []
            missing_categorical_columns = []
            
            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)
                    
            if len(missing_numerical_columns) > 0:
                logging.info(f"Missing numerical columns: {missing_numerical_columns}")
                
            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)
            
            if len(missing_categorical_columns) > 0:
                logging.info(f"Missing categorical columns: {missing_categorical_columns}")
                
            return False if len(missing_numerical_columns) > 0 or len(missing_categorical_columns) > 0 else True
        except Exception as e:
            raise USvisaException(e, sys)
        
    # Hàm read_data() này có thể dùng chung cho cả data ingestion và data validation, 
    # nhưng mình để trong data validation vì nó liên quan đến việc đọc file báo cáo drift sau khi đã tính toán
    # Và static method vì nó không động đến biến instance, có thể gọi trực tiếp bằng tên class, và không cần self
    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise USvisaException(e, sys)
        
    # A function that use "Evidently" library to detect data drift between ref and cur data
    def detect_data_drift(self, reference_df: DataFrame, current_df: DataFrame) -> bool:
        """
        Method Name :   detect_dataset_drift
        Description :   This method validates if drift is detected
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            data_drift_profile = Profile(sections=[DataDriftProfileSection()]) # Create a profile (báo cáo) with the data drift section
            data_drift_profile.calculate(reference_df, current_df) 
            
            json_report = json.loads(data_drift_profile.json()) # Convert the profile to json format
            
            # Save data drift report to yaml file
            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content=json_report)
            
            # Python syntax to access the nested dictionary in json_report
            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
            n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]
            drift_status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]
            
            logging.info(f"Drift metrics: {n_drifted_features}/{n_features} features drifted.")
            logging.info(f"Overall Dataset Drift Detected: {drift_status}")
            
            return drift_status
        except Exception as e:
            raise USvisaException(e, sys)
            
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info("--- STARTING DATA VALIDATION ---")
            error_msg = []
            
            train_df = self.read_data(self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.test_file_path)
            
            # Validate number of columns
            if not self.validate_number_of_columns(train_df):
                error_msg.append("Train dataframe has incorrect number of columns.")
            if not self.validate_number_of_columns(test_df):
                error_msg.append("Test dataframe has incorrect number of columns.")
                
            # Validate name of columns
            if not self.is_column_exist(train_df):
                error_msg.append("Train dataframe is missing required columns.")
            if not self.is_column_exist(test_df):
                error_msg.append("Test dataframe is missing required columns.")
                
            validate_status = len(error_msg) == 0
            validation_error_msg = " | ".join(error_msg)
            
            # Check data drift only if the basic validation is passed
            if validate_status:
                drift_status = self.detect_data_drift(reference_df=train_df, current_df=test_df)
                
                if drift_status:
                    validation_error_msg = "Data drift detected between train and test datasets."
                else:
                    validation_error_msg = "No data drift detected between train and test datasets."
            else:
                logging.info(f"Data validation failed with errors: {validation_error_msg}")
                
            # Artifact
            data_validation_artifact = DataValidationArtifact(
                validation_status=validate_status,
                message=validation_error_msg,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            
            logging.info(f"Data validation artifact created: {data_validation_artifact}")
            logging.info("--- DATA VALIDATION COMPLETED ---")
            
            return data_validation_artifact
        except Exception as e:
            raise USvisaException(e, sys)