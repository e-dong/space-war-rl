"""Constants / Configuration for game"""
from enum import Enum
from typing import TypedDict

import pygame

# TODO: Replace this config with hydra yml configuration


class SpaceEntityType(Enum):
    """Simple enum to determine the space entity type"""

    SHIP, TORPEDO, PHASER = range(3)


SpriteConfig = TypedDict(
    "SpriteConfig",
    {
        "id": str,
        "sprite": pygame.sprite.Sprite,
        "group": pygame.sprite.GroupSingle,
    },
)


# limits FPS to 60
MAX_FPS = 60
# screen dimensions for pygame window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# The delay in ms to check user movement (e.g. acceleration and rotation)
MOVEMENT_TIME_DELAY_MS = 100
# The cooldown period before firing phasers again
PHASER_FIRE_CD = 300
PHASER_MAX_FLIGHT_MS = 50
PHASER_LENGTH = 150
PHASER_WIDTH = 1
# The cooldown period before firing torpedoes again
TORPEDO_FIRE_CD = 100
# The max time in ms a torpedo is allowed to fly for
TORPEDO_MAX_FLIGHT_MS = 10000
TORPEDO_SPEED = 3.5
# The max number of concurrent torpedoes a ship can fire
MAX_TORPEDOES_PER_SHIP = 7