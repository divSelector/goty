import arcade

from constants import *
from player import Player

class Game(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.scene = None
        self.physics = None
        self.player = None
        self.camera = None
        self.hud = None
        self.tile_map = None

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

    #def init_player(self, dimensions, position, color):
        #"""
        #Build a prototype rectangle sprite for player from dimensions (width, height), color, and
        #position, which is specified in pixels from the left and pixels from bottom.
        #"""
        #width, height = dimensions
        #width = int(width * PLAYER_SCALING)
        #height = int(height * PLAYER_SCALING)
        #self.player = Player(
            #width=width, height=height, color=color,
            #move_speed=MOVEMENT_SPEED, jump_speed=JUMP_SPEED
        #)
        #self.player.game = self
        #self.player.scene = self.scene
        #self.player.camera = self.camera
        #self.player.setup(position)

    def init_player(self, sprite, position):
        """
        Build a prototype rectangle sprite for player from dimensions (width, height), color, and
        position, which is specified in pixels from the left and pixels from bottom.
        """
        self.player = Player(
            sprite=sprite,
            move_speed=MOVEMENT_SPEED,
            jump_speed=JUMP_SPEED
        )
        self.player.game = self
        self.player.scene = self.scene
        self.player.camera = self.camera
        self.player.setup(position)

    def setup_level_one(self):
        """Set up the game here. Call this function to start level one."""
        self.camera = arcade.Camera(self.width, self.height)
        self.hud = arcade.Camera(self.width, self.height)

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(
            ":resources:tiled_maps/map.json",
            TILE_SCALING, {
                "Platforms": {
                    "use_spatial_hash": True,
            },
        })

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        #self.init_player(
            #dimensions=(TILE_SIZE / 2, TILE_SIZE),
            #color=arcade.color.WHITE,
            #position=(100, TILE_SIZE)
        #)
        self.init_player(
            sprite="player",
            position=(100, TILE_SIZE)
        )

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        self.physics = arcade.PhysicsEnginePlatformer(
            self.player,
            gravity_constant=GRAVITY,
            walls=self.scene.get_sprite_list("Platforms")
        )

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.Z:
            self.jump_pressed = True
            self.player.jump()
        elif key == arcade.key.DOWN:
            self.down_pressed = True
            #self.player.move()
        elif key in [arcade.key.LEFT, arcade.key.A]:
            self.left_pressed = True
            self.player.walk()
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.right_pressed = True
            self.player.walk()

        print("PRESSED")
        self.log_user_input()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.Z:
            self.jump_pressed = False
            self.player.jump()
        elif key == arcade.key.DOWN:
            self.down_pressed = False
            #self.player.move()
        elif key in [arcade.key.LEFT, arcade.key.A]:
            self.left_pressed = False
            self.player.walk()
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.right_pressed = False
            self.player.walk()

        print("RELEASED")
        self.log_user_input()

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.physics.update()
        self.scene.update()
        self.player.update_animation(delta_time)

        coin_hit_list = arcade.check_for_collision_with_list(
            self.player, self.scene.get_sprite_list("Coins")
        )

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.play_sound(self.collect_coin_sound)
            self.gems += 1

        self.player.center_camera()

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

    def log_user_input(self):
        print(
            f"JUMP: {self.jump_pressed}, DOWN: {self.down_pressed}, "+\
                f"LEFT: {self.left_pressed}, RIGHT: {self.right_pressed}"+\
                    f"\n\tPLAYER POSITION: {self.player.position}"+\
                        f"\n\tPLAYER_CHANGE ({self.player.change_x}, {self.player.change_y})")

if __name__ == "__main__":
    pass

