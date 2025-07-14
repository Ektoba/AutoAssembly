class CaptchaHandler:
    @staticmethod
    def wait_for_manual_input(driver):
        # CAPTCHA 필드 포커스 유도 (필요 시)
        try:
            field = driver.find_element_by_name('captchaField')
            field.click()
        except:
            pass
        input('CAPTCHA 입력 후 Enter 키를 눌러 계속합니다...')