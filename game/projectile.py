"""Collection of classes for weapons"""

import math

import pygame
from pygame import Surface

from game.base import SpaceEntity
from game.conf import (
    PHASER_FIRE_TIME_DELAY_MS,
    PHASER_MAX_FLIGHT_MS,
    TORPEDO_MAX_FLIGHT_MS,
    TORPEDO_SPEED,
    WEAPON,
)


class Phaser(SpaceEntity):
    def __init__(self, source_ship, start_pos, start_ang, start_vel) -> None:
        self.source_ship = source_ship
        self.type = WEAPON.PHASER
        surf = Surface([100, 1]).convert_alpha()
        super().__init__(surf, start_pos, start_ang, start_vel)
        self.start_time = pygame.time.get_ticks()
        self.active = True
        # Update rotation to surface
        self.ang %= 360
        self.ship_pos = start_pos
        phaser_x_pos = self.pos[0] + 50 * math.cos(self.ang * math.pi / 180)
        phaser_y_pos = self.pos[1] + 50 * math.sin(self.ang * math.pi / 180)

        self.pos = (phaser_x_pos, phaser_y_pos)
        surf = pygame.transform.rotate(self.surf, -self.ang)
        self.rect = surf.get_rect(center=self.pos)

    def draw_laser(self, target_group: pygame.sprite.AbstractGroup, end_x=99):
        # Draw a line to represent phaser
        if self.active:
            idx_to_kill = None
            idx = 0
            target_sprites = pygame.sprite.spritecollide(self, target_group, 0)
            for projectile in target_sprites:
                if (
                    projectile != self
                    and projectile != self.source_ship
                    and self.rect.colliderect(projectile.rect)
                ):
                    dist = math.dist(self.ship_pos, (projectile.rect.center))
                    if dist < end_x:
                        end_x = dist
                        idx_to_kill = idx

                idx += 1
            if idx_to_kill is not None:
                target_sprites[idx_to_kill].kill()
            pygame.draw.line(
                self.image, "white", start_pos=(0, 0), end_pos=(end_x, 0)
            )
            self.active = False

    def update(self, target_group, *args, **kwargs):
        self.draw_laser(target_group)
        super().update(*args, **kwargs)

        flight_time = pygame.time.get_ticks() - self.start_time
        if flight_time > PHASER_MAX_FLIGHT_MS:
            self.kill()

    def check_active(self):
        flight_time = pygame.time.get_ticks() - self.start_time
        if flight_time > PHASER_FIRE_TIME_DELAY_MS:
            return False
        return True


class PhotonTorpedo(SpaceEntity):
    """Represents the photon torpedo object that a ship can fire"""

    def __init__(self, start_pos, start_ang, start_vel) -> None:
        self.type = WEAPON.TORPEDO
        surf = Surface([12, 12]).convert_alpha()
        torpedo_x_pos = start_pos[0] + 36 * math.cos(start_ang * math.pi / 180)
        torpedo_y_pos = start_pos[1] + 36 * math.sin(start_ang * math.pi / 180)
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

        self.start_time = pygame.time.get_ticks()

    def update(self, target_group, *args, **kwargs):
        super().update(*args, **kwargs)
        # Torpedo needs to be rotated an additional 90 degrees
        # due to the orientation it was originally drawn
        self.image = pygame.transform.rotate(self.surf, -(self.ang + 90))
        self.rect = self.image.get_rect(center=self.pos)
        # group and collision management
        flight_time = pygame.time.get_ticks() - self.start_time
        if flight_time > TORPEDO_MAX_FLIGHT_MS:
            self.kill()

        for projectile in target_group.sprites():
            if projectile != self and self.rect.colliderect(projectile.rect):
                projectile.kill()
                self.kill()
