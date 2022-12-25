import arcade
from goty.constants import *
from goty.entity import Entity


class Player(Entity):

    def __init__(self, sprite, move_speed, jump_speed):
        super().__init__(sprite)
        self.move_speed = move_speed
        self.jump_speed = jump_speed

        self.jumping = False
        self.is_on_ladder = False

    def setup(self, position):
        left, bottom = position
        self.left = left
        self.bottom = bottom
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite("Player", self)

    def update(self):
        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
            self.change_x = 0

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
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction.value]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.facing_direction.value]

    def walk(self):
        self.change_x = 0

        if self.game.left_pressed and not self.game.right_pressed:
            self.change_x = -self.move_speed
        elif self.game.right_pressed and not self.game.left_pressed:
            self.change_x = self.move_speed

    def jump(self):
        if self.game.jump_pressed:
            if self.game.physics.can_jump() and not self.jumping:
                self.change_y = self.jump_speed
                self.game.play_sound(self.game.jump_sound)
                #self.game.jump_pressed = False
                self.jumping = True

        elif not self.game.jump_pressed:
            if not self.game.physics.can_jump():
                self.change_y = self.change_y / 2

    def center_camera(self):
        screen_center_x = self.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.center_y - (self.camera.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)

if __name__ == "__main__":
    pass
