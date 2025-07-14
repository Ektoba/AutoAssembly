from selenium.webdriver.common.by import By
from models import Bill
from config_loader import config

class BillFetcher:
    """오늘 마감 법안 ID 수집 (Assembly 공식 페이지)"""
    def __init__(self, driver):
        self.driver = driver

    def fetch_today_bills(self) -> list[Bill]:
        # 오늘 날짜 문자열 생성
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        # TODAY_BILLS_URL 포맷에 오늘 날짜 삽입
        url = config.TODAY_BILLS_URL.format(today=today)
        self.driver.get(url)
        # 검색 결과 테이블 내 법안 링크 셀렉터 (Assembly 페이지 구조에 맞게 조정 필요)
        elems = self.driver.find_elements(By.CSS_SELECTOR, "table.search-list a[href*='lgsltPaId']")
        ids = {
            elem.get_attribute('href').split('lgsltPaId=')[1].split('&')[0]
            for elem in elems
        }
        return [Bill(id=b) for b in ids]