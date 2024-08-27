import logging
import os
import sys
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%d_%m_%y-%I_%M_%S_%p')}.log"
LOG_FILE = LOG_FILE.replace('_0', '_').replace('-0', '-')

logs_dir=os.path.join(os.getcwd(),"logs")
os.makedirs(logs_dir,exist_ok=True)

LOG_FILE_PATH=os.path.join(logs_dir,LOG_FILE)

logging.basicConfig(
    
    format="[ %(asctime)s ] %(name)s , line : %(lineno)d - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y %I:%M:%S %p",
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler(sys.stdout)
    ]


)