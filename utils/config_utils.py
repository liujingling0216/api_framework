import os
import configparser

config_file_path = os.path.join(os.path.dirname(__file__),'../conf/localconfig.ini')

class ConfigUtils():
    def __init__(self,configpath=config_file_path):
        self.conf = configparser.ConfigParser()
        self.conf.read(configpath,encoding='utf-8')

    @property
    def get_url(self):
        url = self.conf.get('default','url')
        return url

config = ConfigUtils()

if __name__ == '__main__':
    print(config.get_url)





