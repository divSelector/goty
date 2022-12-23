import arcade

from constants import SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT
from game import Game

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


