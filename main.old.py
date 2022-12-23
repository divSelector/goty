import arcade

SCREEN_TITLE = "Game of the Year 2022"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

PLAYER_SCALING = 1.25
TILE_SIZE = 64
TILE_SCALING = 0.5
COIN_SCALING = 0.5

MOVEMENT_SPEED = 5
JUMP_SPEED = 20
GRAVITY = 1

SOUND_OFF = True


class Player(arcade.SpriteSolidColor):

    def __init__(self, width, height, color, move_speed, jump_speed):
        super().__init__(width, height, color)
        self.move_speed = move_speed
        self.jump_speed = jump_speed

    def update(self):
        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
            self.change_x = 0
        #elif self.right > SCREEN_WIDTH - 1:
            #self.right = SCREEN_WIDTH - 1
            #self.change_x = 0
        #if self.bottom < 0:
            #self.bottom = 0
            #self.change_y = 0
        #elif self.top > SCREEN_HEIGHT - 1:
            #self.top = SCREEN_HEIGHT - 1
            #self.change_y = 0


class Game(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.scene = None
        self.physics = None
        self.player = None
        self.camera = None
        self.hud = None

        self.gems = 0

        arcade.set_background_color(
            arcade.color.BLACK
        )

        self.left_pressed = False
        self.right_pressed = False
        self.jump_pressed = False
        self.down_pressed = False

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")


    def center_camera_to_player(self):
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (self.camera.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)

    def setup_player(self, dimensions, position, color):
        """
        Build a prototype rectangle sprite for player from dimensions (width, height), color, and
        position, which is specified in pixels from the left and pixels from bottom.
        PLAYER_SCALING is optionally used if set to something other than 0.
        Sprite is added to a sprite list for optimized draw.
        """
        width, height = dimensions
        if PLAYER_SCALING != 0:
            width = int(width * PLAYER_SCALING)
            height = int(height * PLAYER_SCALING)
        self.player = Player(
            width=width,
            height=height,
            color=color,
            move_speed=MOVEMENT_SPEED,
            jump_speed=JUMP_SPEED
        )
        left, bottom = position
        self.player.left = left
        self.player.bottom = bottom
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite("Player", self.player)
        self.log_user_input()

    def update_player_speed(self):
        print("LOG_USER_INPUT")
        self.log_user_input()

        self.player.change_x = 0

        if self.jump_pressed:
            if self.physics.can_jump():
                self.player.change_y = self.player.jump_speed
                self.play_sound(self.jump_sound)
                self.jump_pressed = False

        elif not self.jump_pressed:
            if not self.physics.can_jump():
                self.player.change_y = self.player.change_y / 2

        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -self.player.move_speed
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = self.player.move_speed

    def setup_level_one(self):
        """Set up the game here. Call this function to start level one."""
        self.camera = arcade.Camera(self.width, self.height)
        self.hud = arcade.Camera(self.width, self.height)
        self.scene = arcade.Scene()

        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        for ground_x in range(0, int(SCREEN_WIDTH * 2 + TILE_SIZE / 2), TILE_SIZE):
            ground = arcade.SpriteSolidColor(TILE_SIZE, TILE_SIZE, arcade.color.GREEN)
            ground.center_x = ground_x
            ground.center_y = TILE_SIZE / 2
            self.scene.add_sprite("Walls", ground)


        crate_locations = [
            (256, 96), (512, 96),  (768, 96),
                       (512, 160), (768, 160),
                                   (768, 224)
        ]

        for coordinate in crate_locations:
            crate = arcade.SpriteSolidColor(TILE_SIZE, TILE_SIZE, arcade.color.BROWN)
            crate.position = coordinate
            self.scene.add_sprite("Walls", crate)

        for coin_x in range(384, int(SCREEN_WIDTH * 2 + TILE_SIZE / 4), 256):
            coin = arcade.SpriteSolidColor(int(TILE_SIZE / 4), int(TILE_SIZE / 4), arcade.color.GOLD)
            coin.center_x = coin_x
            coin.center_y = 320
            self.scene.add_sprite("Coins", coin)

        self.setup_player(
            dimensions=(TILE_SIZE / 2, TILE_SIZE),
            color=arcade.color.WHITE,
            position=(100, TILE_SIZE)
        )

        self.physics = arcade.PhysicsEnginePlatformer(
            self.player,
            gravity_constant=GRAVITY,
            walls=self.scene.get_sprite_list("Walls")
        )

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.Z:
            self.jump_pressed = True
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = True
            #self.update_player_speed()
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
            self.update_player_speed()

        print("PRESSED")
        self.log_user_input()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.Z:
            self.jump_pressed = False
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = False
            #self.update_player_speed()
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
            self.update_player_speed()

        print("RELEASED")
        self.log_user_input()

    def log_user_input(self):
        print(
            f"JUMP: {self.jump_pressed}, DOWN: {self.down_pressed}, "+\
                f"LEFT: {self.left_pressed}, RIGHT: {self.right_pressed}"+\
                    f"\n\tPLAYER POSITION: {self.player.position}"+\
                        f"\n\tPLAYER_CHANGE ({self.player.change_x}, {self.player.change_y})")

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.physics.update()
        self.scene.update()

        coin_hit_list = arcade.check_for_collision_with_list(
            self.player, self.scene.get_sprite_list("Coins")
        )

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.play_sound(self.collect_coin_sound)
            self.gems += 1

        self.center_camera_to_player()

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()
        self.hud.use()

        score_text = f"Gems: {self.gems}"
        arcade.draw_text(
            score_text,
            25, SCREEN_HEIGHT - 25,
            arcade.color.WHITE,
            20,
            font_name="Kenney Blocks"
        )

    def play_sound(self, sound):
        if not SOUND_OFF:
            arcade.play_sound(sound)

def main():
    game = Game(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        SCREEN_TITLE
    )
    game.setup_level_one()
    arcade.run()

if __name__ == "__main__":
    main()


