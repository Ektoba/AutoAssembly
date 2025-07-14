# 파일: utils/captcha_handler.py
"""
- TensorFlow 예측(모델 사용) → 결과 없거나 신뢰도 낮으면, DB에 이미지+정답 저장
- DB에서 같은 정답의 다른 이미지도 학습 데이터로 활용 가능
- 실행파일(exe) 기준 상대경로로 DB/모델을 모두 처리
"""

import sys
import os
from PIL import Image
import numpy as np
import tensorflow as tf
from utils.captcha_db import get_db_path, init_db, save_captcha, get_images_by_label

MODEL_PATH = os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), "model", "weights.h5")

class CaptchaHandler:
    def __init__(self):
        self.model = None
        if os.path.exists(MODEL_PATH):
            self.model = tf.keras.models.load_model(MODEL_PATH)
        # DB 초기화(없으면 생성)
        init_db()

    def predict(self, img_pil):
        if not self.model:
            return None
        x = np.array(img_pil.convert("L").resize((120, 40))) / 255.0
        x = x.reshape((1, 40, 120, 1))
        pred = self.model.predict(x)
        chars = "0123456789abcdefghijklmnopqrstuvwxyz"
        pred_str = ""
        for out in pred:
            pred_str += chars[np.argmax(out)]
        return pred_str

    def process_captcha(self, img_pil):
        """자동예측 → 없거나 신뢰도↓면 수동입력, 입력/라벨 모두 DB에 누적"""
        pred = self.predict(img_pil)
        if pred and self.check_confidence(pred):
            return pred
        img_pil.show()
        code = input("캡차를 직접 입력하세요: ")
        # 이미지+정답 DB에 저장
        import io
        with io.BytesIO() as buf:
            img_pil.save(buf, format='PNG')
            save_captcha(code, buf.getvalue())
        return code

    def check_confidence(self, pred):
        # 신뢰도 로직(임계치 등) 구현, 필요시 수정
        return False

