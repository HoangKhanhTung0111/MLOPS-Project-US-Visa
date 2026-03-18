import os
import sys

import numpy as np
import dill # Used to "freeze" an python object like a ML model, convert it to binary. Stronger than pickle, and similar to Serializable
import yaml # Read/write .yaml file (.yaml file is used to write config file)
from pandas import DataFrame

from us_visa.exception import USvisaException
from us_visa.logger import logging

def read_yaml_file(file_path: str) -> dict: # type hint (don't have to be that exactly that type, just "hint")
    try:
        with open(file_path, "rb") as yaml_file: # "rb": read byte, safer than "r", because some unique character can't be "r"
            return yaml.safe_load(yaml_file) # Convert content in yaml file to python dict
        
    except Exception as e:
        raise USvisaException(e, sys) from e # Exception chaining, help keep all the history of the error from e
    
def write_yaml_file(file_path: str, content: object, replace: bool=False) -> None: # if replace=True then erase old file
    try:
        if (replace):
            if (os.path.exists(file_path)):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True) # Make a folder contain the yaml file if it haven't exist
        with open(file_path, "w") as file:
            yaml.dump(content, file) # Convert python object/dict to yaml format and write to yaml file
            
    except Exception as e:
        raise USvisaException(e, sys) from e
    
# We wrap the drop() func in this drop_columns() because we want to know "Kiểm soát quy trình xóa đó như thế nào", 
# it have logging, try-except, like a service layer in java spring boot
def drop_columns(df: DataFrame, cols: list) -> DataFrame: 
    """
    drop the columns and form a pandas Dataframe
    df: pandas Dataframe
    cols: list of columns to be dropped
    """
    
    logging.info("Excecution started: drop_columns method with columns: {cols}") # Log to know that code have entered this func
    
    try:
        df = df.drop(columns=cols, axis=1) # axis=1 is col, =0 is row. And can use replace=True instead of df=df.drop()
        
        logging.info("Exit the drop_columns method of utils") # Log to know that have successfully drop columns
        
        return df
    
    except Exception as e:
        raise USvisaException(e, sys) from e
    
def load_object(file_path: str) -> object: # Used to load ML model, use "dill" library
    logging.info("Entered the load_object method of utils")
    
    try:
        with open(file_path, "rb") as file_obj:
            obj = dill.load(file_obj) # "decode" object from the file to its original type
            
            logging.info("Exit the load_object method of utils")
            
            return obj
        
    except Exception as e:
        raise USvisaException(e, sys) from e
    
def save_object(file_path: str, obj: object) -> None:
    logging.info("Entered the save_object method of utils")
    
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as file:
            dill.dump(obj, file)
            
        logging.info("Exit the save_object method of utils")
        
    except Exception as e:
        raise USvisaException(e, sys) from e
    
def save_numpy_array_data(file_path: str, array: np.array) -> None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as file:
            np.save(file, array)
            
    except Exception as e:
        raise USvisaException(e, sys) from e
    
def load_numpy_array_data(file_path: str) -> np.array:
    try:
        with open(file_path, "rb") as file:
            return np.load(file)
    
    except Exception as e:
        raise USvisaException(e, sys) from e