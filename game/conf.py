"""Constants / Confguration for game"""
from enum import Enum


class WEAPON(Enum):
    TORPEDO, PHASER = range(2)


# limits FPS to 60
MAX_FPS = 60
# screen dimensions for pygame window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# The delay in ms to check user input
CHECK_KEYS_TIME_DELAY_MS = 100
# The delay in ms to check firing weapons
WEAPON_FIRE_TIME_DEPLAY_MS = 150
# The max time in ms a torpedo is allowed to fly for
TORPEDO_MAX_FLIGHT_MS = 10000
TORPEDO_SPEED = 4
# The max number of concurrent torpedoes a ship can fire
MAX_TORPEDOES_PER_SHIP = 7
