import json
from pathlib import Path
from config_loader import config

class SubmittedRepository:
    """등록된 법안 ID 저장/조회"""
    def __init__(self):
        self.path = Path(config.OPINION_LOG_PATH)

    def load(self) -> set[str]:
        if self.path.exists():
            return set(json.loads(self.path.read_text()))
        return set()

    def save(self, ids: set[str]):
        self.path.write_text(json.dumps(sorted(ids), ensure_ascii=False))