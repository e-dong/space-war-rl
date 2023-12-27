"""Collection of classes for weapons"""

import math

import pygame
from pygame import Surface

from game.base import SpaceEntity
from game.conf import (
    PHASER_LENGTH,
    PHASER_MAX_FLIGHT_MS,
    PHASER_WIDTH,
    TORPEDO_MAX_FLIGHT_MS,
    TORPEDO_SPEED,
    WEAPON,
)


class Phaser(SpaceEntity):
    """The phaser weapon, fires a straight line up to a fixed distance"""

    source_ship: pygame.sprite.Sprite
    type: WEAPON.PHASER
    active: bool
    start_time: int
    ship_pos: tuple[float, float]

    def __init__(self, source_ship, start_pos, start_ang, start_vel) -> None:
        self.source_ship = source_ship
        self.type = WEAPON.PHASER
        surf = Surface([PHASER_LENGTH, PHASER_WIDTH]).convert_alpha()
        super().__init__(surf, start_pos, start_ang, start_vel)
        self.start_time = pygame.time.get_ticks()
        self.active = True
        # Update rotation to surface
        self.ang %= 360
        self.ship_pos = start_pos

        # Translate the phaser due to rotation to center
        phaser_x_pos = self.pos[0] + (PHASER_LENGTH / 2) * math.cos(
            self.ang * math.pi / 180
        )
        phaser_y_pos = self.pos[1] + (PHASER_LENGTH / 2) * math.sin(
            self.ang * math.pi / 180
        )

        self.pos = (phaser_x_pos, phaser_y_pos)
        surf = pygame.transform.rotate(self.surf, -self.ang)
        self.rect = surf.get_rect(center=self.pos)

    def draw_laser(
        self, target_group: pygame.sprite.Group, end_x=PHASER_LENGTH - 1
    ):
        """Draws the non-piercing laser and handle collisions with sprites
        within target group.

          - Collisions with the rectangle will result in drawing a line to the
            center of the sprite in the target group.
          - If there are multiple collisions, only consider the closest one.
          - If there are no collisions, draw the full length of the laser.
        """

        if self.active:
            idx_to_kill = None
            idx = 0
            collided_sprites = pygame.sprite.spritecollide(
                self, target_group, 0
            )
            for sprite in collided_sprites:
                if (
                    sprite != self
                    and sprite != self.source_ship
                    and self.rect.colliderect(sprite.rect)
                ):
                    dist = math.dist(self.ship_pos, (sprite.rect.center))
                    if dist < end_x:
                        end_x = dist
                        idx_to_kill = idx

                idx += 1
            if idx_to_kill is not None:
                collided_sprites[idx_to_kill].kill()
            pygame.draw.line(
                self.image, "white", start_pos=(0, 0), end_pos=(end_x, 0)
            )
            self.active = False

    def update(self, *args, **kwargs):
        self.draw_laser(kwargs["target_group"])
        super().update(*args, **kwargs)

        flight_time = pygame.time.get_ticks() - self.start_time
        if flight_time > PHASER_MAX_FLIGHT_MS:
            self.kill()


class PhotonTorpedo(SpaceEntity):
    """Represents the photon torpedo object that a ship can fire"""

    type: WEAPON.TORPEDO
    start_time: int

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

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        # Torpedo needs to be rotated an additional 90 degrees
        # due to the orientation it was originally drawn
        self.image = pygame.transform.rotate(self.surf, -(self.ang + 90))
        self.rect = self.image.get_rect(center=self.pos)
        # group and collision management
        flight_time = pygame.time.get_ticks() - self.start_time
        if flight_time > TORPEDO_MAX_FLIGHT_MS:
            self.kill()

        for sprite in kwargs["target_group"].sprites():
            if sprite != self and self.rect.colliderect(sprite.rect):
                sprite.kill()
                self.kill()
