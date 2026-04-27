# Khác với file template.py (tạo ra cấu trúc thư mục và file ở thời điểm khởi tạo project),
# File này chứa các hằng số, dùng để cất output của pipline vào folder artifact (trong lúc train hoặc predict) 
# và các thông tin cần thiết khác (như tên database, collection, url của mongodb, aws,...)

# Không nên mã hóa luôn giá trị của MongoDB URL vào đây, mà file này chỉ để chứa tên hằng
# còn việc lấy giá trị của Key sẽ được thực hiện ở trong các class

import os
from datetime import date

# Mongodb related constants
DATABASE_NAME = "US_VISA"
COLLECTION_NAME = "visa_data"
MONGODB_URL_KEY = "MONGODB_URL"

# Folder and file name related constants
PIPELINE_NAME: str = "usvisa" # Type hint: explicitly define the pipeline name as a constant
ARTIFACT_DIR: str = "artifact"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

MODEL_FILE_NAME = "model.pkl"
FILE_NAME: str = "usvisa.csv"

TARGET_COLUMN = "case_status"
CURRENT_YEAR = date.today().year
# file .pkl is used to freeze an object in python, 
# in this case, we will freeze the preprocessing object (contains steps to preprocess data-data transformation),
# like scaling, encoding,..., and then we can load it later to preprocess the data in the same way as we did in training step 
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")

"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "visa_data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2