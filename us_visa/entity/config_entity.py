'''
MỤC ĐÍCH CỦA VIỆC PHẢI KHAI BÁO THÀNH CÁC CLASS LÀ:
1. Gom nhóm các thông tin liên quan đến nhau vào cùng 1 class
2. Dễ truyền dữ liệu: VD: khi viết hàm chia data, thay vì phải truyền nhiều tham số, thì chỉ cần truyền 1 object DataIngestionConfig 
'''

'''
Mục đích chính của file này là: định nghĩa cấu trúc lưu trữ thông tin, chứa đường dẫn, tên file, và các tham số cần thiết (như train_test_split_ratio)
'''
import os
from us_visa.constants import *
from dataclasses import dataclass
from datetime import datetime

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S") # type hint

# Thông thường nếu là 1 python class thì sẽ phải tự khơi tạo hàm def __init__()
@dataclass # Decorator to automatically generate special methods like __init__() and __repr__()
class TrainingPipelineConfig:
    pipeline_name: str = PIPELINE_NAME
    
    # Không dùng ARTIFACT_DIR trực tiếp vì nó sẽ bị ghi đè mỗi lần chạy pipeline, 
    # thay vào đó tạo folder mới với timestamp để lưu output của mỗi lần chạy
    # Không dùng ARARTIFACT_DIR + "/" + TIMESTAMP vì sẽ không tương thích với các hệ điều hành khác nhau (Windows: \, Linux: /, MacOS),
    artifact_dir: str = os.path.join(ARTIFACT_DIR, TIMESTAMP) 
    timestamp: str = TIMESTAMP
    
# Tạo instance của TrainingPipelineConfig để sử dụng trong pipeline
training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()

# Định nghĩa nơi dữ liệu thô dc tải về sẽ được lưu trữ ở đâu, nơi chia train, test, và tỉ lệ chia
@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)
    feature_store_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)
    training_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
    testing_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)
    train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    collection_name:str = DATA_INGESTION_COLLECTION_NAME
    
# Define where the data drift report will be stored, and what is the name of the report file
@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME)
    drift_report_file_path: str = os.path.join(data_validation_dir, DATA_VALIDATION_DRIFT_REPORT_DIR,
                                               DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
    
@dataclass
class DataTransformationConfig:
    data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME)
    transformed_train_file_path: str = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                    TRAIN_FILE_NAME.replace("csv", "npy")) # Change .csv to .npy because we will save the transformed data in numpy format
    transformed_test_file_path: str = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                   TEST_FILE_NAME.replace("csv", "npy"))
    transformed_object_file_path: str = os.path.join(data_transformation_dir,
                                                     DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
                                                     PREPROCESSING_OBJECT_FILE_NAME)