# Khác với file template.py (tạo ra cấu trúc thư mục và file ở thời điểm khởi tạo project),
# File này chứa các hằng số, dùng để cất output của pipline vào folder artifact (trong lúc train hoặc predict) 
# và các thông tin cần thiết khác (như tên database, collection, url của mongodb, aws,...)

import os
from datatime import datetime
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

DATABASE_NAME = "US_VISA"

COLLECTION_NAME = "visa_data"

MONGODB_URL_KEY = os.getenv("MONGODB_URL")

PIPELINE_NAME: str = "usvisa" # Type hint: explicitly define the pipeline name as a constant
ARTIFACT_DIR: str = "artifact"

MODEL_FILE_NAME = "model.pkl"

"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "visa_data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2