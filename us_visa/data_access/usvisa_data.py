"""
The main function of this module is to collect data from a collection in MongoDB,
and return it as a pandas DataFrame
and do some basic data cleaning
"""

from us_visa.configuration.mongo_db_connection import MongoDBClient
from us_visa.constants import DATABASE_NAME
from us_visa.exception import USvisaException

import pandas as pd
import numpy as np
import sys
from typing import Optional # for "type hinting"

class USvisaData:
    """
    A class to handle data access for the US visa dataset from MongoDB and export MongoDB data to DataFrame.
    """
    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME) # Connect to MongoDB using the MongoDBClient class
        except Exception as e:
            raise USvisaException(e, sys)
        
    # database_name is optional because it is already set in the MongoDBClient class, but we can override it if needed
    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Exports a MongoDB collection as a pandas DataFrame.
        Args:
            collection_name (str): The name of the MongoDB collection to export.
            database_name (Optional[str]): The name of the MongoDB database. If None, it will use the default database set in MongoDBClient.
        Returns:
            pd.DataFrame: A DataFrame containing the data from the specified MongoDB collection.
        """
        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name] # if database_name is not provided, use the default database from MongoDBClient
            else:
                collection = self.mongo_client[database_name][collection_name] # if database_name is provided, use it to get the collection
                
            df = pd.DataFrame(list(collection.find())) # Convert the MongoDB collection to a pandas DataFrame, .find() returns a cursor, so we convert it to a list first
            if "_id" in df.columns.to_list(): # if the _id column is present, we drop it because it is not needed for analysis
                df.drop("_id", axis=1, inplace=True) # drop the _id column from the DataFrame
                
            df.replace({"na": np.nan}, inplace=True) # replace "na" with np.nan for better handling of missing values
            return df
        
        except Exception as e:
            raise USvisaException(e, sys)