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


class AnimationPlayer:
    """그래픽 창 없이도 검증할 수 있는 애니메이션 재생 상태."""
    def __init__(self, animations):
        self.animations = animations
        self.animation_index = 0
        self.frame_index = 0
        self.elapsed = 0.0
        self.completed_loops = 0
        self.paused = False

    @property
    def animation(self):
        return self.animations[self.animation_index]

    @property
    def frame(self):
        return self.animation['frames'][self.frame_index]

    def update(self, dt):
        """5회 반복 → 마지막 프레임에서 1초 정지. 남은 시간도 보존한다."""
        if dt < 0:
            raise ValueError('dt must be nonnegative')
        self.elapsed += dt
        while True:
            duration = PAUSE_SECONDS if self.paused else 1.0 / self.animation['fps']
            if self.elapsed + 1e-10 < duration:
                break
            self.elapsed = max(0.0, self.elapsed - duration)
            if self.paused:
                self.animation_index = (self.animation_index + 1) % len(self.animations)
                self.paused = False
                self.completed_loops = 0
                self.frame_index = 0
                continue
            self.frame_index += 1
            if self.frame_index >= len(self.animation['frames']):
                self.completed_loops += 1
                if self.completed_loops == REPEAT_COUNT:
                    self.paused = True
                    self.frame_index = len(self.animation['frames']) - 1
                else:
                    self.frame_index = 0
