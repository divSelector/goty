import arcade
from goty.constants import *
from goty.entity import Entity


class Enemy(Entity):

    def __init__(self, sprite):
        super().__init__(sprite)

    def face_player(self):
        if self.game.player.center_x < self.center_x:
            self.facing_direction = FacingDirection.LEFT
        elif self.game.player.center_x > self.center_x:
            self.facing_direction = FacingDirection.RIGHT
        self.texture = self.idle_texture_pair[self.facing_direction.value]

    def update(self):
        self.face_player()


class RedPantsEnemy(Enemy):

    def __init__(self):
        super().__init__("player-redpants")

class GreenPantsEnemy(Enemy):

    def __init__(self):
        super().__init__("player-greenpants")

class GreyPantsEnemy(Enemy):

    def __init__(self):
        super().__init__("player-greypants")

class BluePantsEnemy(Enemy):

    def __init__(self):
        super().__init__("player")
