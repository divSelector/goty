import arcade
from goty.constants import *
from goty.entity import Entity


class Enemy(Entity):

    def __init__(self, sprite):
        super().__init__(sprite)
        self.facing_direction = FacingDirection.LEFT
        self.texture = self.idle_texture_pair[self.facing_direction.value]


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
