from selenium.webdriver.common.by import By
from config_loader import config
from models import Opinion
from utils.captcha_handler import CaptchaHandler

class OpinionService:
    """단일 법안 의견 등록"""
    def __init__(self, driver):
        self.driver = driver

    def submit(self, opinion: Opinion) -> bool:
        url = f"{config.BASE_URL}/napal/search/lgsltpaSearch/view.do?lgsltPaId={opinion.bill_id}"
        self.driver.get(url)
        form = self.driver.find_element(By.ID, 'frm')
        self.driver.find_element(By.CSS_SELECTOR, "input[name='delYn'][value='Y']").click()
        self.driver.find_element(By.NAME, 'sj').send_keys(opinion.title)
        self.driver.find_element(By.NAME, 'cn').send_keys(opinion.content)
        CaptchaHandler.wait_for_manual_input(self.driver)
        form.submit()
        return True