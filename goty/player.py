import arcade
from goty.constants import *
from goty.entity import Entity


class Player(Entity):

    def __init__(self, sprite, move_speed, jump_speed):
        super().__init__(sprite)
        self.move_speed = move_speed
        self.jump_speed = jump_speed
        self.facing_direction = FacingDirection.RIGHT

    def setup(self, position):
        left, bottom = position
        self.left = left
        self.bottom = bottom
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite("Player", self)
        for eq_sprite in ["robe01", "hat02", "book02"]:
            self.scene.add_sprite("Player", self.equip(eq_sprite))

    def update(self):
        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
            self.change_x = 0

        self.left = int(self.left)
        self.bottom = int(self.bottom)

    def walk(self):
        self.change_x = 0

        if self.game.left_pressed and not self.game.right_pressed and not self.crouching:
            self.change_x = -self.move_speed
        elif self.game.right_pressed and not self.game.left_pressed and not self.crouching:
            self.change_x = self.move_speed

        # Handle Change Direction While Crouching
        elif self.game.left_pressed and not self.game.right_pressed and self.crouching:
            self.facing_direction = FacingDirection.LEFT
        elif self.game.right_pressed and not self.game.left_pressed and self.crouching:
            self.facing_direction = FacingDirection.RIGHT

    def jump(self):
        if self.game.jump_pressed:
            if self.game.physics.can_jump() and not self.jumping:
                self.change_y = self.jump_speed
                self.game.play_sound(self.game.jump_sound)
                self.jumping = True

        elif not self.game.jump_pressed:
            if not self.game.physics.can_jump():
                self.change_y = self.change_y / 2

    def crouch(self):
        if self.game.down_pressed:
            if self.game.physics.can_jump() and not self.jumping:
                self.change_x = 0
                # TODO crouching hit box change logic
                self.crouching = True
        elif not self.game.down_pressed and self.game.left_pressed:
            self.change_x = -self.move_speed
        elif not self.game.down_pressed and self.game.right_pressed:
            self.change_x = self.move_speed

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
