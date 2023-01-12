import sys
from PIL import Image
from pathlib import Path
from enum import Enum

_, filename = sys.argv

NUM_ROWS = 4
NUM_COLS = 8
SPRITE_WIDTH = 46
SPRITE_HEIGHT = 50

def add_margin(pil_img,
               top=0,
               right=0,
               bottom=0,
               left=0,
               color=(255, 0, 0, 0)):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new("RGBA", (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result


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


COPY_FROM = {3: 11, 4: 12, 5: 13, 6: 14}
paste_data = {}


sprite_map_path = Path(filename)
sprite_dir = Path.cwd() / sprite_map_path.stem
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
        new_sprite = add_margin(sprite, top=4)
        try:
            new_sprite.save(
                sprite_dir / SpriteFrame(count).to_filename()
            )
        except ValueError:
            pass
        count += 1

if filename[0:3] in ['helm', 'hat']:
    stand_attack_imgs = [
        Image.open(
            sprite_dir / SpriteFrame(n).to_filename()
        ) for n in range(3, 7)
    ]

    stand_attack_bottom_copies = [
        sprite.crop((0,50,46,54))
        for sprite in stand_attack_imgs
    ]

    stand_attack_top_copies = [
        sprite.crop((0,0,46,50))
        for sprite in stand_attack_imgs
    ]

    jump_attack_imgs = [
        Image.open(
            sprite_dir / SpriteFrame(n).to_filename()
        ) for n in range(11, 15)
    ]

    for idx, top_bottom in enumerate(zip(stand_attack_bottom_copies, jump_attack_imgs)):
        top, bottom = top_bottom
        new = Image.new("RGBA", bottom.size, (255,0,0,0))
        new.paste(bottom)
        new.paste(top)
        new.save(sprite_dir / f'jump_attack_{idx+1}.png')

    for idx, sprite in enumerate(stand_attack_top_copies):
        new_sprite = add_margin(sprite, bottom=4)
        new_sprite.save(sprite_dir / f'stand_attack_{idx+1}.png')
