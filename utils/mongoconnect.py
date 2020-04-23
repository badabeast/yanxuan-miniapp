from utils.filereader import InIReader
from mongoengine import *
import os
from pathlib import Path
class MongoConnect():
    def __init__(self, *args, **kwargs):
        CURRENT_PATH = Path(__file__).parent
        configfile = os.path.join(os.path.dirname(CURRENT_PATH),"conf","conf.ini")
        config = InIReader(configfile).config
        connect(config.get('mongodb','dbname'),
                host=config.get('mongodb','host'),
                port=config.getint('mongodb','port'))
        return super().__init__(*args, **kwargs)