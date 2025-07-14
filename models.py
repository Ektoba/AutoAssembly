"""
도메인 모델 정의
"""
from dataclasses import dataclass

@dataclass
class Bill:
    id: str

@dataclass
class Opinion:
    bill_id: str
    title: str
    content: str
    oppose: bool = True