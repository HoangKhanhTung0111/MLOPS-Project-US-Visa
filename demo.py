"""
from us_visa.logger import logging
logging.info("Test logging module")
"""

"""
from us_visa.exception import USvisaException
import sys
try:
    a = 1 / 0
except Exception as e:
    raise USvisaException(e, sys)
"""

from us_visa.pipline.training_pipeline import TrainingPipeline
from dotenv import load_dotenv # Khi test demo thì cũng phải load env

load_dotenv() # Load environment variables from .env file

obj = TrainingPipeline()
obj.run_pipeline()