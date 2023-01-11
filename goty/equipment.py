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
        #super().update()
        self.center_x = int(self.equipper.center_x)
        self.center_y = int(self.equipper.center_y)
        self.facing_direction = self.equipper.facing_direction
        self.update_animation()


