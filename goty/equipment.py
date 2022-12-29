import arcade
from goty.constants import *
from goty.entity import Entity


class Equipment(Entity):
    def __init__(self, equipment_sprite: str, sprite_to_equip: arcade.Sprite):
        super().__init__(equipment_sprite)
        self.equipper = sprite_to_equip

    def update(self):
        self.center_x = self.equipper.center_x
        self.center_y = self.equipper.center_y
        self.facing_direction = self.equipper.facing_direction
        self.update_animation()

    def update_animation(self, delta_time: float = 1 / 60):
        # Jumping animation
        if self.equipper.change_y > 0 and not self.equipper.is_on_ladder:
            self.texture = self.jump_texture_pair[self.facing_direction.value]
            return
        elif self.equipper.change_y < 0 and not self.equipper.is_on_ladder:
            self.texture = self.fall_texture_pair[self.facing_direction.value]
            return

        # Idle animation
        if self.equipper.change_x == 0 and not self.equipper.crouching:
            self.texture = self.idle_texture_pair[self.facing_direction.value]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.equipper.cur_texture // UPDATES_PER_FRAME
        direction = self.facing_direction.value
        self.texture = self.walk_textures[frame][direction]


        # Crouch animation
        if self.equipper.crouching:
            self.texture = self.crouch_texture_pair[self.facing_direction.value]
