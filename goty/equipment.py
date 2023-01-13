import arcade
from goty.constants import *
from goty.entity import Entity


def get_equip_names(eq_list):
    return [eq_name + str(i).zfill(2)
     for i in range(1,9)
     for eq_name in eq_list]


class Equipment(Entity):

    body_items = get_equip_names(['armor', 'robe'])
    accesory_items = get_equip_names(['book', 'shield'])
    head_items = get_equip_names(['helm', 'hat'])

    def __init__(self, equipment_sprite: str, sprite_to_equip: arcade.Sprite):
        super().__init__(equipment_sprite)
        self.equipper = sprite_to_equip

    def update(self):
        self.center_x = int(self.equipper.center_x)
        self.center_y = int(self.equipper.center_y)
        self.facing_direction = self.equipper.facing_direction
        self.update_animation()

    def equip(self):
        raise NotImplementedError("Equipment cannot equip.")

    def wield(self):
        raise NotImplementedError("Equipment cannot wield.")


class Weapon(Equipment):

    def __init__(self, weapon_sprite, sprite_to_wield):
        super().__init__(weapon_sprite, sprite_to_wield)
        self.init_textures()

    def init_textures(self):
        self.idle_texture_pair = self.get_textures("idle_1.png")
        self.idle_texture_pair_2 = self.get_textures("idle_2.png")
        self.weapon_1 = self.get_textures("s_1.png")
        self.weapon_2 = self.get_textures("s_2.png")
        self.weapon_3 = self.get_textures("s_3.png")
        self.weapon_4 = self.get_textures("s_4.png")

    def set_texture(self):
        self.texture = self.idle_texture_pair[self.facing_direction.value]

    def update(self):
        self.facing_direction = self.equipper.facing_direction
        if self.facing_direction == FacingDirection.RIGHT:
            offset = 10
        if self.facing_direction == FacingDirection.LEFT:
            offset = -10
        self.center_x = int(self.equipper.center_x + offset)
        self.center_y = int(self.equipper.center_y)

        self.update_animation()

    def update_animation(self):
        pass
