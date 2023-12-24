"""Collection of classes for weapons"""

import math

import pygame
from pygame import Surface

from game.base import SpaceEntity
from game.conf import TORPEDO_MAX_FLIGHT_MS, TORPEDO_SPEED, WEAPON


class Phaser(SpaceEntity):
    def __init__(
        self, ship, start_pos, start_ang, start_vel, projectile_group
    ) -> None:
        self.firing_ship = ship
        self.type = WEAPON.PHASER
        self.projectile_group = projectile_group
        surf = Surface([100, 1]).convert_alpha()
        super().__init__(surf, start_pos, start_ang, start_vel)
        self.start_time = pygame.time.get_ticks()

        # Update rotation to surface

        self.ang %= 360
        self.ship_pos = start_pos
        phaser_x_pos = self.pos[0] + 50 * math.cos(self.ang * math.pi / 180)
        phaser_y_pos = self.pos[1] + 50 * math.sin(self.ang * math.pi / 180)

        self.pos = (phaser_x_pos, phaser_y_pos)
        surf = pygame.transform.rotate(self.surf, -self.ang)
        self.rect = surf.get_rect(center=self.pos)
        self.draw_laser()

    def draw_laser(self, end_x=99):
        # Draw a line to represent phaser
        for projectile in self.projectile_group.sprites():
            if projectile != self and self.rect.colliderect(projectile.rect):
                end_x = math.dist(self.ship_pos, (projectile.rect.center))

                self.projectile_group.remove(projectile)
                break
        pygame.draw.line(
            self.image, "white", start_pos=(0, 0), end_pos=(end_x, 0)
        )
        self.image = pygame.transform.rotate(self.surf, -self.ang)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        flight_time = pygame.time.get_ticks() - self.start_time
        if flight_time > PHASER_MAX_FLIGHT_MS:
            self.projectile_group.remove(self)

    def check_active(self):
        flight_time = pygame.time.get_ticks() - self.start_time
        if flight_time > PHASER_FIRE_TIME_DELAY_MS:
            return False
        return True


class PhotonTorpedo(SpaceEntity):
    """Represents the photon torpedo object that a ship can fire"""

    def __init__(
        self, start_pos, start_ang, start_vel, projectile_group
    ) -> None:
        self.type = WEAPON.TORPEDO
        surf = Surface([12, 12]).convert_alpha()
        torpedo_x_pos = start_pos[0] + 30 * math.cos(start_ang * math.pi / 180)
        torpedo_y_pos = start_pos[1] + 30 * math.sin(start_ang * math.pi / 180)
        super().__init__(
            surf, (torpedo_x_pos, torpedo_y_pos), start_ang, start_vel
        )

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
                if projectile.type != WEAPON.PHASER:
                    self.projectile_group.remove(projectile)
