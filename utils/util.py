from logging import basicConfig, error, critical, warning, debug, info
from logging import CRITICAL, WARNING, INFO, DEBUG, ERROR
from logging import FileHandler, StreamHandler
from decouple import config
import os

def log (filename):
    log_filename = f"./logs/{filename}.txt"
    os.makedirs(os.path.dirname(log_filename), exist_ok=True)
    basicConfig(
        level=config('NIVEL_LOG'),
            handlers=[
            FileHandler(log_filename,encoding = "UTF-8"), 
            StreamHandler()
        ],
        format='%(asctime)s %(name)s %(levelname)s: %(message)s',
    )