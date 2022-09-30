from logging import basicConfig, error, critical, warning, debug, info
from logging import CRITICAL, WARNING, INFO, DEBUG, ERROR
from logging import FileHandler, StreamHandler
from decouple import config

def log (filename):
    basicConfig(
        level=config('NIVEL_LOG'),
            handlers=[
            FileHandler(f"./logs/{filename}.txt",encoding = "UTF-8"), 
            StreamHandler()
        ],
        format='%(asctime)s %(name)s %(levelname)s: %(message)s',
    )