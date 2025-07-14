from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class DriverManager:
    """웹드라이버 초기화 및 종료"""
    def __init__(self, headless: bool = False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options)
        self.driver.implicitly_wait(10)

    def get_driver(self):
        return self.driver

    def quit(self):
        self.driver.quit()