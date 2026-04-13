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