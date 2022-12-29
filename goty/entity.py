import arcade
from goty.constants import *


class Entity(arcade.Sprite):
    PATH_SPRITES = "assets/sprites"

    def __init__(self, sprite):
        super().__init__()
        self.sprite_name = sprite
        self.facing_direction = FacingDirection.RIGHT

        # Used for image sequences
        self.cur_texture = 0
        self.scale = PLAYER_SCALING
        self.animations = {}

        self.equip_textures = []
        self.idle_texture_pair = self.get_textures("stand_idle.png")
        self.stand_damaged_texture_pair = self.get_textures("stand_damaged.png")
        self.jump_texture_pair = self.get_textures("jump_air.png")
        self.fall_texture_pair = self.get_textures("jump_ground.png")
        self.jump_damaged_texture_pair = self.get_textures("jump_damaged.png")
        self.crouch_texture_pair = self.get_textures("crouch_idle.png")
        self.crouch_slide_texture_pair = self.get_textures("crouch_slide.png")
        self.crouch_damaged_texture_pair = self.get_textures("crouch_damaged.png")
        self.walk_textures = self.get_textures((
            "run_1.png", "run_2.png", "run_3.png", "run_4.png",
            "run_5.png", "run_6.png", "run_7.png", "run_8.png"
        ))
        self.stand_attack_textures = self.get_textures((
            "stand_attack_1.png", "stand_attack_2.png",
            "stand_attack_3.png", "stand_attack_4.png"
        ))
        self.jump_attack_textures = self.get_textures((
            "jump_attack_1.png", "jump_attack_2.png",
            "jump_attack_3.png", "jump_attack_4.png"
        ))
        self.crouch_attack_textures = self.get_textures((
            "crouch_attack_1.png", "crouch_attack_2.png",
            "crouch_attack_3.png", "crouch_attack_4.png"
        ))

        # Set the initial texture
        self.texture = self.idle_texture_pair[self.facing_direction.value]

        ## Hit box will be set based on the first image used. If you want to specify
        ## a different hit box, you can do it like the code below.
        ## self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        #self.set_hit_box(self.texture.hit_box_points)


    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == FacingDirection.RIGHT:
            self.facing_direction = FacingDirection.LEFT
        elif self.change_x > 0 and self.facing_direction == FacingDirection.LEFT:
            self.facing_direction = FacingDirection.RIGHT

        # Jumping animation
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.facing_direction.value]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.facing_direction.value]
            return

        # Idle animation
        if self.change_x == 0 and not self.crouching:
            self.texture = self.idle_texture_pair[self.facing_direction.value]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.facing_direction.value
        self.texture = self.walk_textures[frame][direction]

        # Crouch animation
        if self.crouching:
            self.texture = self.crouch_texture_pair[self.facing_direction.value]

    def get_textures(self, value):
        def get_pair(filename):
            return (
                arcade.load_texture(filename),
                arcade.load_texture(filename, flipped_horizontally=True)
            )
        folder = f"{Entity.PATH_SPRITES}/{self.sprite_name}"
        if isinstance(value, str):
            return get_pair(f"{folder}/{value}")
        elif isinstance(value, tuple):
            return [get_pair(f"{folder}/{fn}") for fn in value]

    def equip(self, equip_name):
        return Equipment(equip_name, self)



class Equipment(Entity):
    def __init__(self, equipment_sprite: str, sprite_to_equip: arcade.Sprite):
        super().__init__(equipment_sprite)
        self.equipped_by = sprite_to_equip
        self.left = self.equipped_by.left
        self.bottom = self.equipped_by.bottom
        self.facing_direction = self.equipped_by.facing_direction
        self.texture = self.idle_texture_pair[self.facing_direction.value]

