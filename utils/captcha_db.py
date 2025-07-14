# 파일: utils/captcha_db.py
"""
- 프로그램 실행시 capchar.db(캡차 수동입력 DB)가 없으면 자동 생성
- DB에는 '라벨(정답)', '이미지', '입력일시' 저장 (여러 이미지가 같은 정답을 가질 수 있음)
- TensorFlow 모델 예측시 DB를 먼저 조회하여, 같은 숫자(정답)의 다른 이미지가 있어도 모두 사용 가능
- 실행 파일(pyinstaller로 exe로 빌드 시) 기준 상대경로 사용
"""

import os
import sqlite3
from pathlib import Path

def get_db_path():
    # exe 실행 기준 현재 경로
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "captcha.db")

def init_db():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS captchas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT NOT NULL,
            image BLOB NOT NULL,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_label ON captchas(label)")
    conn.commit()
    conn.close()

def save_captcha(label: str, image_bytes: bytes):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO captchas (label, image) VALUES (?, ?)", (label, image_bytes))
    conn.commit()
    conn.close()

def get_images_by_label(label: str):
    """동일한 정답(label)에 해당하는 여러 이미지가 모두 반환됨."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT image FROM captchas WHERE label=?", (label,))
    images = [row[0] for row in c.fetchall()]
    conn.close()
    return images

# 실행 예시:
if __name__ == "__main__":
    import sys
    init_db()
    # (이미지/라벨 추가, 조회 예시는 필요시 직접 작성)

