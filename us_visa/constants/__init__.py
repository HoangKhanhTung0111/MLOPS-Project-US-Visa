import os
from datatime import datetime
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

DATABASE_NAME = "US_VISA"

COLLECTION_NAME = "visa_data"

MONGODB_URL_KEY = os.getenv("MONGODB_URL")