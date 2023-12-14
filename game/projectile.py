"""Collection of classes for weapons"""

import math

import pygame
from pygame import Surface

from game.base import SpaceEntity

# TODO Add timeout, so torpedoes don't stay on the screen forever

class PhotonTorpedo(SpaceEntity):
    """Represents the photon torpedo object that a ship can fire"""

    def __init__(self, start_pos, start_ang, start_vel) -> None:
        surf = Surface([12, 12]).convert_alpha()
        super().__init__(surf, start_pos, start_ang, start_vel)

        # Draw on the surface of what the torpedo looks like
        pygame.draw.polygon(self.image, "white", [[5, 0], [3, 5], [7, 5]], 1)
        pygame.draw.polygon(self.image, "white", [[0, 10], [3, 9], [3, 5]], 1)
        pygame.draw.polygon(self.image, "white", [[7, 5], [7, 9], [11, 10]], 1)
        pygame.draw.line(self.image, "white", (3, 9), (7, 9))
        pygame.draw.line(self.image, "white", (5, 5), (5, 11))

        # Apply torpedoes velocity on ship's velocity
        x_vel, y_vel = self.vel
        x_vel += 3 * math.cos(self.ang * math.pi / 180)
        y_vel += 3 * math.sin(self.ang * math.pi / 180)
        self.vel = (x_vel, y_vel)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        # Torpedo needs to be rotated an additional 90 degrees
        # due to the orientation it was originally drawn
        self.image = pygame.transform.rotate(self.surf, -(self.ang + 90))
        self.rect = self.image.get_rect(center=self.pos)
