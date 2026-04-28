"""
The main function of this file is to interpret from word to number (Label Encoding), and from number to word (Decoding)
Eg: case_status column in the dataset contains 2 values: "Denied": 0, "Approved": 1
"""

import sys
from pandas import DataFrame
from sklearn.pipeline import Pipeline

from us_visa.exception import USVisaException
from us_visa.logger import logging

class TargetValueMapping:
    # Chiều thuận từ chữ sang số (khi training)
    def __init__(self):
        self.Certificate: int = 0
        self.Denied: int = 1
    
    # Create a method to return a dict to map the target variable values: {"Certificate": 0, "Denied": 1}
    def _asdict(self):
        return self.__dict__
    
    # Chiều nghịch từ số sang chữ (khi predict): {0: "Certificate", 1: "Denied"}
    def reverse_mapping(self) -> dict:
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(), mapping_response.keys())) # zip() group values and keys together, then dict() convert them to dict