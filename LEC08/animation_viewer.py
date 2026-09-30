"""Drill #8: 시간 기반 Pico2D 애니메이션 뷰어."""
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
CANVAS_WIDTH = 720
CANVAS_HEIGHT = 600
REPEAT_COUNT = 5
PAUSE_SECONDS = 1.0


def load_atlas(path=None):
    """실행 위치에 관계없이 소스 파일 기준으로 메타데이터를 읽는다."""
    path = Path(path) if path is not None else BASE_DIR / "assets/atlas.json"
    return json.loads(path.read_text(encoding="utf-8"))
