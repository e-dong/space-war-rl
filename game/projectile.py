"""Collection of classes for weapons"""

import math

import pygame
from pygame import Surface

from game.base import SpaceEntity
from game.conf import TORPEDO_MAX_FLIGHT_MS, TORPEDO_SPEED


class PhotonTorpedo(SpaceEntity):
    """Represents the photon torpedo object that a ship can fire"""

    def __init__(
        self, start_pos, start_ang, start_vel, projectile_group
    ) -> None:
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
        x_vel += TORPEDO_SPEED * math.cos(self.ang * math.pi / 180)
        y_vel += TORPEDO_SPEED * math.sin(self.ang * math.pi / 180)
        self.vel = (x_vel, y_vel)

        self.projectile_group = projectile_group
        self.start_time = pygame.time.get_ticks()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        # Torpedo needs to be rotated an additional 90 degrees
        # due to the orientation it was originally drawn
        self.image = pygame.transform.rotate(self.surf, -(self.ang + 90))
        self.rect = self.image.get_rect(center=self.pos)
        # group and collision management
        flight_time = pygame.time.get_ticks() - self.start_time
        if flight_time > TORPEDO_MAX_FLIGHT_MS:
            self.projectile_group.remove(self)

        for projectile in self.projectile_group.sprites():
            if projectile != self and self.rect.colliderect(projectile.rect):
                self.projectile_group.remove(projectile)
                self.projectile_group.remove(self)
