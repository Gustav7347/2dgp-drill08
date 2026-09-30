"""원본 PNG의 투명 여백을 잘라 가변 크기 atlas + 피벗 메타데이터 생성.
재생할 때는 Pillow 불필요. 재생성할 때만: python -m pip install Pillow
"""
from pathlib import Path
import json
from PIL import Image

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
SPECS = [
    ('Idle', 'Idle.png', 64, 8, 8),
    ('Run', 'Walking_Right.png', 64, 4, 8),
    ('Melee', 'attack01.png', 80, 5, 10),
    ('Ranged', 'ranged01.png', 80, 4, 8),
]


def build():
    atlas = Image.new('RGBA', (512, 256))
    animations = []
    y = 2
    for name, filename, cell_w, count, fps in SPECS:
        source = Image.open(ASSETS / 'source' / filename).convert('RGBA')
        frames = []
        x, row_height = 2, 0
        for index in range(count):
            cell = source.crop((index * cell_w, 0, (index + 1) * cell_w, 64))
            box = cell.getchannel('A').getbbox()
            if box is None:
                raise ValueError(f'{filename}: empty frame {index}')
            left, top, right, bottom = box
            cropped = cell.crop(box)
            width, height = cropped.size
            if x + width > atlas.width:
                raise ValueError('Atlas row overflow')
            atlas.paste(cropped, (x, y))
            frames.append(dict(x=x, y=y, w=width, h=height,
                               pivot_x=32-left, pivot_y=32-top))
            x += width + 2
            row_height = max(row_height, height)
        animations.append(dict(name=name, fps=fps, frames=frames))
        y += row_height + 2
    atlas = atlas.crop((0, 0, 512, y))
    atlas.save(ASSETS / 'atlas.png')
    data = dict(image='atlas.png', width=atlas.width, height=atlas.height,
                animations=animations)
    (ASSETS / 'atlas.json').write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
    print(f'{len(animations)} animations; {sum(len(a["frames"]) for a in animations)} frames')


if __name__ == '__main__':
    build()
