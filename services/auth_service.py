from selenium.webdriver.common.by import By
from config_loader import config
from utils.captcha_handler import CaptchaHandler

class AuthService:
    """로그인 처리 (단일 책임)"""
    def __init__(self, driver):
        self.driver = driver

    def login(self):
        # 로그인 페이지 접속
        self.driver.get(f"{config.BASE_URL.replace('pal.', 'member.')}/login/loginPage.do")
        # 필드명: loginId, loginPwd
        self.driver.find_element(By.NAME, 'loginId').send_keys(config.ASSEMBLY_ID)
        self.driver.find_element(By.NAME, 'loginPwd').send_keys(config.ASSEMBLY_PW)
        # CAPTCHA 대기
        CaptchaHandler.wait_for_manual_input(self.driver)
        # 로그인 버튼 클릭
        self.driver.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()