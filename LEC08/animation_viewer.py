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


def validate_atlas(data):
    """잘못된 atlas를 렌더러에 넘기지 않고 원인을 명확하게 알려준다."""
    animations = data['animations']
    if len(animations) < 4:
        raise ValueError('At least four animations are required')
    for animation in animations:
        if animation['fps'] <= 0 or not animation['frames']:
            raise ValueError('Each animation needs frames and positive fps')
        for f in animation['frames']:
            if not (f['w'] > 0 and f['h'] > 0 and f['x'] >= 0 and f['y'] >= 0
                    and f['x'] + f['w'] <= data['width']
                    and f['y'] + f['h'] <= data['height']):
                raise ValueError('Frame rectangle lies outside atlas')


def calculate_scale(data):
    """가장 작은 자세도 화면 높이 절반 이상, 큰 자세도 화면 안에."""
    frames = [f for a in data['animations'] for f in a['frames']]
    minimum = min(f['h'] for f in frames)
    scale = max(1, int(CANVAS_HEIGHT * 0.62 / minimum + 0.999))
    return scale


def frame_geometry(frame, scale):
    # atlas는 좌상단 좌표, Pico2D 화면은 좌하단 좌표를 사용한다.
    # 원본의 (32, 32) 피벗을 유지하여 trim 크기가 달라도 흔들리지 않는다.
    x = CANVAS_WIDTH / 2 + (frame['w'] / 2 - frame['pivot_x']) * scale
    y = CANVAS_HEIGHT / 2 + (5 + frame['pivot_y'] - frame['h'] / 2) * scale
    return x, y, frame['w'] * scale, frame['h'] * scale


def draw_character(image, frame, scale):
    bottom = image.h - frame['y'] - frame['h']
    image.clip_draw(frame['x'], bottom, frame['w'], frame['h'],
                    *frame_geometry(frame, scale))


def main():
    import time
    import pico2d as p2d

    data = load_atlas()
    validate_atlas(data)
    player = AnimationPlayer(data['animations'])
    scale = calculate_scale(data)
    p2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        image = p2d.load_image(str(BASE_DIR / 'assets' / data['image']))
        previous = time.perf_counter()
        running = True
        while running:
            for event in p2d.get_events():
                if event.type == p2d.SDL_QUIT or (
                    event.type == p2d.SDL_KEYDOWN and event.key == p2d.SDLK_ESCAPE
                ):
                    running = False
            if not running:
                break
            now = time.perf_counter()
            player.update(now - previous)
            previous = now
            p2d.clear_canvas()
            draw_character(image, player.frame, scale)
            p2d.update_canvas()
            p2d.delay(0.005)
    finally:
        p2d.close_canvas()


if __name__ == '__main__':
    main()
