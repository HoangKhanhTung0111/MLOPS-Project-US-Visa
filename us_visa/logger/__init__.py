# CUSTOM LOGGING MODULE


import logging
import os

#from from_root import from_root # Help identify the root folder of the project, even if run on child folder -> Bug
from datetime import datetime

# datetime.now(): Return the OS's time in a list (month, day, year,...)
# .strftime: Convert time to string 
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

log_dir = os.path.join(os.getcwd(), "logs")

# return "D:\2025\MLOPS-Project-US-Visa\logs\03_15_2026_14_30_00.log"
logs_path = os.path.join(log_dir, LOG_FILE)

os.makedirs(log_dir, exist_ok=True)

# Re-config the logging module (or class)
# %(asctime)s: Time that code is excecute
# %(name)s: Name of the module running the code
# %(levelname)s: Importance level (INFOR, WARNING, ERROR, DEBUG)
# %(message)s: Message you want to write
logging.basicConfig(
    filename=logs_path,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)