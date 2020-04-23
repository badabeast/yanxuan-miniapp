from configparser import ConfigParser
import os
# from designpattern import Singleton

class InIReader(ConfigParser):
    def __init__(self, filepath, parent=None):
        super(InIReader, self).__init__(parent)
        # self.configfile = os.path.join(os.getcwd(),'conf','conf.ini')
        self.config = ConfigParser()
        self.config.read(filepath,encoding="utf-8")

if __name__ == "__main__":
    configfile = os.path.join(os.getcwd(),"conf","conf.ini")
    c = ConfigParser()
    c.read(configfile,encoding="utf-8")
    # config = InIReader(configfile).config
    print(c.get('mongodb','port'))