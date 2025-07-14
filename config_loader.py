import configparser
from datetime import datetime

class Config:
    def __init__(self, path='config.ini'):
        parser = configparser.ConfigParser()
        parser.read(path, encoding='utf-8')
        today = datetime.now().strftime('%Y-%m-%d')
        cfg = parser['DEFAULT']
        self.ASSEMBLY_ID = cfg.get('ASSEMBLY_ID')
        self.ASSEMBLY_PW = cfg.get('ASSEMBLY_PW')
        self.TWO_CAPTCHA_API_KEY = cfg.get('TWO_CAPTCHA_API_KEY')
        self.BASE_URL = cfg.get('BASE_URL')
        self.TODAY_BILLS_URL = cfg.get('TODAY_BILLS_URL').format(today=today)
        self.OPINION_TITLE = cfg.get('OPINION_TITLE')
        self.OPINION_CONTENT = cfg.get('OPINION_CONTENT')
        self.OPINION_LOG_PATH = cfg.get('OPINION_LOG_PATH')

config = Config()