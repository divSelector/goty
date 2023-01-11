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
        super().update()
        self.center_x = int(self.equipper.center_x)
        self.center_y = int(self.equipper.center_y)
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
        self.cur_walk_texture += 1
        if self.cur_walk_texture > 7 * UPDATES_PER_FRAME:
            self.cur_walk_texture = 0
        frame = self.equipper.cur_walk_texture // UPDATES_PER_FRAME
        direction = self.facing_direction.value
        self.texture = self.walk_textures[frame][direction]


        # Crouch animation
        if self.equipper.crouching:
            self.texture = self.crouch_texture_pair[self.facing_direction.value]


        ## Attack animation
        #if self.equipper.attacking:
            #if self.equipper.crouching:
                #attack_textures = self.crouch_attack_textures
            #elif self.equipper.jumping:
                #attack_textures = self.jump_attack_textures
            #else:
                #attack_textures = self.stand_attack_textures
            #self.cur_attack_texture += 1
            #if self.cur_attack_texture > 3 * UPDATES_PER_FRAME:
                #self.cur_attack_texture = 0
            #frame = self.equipper.cur_attack_texture // UPDATES_PER_FRAME
            #direction = self.facing_direction.value
            #self.texture = attack_textures[frame][direction]

