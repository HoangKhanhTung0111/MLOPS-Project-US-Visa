'''
File này khác với config_entity.py ở chỗ, nó lưu thông tin về artifact (OUTPUT) của pipeline
Được tạo ra sau khi 1 giai đoạn của pipeline hoàn thành
VD: Hệ thống ban đầu đọc file config_entity.py để lấy tỷ lệ chia train test, sau đó
chạy hàm chia data, lưu file train.csv và test.csv vào thư mục A
code sẽ trả về 1 object DataIngestionArtifact chứa đường dẫn đến file train.csv và test.csv, 
sau đó sẽ được truyền vào giai đoạn tiếp theo của pipeline (VD: data transformation) để sử dụng
'''

from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status:bool
    message: str
    drift_report_file_path: str
    
@dataclass
class DataTransformationArtifact:
    transformed_object_file_path:str 
    transformed_train_file_path:str
    transformed_test_file_path:str
