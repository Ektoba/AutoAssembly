from config_loader import config
from services.driver_manager import DriverManager
from services.auth_service import AuthService
from services.bill_fetcher import BillFetcher
from services.opinion_service import OpinionService
from repository.submitted_repo import SubmittedRepository


def main():
    # 설정 파일은 프로젝트 루트의 config.ini 를 통해 초기화된 config 객체를 사용합니다.
    dm = DriverManager(headless=False)
    driver = dm.get_driver()
    try:
        # 로그인
        AuthService(driver).login()
        # 법안 수집
        bills = BillFetcher(driver).fetch_today_bills()
        repo = SubmittedRepository()
        submitted = repo.load()
        # 의견 제출
        for bill in bills:
            if bill.id in submitted:
                continue
            from models import Opinion
            opinion = Opinion(
                bill_id=bill.id,
                title=config.OPINION_TITLE,
                content=config.OPINION_CONTENT
            )
            OpinionService(driver).submit(opinion)
            submitted.add(bill.id)
            repo.save(submitted)
    finally:
        dm.quit()

if __name__ == '__main__':
    main()