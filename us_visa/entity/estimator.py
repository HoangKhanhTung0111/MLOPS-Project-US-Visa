"""
This file have 2 main function (2 classes). First, is to interpret from word to number (Label Encoding), and from number to word (Decoding)
Eg: case_status column in the dataset contains 2 values: "Denied": 0, "Approved": 1

Second, is to create the wrapper class (USvisaModel): Thực hiện quá trình predict
"""

import sys
from pandas import DataFrame
from sklearn.pipeline import Pipeline

from us_visa.exception import USvisaException
from us_visa.logger import logging

class TargetValueMapping:
    # Chiều thuận từ chữ sang số (khi training)
    def __init__(self):
        self.Certified: int = 0
        self.Denied: int = 1
    
    # Create a method to return a dict to map the target variable values: {"Certificate": 0, "Denied": 1}
    def _asdict(self):
        return self.__dict__
    
    # Chiều nghịch từ số sang chữ (khi predict): {0: "Certificate", 1: "Denied"}
    def reverse_mapping(self) -> dict:
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(), mapping_response.keys())) # zip() group values and keys together, then dict() convert them to dict
    
# Class wrapper này sẽ thực hiện luôn 2 chức năng chính của pipeline là data transformation và model prediction,
# class này đặt cùng class mapping để dễ dàng cho quá trình predict, class USvisaModel sẽ đưa ra predict, 
# còn class TargetValueMapping sẽ giúp chuyển đổi giá trị của target variable (case_status) từ chữ sang số và ngược lại
# Thực chất là class này nhận vào 2 object là oject chứa các bước tiền xử lý dữ liệu, và object chứa model tốt nhất được chọn bởi neuro-mf, 
# sau đó khi gọi hàm predict() của class này thì sẽ tự động thực hiện quá trình transform dữ liệu đầu vào và đưa ra kết quả dự đoán luôn,
class USvisaModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        """
        :param preprocessing_object: Input Object of preprocesser
        :param trained_model_object: Input Object of trained model 
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, dataframe: DataFrame) -> DataFrame:
        """
        Function accepts raw inputs and then transformed raw input using preprocessing_object
        which guarantees that the inputs are in the same format as the training data
        At last it performs prediction on transformed features
        """
        logging.info("Entered predict method of USvisaModel class")

        try:
            logging.info("Using the trained model to get predictions")

            transformed_feature = self.preprocessing_object.transform(dataframe)

            logging.info("Used the trained model to get predictions")
            return self.trained_model_object.predict(transformed_feature)

        except Exception as e:
            raise USvisaException(e, sys)

    # hàm có dấu __ là hàm hệ thống gọi ngầm, không cần gọi trực tiếp, nó sẽ tự động được gọi khi thực hiện các thao tác liên quan đến object của class USvisaModel
    # nó quyết định khi sử dụng print(model) thì sẽ in ra gì,...
    # tức là thay vì in ra <__main__.USvisaModel object at 0x7f8...>, thì sẽ in ra tên của model được sử dụng, ví dụ: RandomForestClassifier() 
    # __repr__() dùng để trả về 1 chuỗi đại diện cho object, thường được sử dụng cho mục đích debug,
    def __repr__(self):
        """Định nghĩa tên hiển thị của Object khi gọi trong Interactive Shell"""
        return f"{type(self.trained_model_object).__name__}()" # __name() tìm tên của của model được sử dụng

    # còn __str__() thì trả về 1 chuỗi dễ đọc hơn, thường được sử dụng để hiển thị thông tin cho người dùng
    def __str__(self):
        """Định nghĩa tên hiển thị của Object khi dùng lệnh print()"""
        return f"{type(self.trained_model_object).__name__}()"