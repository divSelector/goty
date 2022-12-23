import arcade

class Player(arcade.SpriteSolidColor):

    def __init__(self, width, height, color, move_speed, jump_speed):
        super().__init__(width, height, color)
        self.move_speed = move_speed
        self.jump_speed = jump_speed

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

    def move(self):
        self.change_x = 0

        if self.game.jump_pressed:
            if self.game.physics.can_jump():
                self.change_y = self.jump_speed
                self.game.play_sound(self.game.jump_sound)
                self.game.jump_pressed = False

        elif not self.game.jump_pressed:
            if not self.game.physics.can_jump():
                self.change_y = self.change_y / 2

        if self.game.left_pressed and not self.game.right_pressed:
            self.change_x = -self.move_speed
        elif self.game.right_pressed and not self.game.left_pressed:
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
