import arcade
import math
import random
from goty.constants import *
from goty.player import Player
from goty.enemy import RedPantsEnemy, BluePantsEnemy, GreenPantsEnemy, GreyPantsEnemy
from goty.physics import PhysicsEngine
from goty.equipment import Equipment

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
        self.attack_pressed = False

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

    def init_player(self, sprite, position):
        """
        Initializes a player... passes the game, camera, and scene to the player.
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

    def init_enemy(self, enemy_class):
        enemy = enemy_class()
        enemy.game = self
        return enemy


    def setup_level_one(self):
        """Set up the game here. Call this function to start level one."""
        self.camera = arcade.Camera()
        self.hud = arcade.Camera()

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(
            LEVEL_ONE_MAP,
            TILE_SCALING, {
                LAYER_NAME_PLATFORMS: {
                    "use_spatial_hash": True,
            },
        })

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # -- Enemies
        enemies_layer = self.tile_map.object_lists[LAYER_NAME_ENEMIES]


        for enemy_obj in enemies_layer:
            cartesian = self.tile_map.get_cartesian(
                enemy_obj.shape[0], enemy_obj.shape[1]
            )
            enemy_type = enemy_obj.properties["type"]
            if enemy_type == "red_pants":
                enemy = self.init_enemy(RedPantsEnemy)
            elif enemy_type == "green_pants":
                enemy = self.init_enemy(GreenPantsEnemy)
            elif enemy_type == "grey_pants":
                enemy = self.init_enemy(GreyPantsEnemy)
            elif enemy_type == "blue_pants":
                enemy = self.init_enemy(BluePantsEnemy)

            else:
                raise Exception(f"Unknown enemy type {enemy_type}.")
            enemy.left = math.floor(
                cartesian[0] * TILE_SCALING * self.tile_map.tile_width
            )
            enemy.bottom = math.floor(
                (cartesian[1]) * (self.tile_map.tile_height * TILE_SCALING)
            )

            self.scene.add_sprite(LAYER_NAME_ENEMIES, enemy)
            for eq_sprite in [random.choice(Equipment.body_items),
                              random.choice(Equipment.accesory_items),
                              random.choice(Equipment.head_items)]:
                self.scene.add_sprite(LAYER_NAME_ENEMIES, enemy.equip(eq_sprite))


        self.init_player(
            sprite="player",
            position=(TILE_SIZE, TILE_SIZE * 4)
        )

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        self.physics = PhysicsEngine(
            self.player,
            gravity_constant=GRAVITY,
            walls=self.scene.get_sprite_list(LAYER_NAME_PLATFORMS),
            enemy_sprites=self.scene.get_sprite_list(LAYER_NAME_ENEMIES)
        )


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.Z:
            self.jump_pressed = True
            self.player.jump()
        if key == arcade.key.X:
            self.attack_pressed = True
            self.player.attack()
        if key == arcade.key.DOWN:
            self.down_pressed = True
            self.player.crouch()
        if key in [arcade.key.LEFT, arcade.key.A]:
            self.left_pressed = True
            self.player.walk()
        if key in [arcade.key.RIGHT, arcade.key.D]:
            self.right_pressed = True
            self.player.walk()

        print("PRESSED")
        self.log_user_input()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.Z:
            self.jump_pressed = False
            #self.player.jump()
            self.player.jumping = False
        if key == arcade.key.X:
            self.attack_pressed = False
            self.player.attacking = False
            self.player.update_movement_speed()
        if key == arcade.key.DOWN:
            self.down_pressed = False
            #self.player.crouch()
            self.player.crouching = False
        if key in [arcade.key.LEFT, arcade.key.A]:
            self.left_pressed = False
            self.player.update_movement_speed()
        if key in [arcade.key.RIGHT, arcade.key.D]:
            self.right_pressed = False
            self.player.update_movement_speed()

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
            print(coin.properties)
            # Figure out how many points this coin is worth
            if "Points" not in coin.properties:
                print("Warning, collected a coin without a Points property.")
            else:
                points = int(coin.properties["Points"])
                self.gems += points

            coin.remove_from_sprite_lists()
            self.play_sound(self.collect_coin_sound)

        self.player.center_camera()

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw(pixelated=True)
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
                    f"\nATTACK: {self.attack_pressed}"
                    f"\n\tPLAYER POSITION: {self.player.position}"+\
                        f"\n\tPLAYER_CHANGE ({self.player.change_x}, {self.player.change_y})"+\
                            f"\n\tIS_CROUCHING: {self.player.crouching}"+\
                                f"\n\tIS_ATTACK: {self.player.attacking}"+\
                                    f"\n\tIS_WALKING: {self.player.walking}"+\
                                         f"\n\tIS_JUMPINH: {self.player.jumping}"+\
                                    "")

if __name__ == "__main__":
    pass

