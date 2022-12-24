import sys
from PIL import Image
from pathlib import Path
from enum import Enum

_, filename = sys.argv

NUM_ROWS = 4
NUM_COLS = 8
SPRITE_WIDTH = 46
SPRITE_HEIGHT = 50

class SpriteFrame(Enum):
    STAND_IDLE = 1
    CROUCH_IDLE = 2
    STAND_ATTACK_1 = 3
    STAND_ATTACK_2 = 4
    STAND_ATTACK_3 = 5
    STAND_ATTACK_4 = 6
    JUMP_AIR = 7
    JUMP_GROUND = 8
    STAND_DAMAGED = 9
    CROUCH_DAMAGED = 10
    JUMP_ATTACK_1 = 11
    JUMP_ATTACK_2 = 12
    JUMP_ATTACK_3 = 13
    JUMP_ATTACK_4 = 14
    JUMP_DAMAGED = 17
    CROUCH_SLIDE = 18
    CROUCH_ATTACK_1 = 19
    CROUCH_ATTACK_2 = 20
    CROUCH_ATTACK_3 = 21
    CROUCH_ATTACK_4 = 22
    RUN_1 = 25
    RUN_2 = 26
    RUN_3 = 27
    RUN_4 = 28
    RUN_5 = 29
    RUN_6 = 30
    RUN_7 = 31
    RUN_8 = 32

    def to_filename(self):
        return f"{self.name.lower()}.png"


sprite_map_path = Path(filename)
name = sprite_map_path.stem
sprite_dir = Path.cwd() / name
if not sprite_dir.exists():
    sprite_dir.mkdir()
sheet = Image.open(sprite_map_path)
count = 1
for y in range(NUM_ROWS):
    for x in range(NUM_COLS):
        a = (x + 1) * SPRITE_WIDTH
        b = (y + 1) * SPRITE_HEIGHT
        sprite = sheet.crop((
            a - SPRITE_WIDTH,
             b - SPRITE_HEIGHT,
             a, b
        ))
        try:
            sprite.save(
                sprite_dir / SpriteFrame(count).to_filename()
            )
        except ValueError:
            pass
        count += 1
