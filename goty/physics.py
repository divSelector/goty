from typing import Iterable, List, Optional, Union

from arcade import (Sprite, SpriteList, check_for_collision,
                    check_for_collision_with_lists, get_distance)
from arcade.physics_engines import PhysicsEnginePlatformer, _move_sprite

class PhysicsEngine(PhysicsEnginePlatformer):
    def __init__(self,
                player_sprite: Sprite,
                platforms: Optional[Union[SpriteList, Iterable[SpriteList]]] = None,
                gravity_constant: float = 0.5,
                ladders: Optional[Union[SpriteList, Iterable[SpriteList]]] = None,
                walls: Optional[Union[SpriteList, Iterable[SpriteList]]] = None,
                enemy_sprites: Optional[Union[SpriteList, Iterable[SpriteList]]] = None
                ):
        """
        Create a physics engine for a platformer.
        """
        self.ladders: Optional[List[SpriteList]]
        self.platforms: List[SpriteList]
        self.walls: List[SpriteList]

        if ladders:
            self.ladders = [ladders] if isinstance(ladders, SpriteList) else list(ladders)
        else:
            self.ladders = None

        if platforms:
            if isinstance(platforms, SpriteList):
                self.platforms = [platforms]
            else:
                self.platforms = list(platforms)
        else:
            self.platforms = []

        if walls:
            self.walls = [walls] if isinstance(walls, SpriteList) else list(walls)
        else:
            self.walls = []

        if enemy_sprites:
            self.enemies = [enemy_sprites] if isinstance(enemy_sprites, SpriteList) else list(enemy_sprites)
        else:
            self.enemies = []

        self.player_sprite: Sprite = player_sprite
        self.gravity_constant: float = gravity_constant
        self.jumps_since_ground: int = 0
        self.allowed_jumps: int = 1
        self.allow_multi_jump: bool = False

    def update(self):
        """
        Move everything and resolve collisions.
        :Returns: SpriteList with all sprites contacted. Empty list if no sprites.
        """
        # start_time = time.time()
        # print(f"Spot A ({self.player_sprite.center_x}, {self.player_sprite.center_y})")

        # --- Add gravity if we aren't on a ladder
        if not self.is_on_ladder():
            self.player_sprite.change_y -= self.gravity_constant

        enemy_hit_list = []
        for enemy_list in self.enemies:
            for enemy in enemy_list:
                enemy.change_y -= self.gravity_constant
                enemy_hit_list.append(
                    _move_sprite(enemy, self.walls + self.platforms, ramp_up=True)
                )


            # print(f"Spot F ({self.player_sprite.center_x}, {self.player_sprite.center_y})")

        # print(f"Spot B ({self.player_sprite.center_x}, {self.player_sprite.center_y})")

        player_hit_list = _move_sprite(self.player_sprite, self.walls + self.platforms, ramp_up=True)
        complete_hit_list = player_hit_list + enemy_hit_list


        for platform_list in self.platforms:
            for platform in platform_list:
                if platform.change_x != 0 or platform.change_y != 0:

                    # Check x boundaries and move the platform in x direction
                    if platform.boundary_left and platform.left <= platform.boundary_left:
                        platform.left = platform.boundary_left
                        if platform.change_x < 0:
                            platform.change_x *= -1

                    if platform.boundary_right and platform.right >= platform.boundary_right:
                        platform.right = platform.boundary_right
                        if platform.change_x > 0:
                            platform.change_x *= -1

                    platform.center_x += platform.change_x

                    # Check y boundaries and move the platform in y direction
                    if platform.boundary_top is not None \
                            and platform.top >= platform.boundary_top:
                        platform.top = platform.boundary_top
                        if platform.change_y > 0:
                            platform.change_y *= -1

                    if platform.boundary_bottom is not None \
                            and platform.bottom <= platform.boundary_bottom:
                        platform.bottom = platform.boundary_bottom
                        if platform.change_y < 0:
                            platform.change_y *= -1

                    platform.center_y += platform.change_y

        # print(f"Spot Z ({self.player_sprite.center_x}, {self.player_sprite.center_y})")
        # Return list of encountered sprites
        # end_time = time.time()
        # print(f"Update - {end_time - start_time:7.4f}\n")

        return complete_hit_list
