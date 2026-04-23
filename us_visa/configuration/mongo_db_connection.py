'''
The main purpose of this file is to define a class where you can just call that class, and you can connect to mongodb
instead of writing the same code to connect to mongodb in every file, you can just import this class and call it to connect to mongodb
'''

# Ta sẽ không đặt dotenv ở đây, mà hàm load_dotenv() sẽ được đặt ở file main.py
# Tức là việc nạp biến MT sẽ chỉ nên được thực hiện 1 lần duy nhất ở fiel main.py
# Nếu chỗ nào cần dùng biến MT mà cứ phải load_dotenv() thì sẽ không ổn, vì nó sẽ bị lặp lại nhiều lần


import sys

from us_visa.exception import USvisaException
from us_visa.logger import logging

import os
from us_visa.constants import DATABASE_NAME, MONGODB_URL_KEY
import pymongo
import certifi # A library that provides root certificates

# When connecting to MongoDB Atlas, it need SSL/TLS connection
# But sometimes, your local machine may not have the necessary root certificates to establish a secure connection
# So certifi.where() will provide the path to the certificate file that contains the trusted root certificates
ca = certifi.where()

class MongoDBClient:
    """
    Use this class to connect to MongoDB and perform database operations
    """
    
    client = None
    
    def __init__(self, database_name=DATABASE_NAME) -> None: # self: Là đối tượng hiện tại của class
        try:
            if MongoDBClient.client is None: # If the client is not already created, create a new one (tránh mở nhiều kết nối đến MongoDB - singleton pattern)
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set. Please set it in the .env file.")
                
                # Connect to MongoDB, pass the certificate file ca
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
                
                self.client = MongoDBClient.client # Gán kết nối chung (MongoDBClient.client) cho instance variable (đối tượng hiện tại)
                self.database = self.client[database_name] # Choose the specific database
                self.datbase_name = database_name # Store the database name as an instance variable
                logging.info(f"Connected to MongoDB database: {database_name} successfully.")
                
        except Exception as e:
            raise USvisaException(e, sys)
                