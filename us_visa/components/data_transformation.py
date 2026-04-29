"""
The main function of this file is to perform data transformation,
which includes encoding categorical variables, scaling numerical features, and handling missing values.
"""

import sys

import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, PowerTransformer
from sklearn.compose import ColumnTransformer

from us_visa.constants import TARGET_COLUMN, SCHEMA_FILE_PATH, CURRENT_YEAR
from us_visa.entity.config_entity import DataTransformationConfig
from us_visa.entity.artifact_entity import DataTransformationArtifact, DataIngestionArtifact, DataValidationArtifact
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.utils.main_utils import save_object, save_numpy_array_data, read_yaml_file, drop_columns
from us_visa.entity.estimator import TargetValueMapping


class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact):
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_transformation_config: configuration for data transformation
        """
        try:
            # Vẫn cần artifact của data ingestion vì quá trình data validation chỉ kiểm tra dữ liệu,
            # còn data transformation thì vần cần dữ liệu từ data ingestion
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise USvisaException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise USvisaException(e, sys)
        
    def get_data_transformer_object(self) -> Pipeline:
        """
        Method Name :   get_data_transformer_object
        Description :   This method creates and returns a data transformer object for the data
        
        Output      :   data transformer object is created and returned 
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info(
            "Entered get_data_transformer_object method of DataTransformation class"
        )

        try:
            logging.info("Initializing preprocessing steps (StandardScaler, OneHotEncoder, OrdinalEncoder, PowerTransformer)")

            # Cú pháp để khởi tạo các bước tiền sử lý dữ liệu
            numeric_transformer = StandardScaler()
            oh_transformer = OneHotEncoder()
            ordinal_encoder = OrdinalEncoder()

            logging.info("Initialized StandardScaler, OneHotEncoder, OrdinalEncoder")

            # Khai báo 1 pipeline để thực hiện PowerTransformer
            transform_pipe = Pipeline(steps=[
                ('transformer', PowerTransformer(method='yeo-johnson'))
            ])
            
            # Khởi tạo đối tượng ColumnTransformer để áp dụng các bước tiền xử lý đã khai báo ở trên cho các cột tương ứng trong dataset
            preprocessor = ColumnTransformer(
                transformers=[
                    ("OneHotEncoder", oh_transformer, self._schema_config['oh_columns']),
                    ("Ordinal_Encoder", ordinal_encoder, self._schema_config['or_columns']),
                    ("Transformer", transform_pipe, self._schema_config['transform_columns']),
                    ("StandardScaler", numeric_transformer, self._schema_config['num_features'])
                ]
            )

            logging.info("Successfully created preprocessor ColumnTransformer object")
            
            return preprocessor

        except Exception as e:
            raise USvisaException(e, sys) from e
        
    def initiate_data_transformation(self, ) -> DataTransformationArtifact:
        """
        Method Name :   initiate_data_transformation
        Description :   This method initiates the data transformation component for the pipeline 
        
        Output      :   data transformer steps are performed and preprocessor object is created  
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            # 1. Check only if data validation is successful, we perform data transformation
            if self.data_validation_artifact.validation_status:
                logging.info("--- STARTING DATA TRANSFORMATION ---")
                
                preprocessor = self.get_data_transformer_object()
                
                # 2. Read the data
                train_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
                test_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.test_file_path)

                # Get the columns to be dropped from the schema config
                drop_cols = self._schema_config['drop_columns']
                
                # 3. Group feature engineering for both train and test
                for df in [train_df, test_df]:
                    # Tạo cột mới: Tuổi công ty
                    df['company_age'] = CURRENT_YEAR - df['yr_of_estab']
                    # Chuyển đổi nhãn Target sang số (0, 1)
                    df[TARGET_COLUMN] = df[TARGET_COLUMN].replace(TargetValueMapping()._asdict())

                # drop unnecessary columns
                train_df = drop_columns(df=train_df, cols=drop_cols)
                test_df = drop_columns(df=test_df, cols=drop_cols)

                # 4. Separate input features and target feature from train and test dataframe
                input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
                target_feature_train_df = train_df[TARGET_COLUMN]
                
                input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
                target_feature_test_df = test_df[TARGET_COLUMN]

                # 5. Apply the preprocessor object on input features of train and test
                logging.info("Applying preprocessor object on input features of train and test dataframes")
                
                # Train data use fit_transform() (vừa fit vừa transform)
                input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
                
                # Test data use only transform() (vì đã fit trên train data rồi)
                input_feature_test_arr = preprocessor.transform(input_feature_test_df)
                
                # 6. Apply SMOTEENN to handle imbalanced data (on train data only, not on test data)
                logging.info("Applying SMOTEENN to handle imbalanced data")
                smt = SMOTEENN(sampling_strategy='minority')
                input_feature_train_arr, target_feature_train_arr = smt.fit_resample(input_feature_train_arr, target_feature_train_df)
                logging.info(f"Shape of input features after SMOTEENN: {input_feature_train_arr.shape}, Shape of target feature after SMOTEENN: {target_feature_train_arr.shape}")
                
                # 7. Save data in numpy array format
                # np.c__() is used to concatenate the input features and target feature together in the same array
                # input feature already in array format after preprocessor, target feature need to convert to array format by np.array()
                train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_arr)] 
                test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
                
                # 8. Save artifacts: preprocessor object, train array, test array
                save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
                save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
                save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)

                logging.info("--- COMPLETED DATA TRANSFORMATION ---")
                
                # 9. Prepare artifact to return from this component
                data_transformation_artifact = DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
                )

                return data_transformation_artifact
            else:
                raise Exception(self.data_validation_artifact.message)

        except Exception as e:
            raise USvisaException(e, sys) from e