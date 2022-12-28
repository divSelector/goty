from enum import Enum

SCREEN_TITLE = "Game of the Year 2022"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

PLAYER_SCALING = 2.5
TILE_SIZE = 64
TILE_SCALING = 0.5
COIN_SCALING = 0.5

MOVEMENT_SPEED = 7
JUMP_SPEED = 20
GRAVITY = 1.1
UPDATES_PER_FRAME = 5

SOUND_OFF = True

class FacingDirection(Enum):
    RIGHT = 0
    LEFT = 1

LEVEL_ONE_MAP = "assets/tilemaps/map.json"
