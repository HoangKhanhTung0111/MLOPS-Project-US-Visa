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


"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "visa_data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2