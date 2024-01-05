"""Collection of classes for weapons"""

import math
from typing import Any

import pygame
from pygame import Surface

from space_war.sim.base import SpaceEntity
from space_war.sim.conf import (
    PHASER_LENGTH,
    PHASER_MAX_FLIGHT_MS,
    PHASER_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TORPEDO_MAX_FLIGHT_MS,
    TORPEDO_SPEED,
    SpaceEntityType,
)
from space_war.sim.util import create_linear_eq


class BaseWeapon(pygame.sprite.Sprite):
    """Simple base class for weapons. All weapons have a specific duration."""

    # TODO: add a damage attribute to inflict damage to ship's shield on hit

    def __init__(self, duration) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.start_time = pygame.time.get_ticks()
        self.max_duration = duration

    def is_expired(self) -> bool:
        """Returns True if duration of weapon exceeds the max duration"""
        current_duration = pygame.time.get_ticks() - self.start_time
        return current_duration >= self.max_duration

    def update(self, *args: Any, **kwargs: Any):
        """Update entrypoint for weapons"""
        super().update(*args, **kwargs)
        if self.is_expired():
            self.kill()


class Phaser(BaseWeapon):
    """The phaser weapon, fires a straight line up to a fixed distance

    Attributes
    ----------
    source_ship: The ship that is firing the phaser
    active: Whether the phaser is actively being fired or not
    ship_pos: The center position of the source_ship
    coords: List of coordinates to draw the phaser. Ordered by the end to start.

    """

    source_ship: pygame.sprite.Sprite
    active: bool
    start_time: int
    ship_pos: tuple[float, float]
    coords: list[tuple[float, float]]

    def __init__(self, source_ship) -> None:
        super().__init__(duration=PHASER_MAX_FLIGHT_MS)
        self.source_ship = source_ship
        self.image = Surface([SCREEN_WIDTH, SCREEN_HEIGHT]).convert_alpha()
        self.rect = self.image.get_rect()
        self.active = True
        self.hit_detect_info = {
            "rect": [],
            "start_pos": [],
            "end_pos": [],
            "dist": [],
        }
        self.coords = []

    def _draw_phaser(self, ship_pos):
        """Draws coordinates for the phaser based on coordinates set in
        self._detect_hit. This is visible to the player.

        """

        # Calculate change in position since calculation
        # and translate all the lines
        (old_startx, old_starty), _ = self.coords[-1]
        deltax = ship_pos[0] - old_startx
        deltay = ship_pos[1] - old_starty
        for (startx, starty), (endx, endy) in self.coords:
            startx += deltax
            starty += deltay
            endx += deltax
            endy += deltay

            pygame.draw.line(
                self.image,
                "white",
                start_pos=(startx, starty),
                end_pos=(endx, endy),
                width=PHASER_WIDTH,
            )

    def _detect_hit(
        self,
        target_group: pygame.sprite.Group,
    ):
        """Calculates the start and end coordinates of the lines to be
        shown to the player.

          - Collisions with the rectangle will result in drawing a line to the
            center of the sprite in the target group.
          - If there are multiple collisions, only consider the closest one.
          - If there are no collisions, draw the full length of the laser.
        """

        if self.active:
            idx_to_kill = None
            idx = 0
            rect_idx = None
            min_dist = PHASER_LENGTH
            dist = PHASER_LENGTH
            end_pos = self.hit_detect_info["end_pos"][-1]
            start_pos = self.hit_detect_info["start_pos"][-1]
            target_sprites = target_group.sprites()

            for sprite in target_sprites:
                if sprite not in (self, self.source_ship):
                    rect_collide_idx = sprite.rect.collidelist(
                        self.hit_detect_info["rect"]
                    )
                    if rect_collide_idx != -1:
                        dist = math.dist(
                            self.hit_detect_info["start_pos"][rect_collide_idx],
                            sprite.rect.center,
                        )
                        if rect_collide_idx == 1:
                            dist += self.hit_detect_info["dist"][0]

                        if dist < min_dist:
                            min_dist = dist
                            idx_to_kill = idx
                            start_pos = self.hit_detect_info["start_pos"][
                                rect_collide_idx
                            ]
                            end_pos = sprite.rect.center
                            rect_idx = rect_collide_idx

                idx += 1
            if idx_to_kill is not None:
                target_sprites[idx_to_kill].kill()

            self.coords.append((start_pos, end_pos))
            if (start_pos, end_pos) != (
                self.hit_detect_info["start_pos"][0],
                self.hit_detect_info["end_pos"][0],
            ) and (rect_idx is None or rect_idx == 1):
                self.coords.append(
                    (
                        self.hit_detect_info["start_pos"][0],
                        self.hit_detect_info["end_pos"][0],
                    )
                )

            self.active = False

    def _update_hit_detector_rects(self, ship_pos, ship_ang):
        """Creates hit detection rectangles for the phasers. These are
        invisible to the player.
        """

        x_linear_eq, y_linear_eq, slope = create_linear_eq(ship_ang, ship_pos)

        # TODO: Make screen wrap around logic iterative

        target_pos = (
            ship_pos[0] + PHASER_LENGTH * math.cos(ship_ang * math.pi / 180),
            ship_pos[1] + PHASER_LENGTH * math.sin(ship_ang * math.pi / 180),
        )

        x_pos, y_pos = target_pos
        new_x_pos, new_y_pos = ship_pos

        if x_pos >= SCREEN_WIDTH:
            x_pos = SCREEN_WIDTH
            y_pos = y_linear_eq(x_pos) if slope != 0 else y_pos
            new_x_pos = 0
        elif x_pos <= 0:
            x_pos = 0
            y_pos = y_linear_eq(x_pos) if slope != 0 else y_pos
            new_x_pos = SCREEN_WIDTH

        if y_pos >= SCREEN_HEIGHT:
            y_pos = SCREEN_HEIGHT
            x_pos = x_linear_eq(y_pos) if slope != 0 else x_pos
            new_y_pos = 0
        elif y_pos <= 0:
            y_pos = 0
            x_pos = x_linear_eq(y_pos) if slope != 0 else x_pos
            new_y_pos = SCREEN_HEIGHT

        target_pos = (x_pos, y_pos)

        # Remove old lines
        self.image.fill("black")

        # Use this rect to detect collisions
        rect = pygame.draw.line(
            self.image,
            pygame.color.Color(0, 0, 0, 0),
            ship_pos,
            target_pos,
            PHASER_WIDTH,
        )
        dist = math.dist(ship_pos, target_pos)
        self.hit_detect_info["rect"].append(rect)
        self.hit_detect_info["start_pos"].append(ship_pos)
        self.hit_detect_info["end_pos"].append(target_pos)
        self.hit_detect_info["dist"].append(dist)
        remaining_dist = PHASER_LENGTH - dist
        if math.floor(remaining_dist) > 0:
            # Then create another rect to wraps around the screen
            new_target_pos = (
                new_x_pos + remaining_dist * math.cos(ship_ang * math.pi / 180),
                new_y_pos + remaining_dist * math.sin(ship_ang * math.pi / 180),
            )
            new_rect = pygame.draw.line(
                self.image,
                pygame.color.Color(0, 0, 0, 0),
                (new_x_pos, new_y_pos),
                new_target_pos,
                PHASER_WIDTH,
            )
            self.hit_detect_info["rect"].append(new_rect)
            self.hit_detect_info["start_pos"].append((new_x_pos, new_y_pos))
            self.hit_detect_info["end_pos"].append(new_target_pos)
            self.hit_detect_info["dist"].append(remaining_dist)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._update_hit_detector_rects(kwargs["ship_pos"], kwargs["ship_ang"])
        self._detect_hit(target_group=kwargs["target_group"])
        self._draw_phaser(kwargs["ship_pos"])


class PhotonTorpedo(BaseWeapon, SpaceEntity):
    """Represents the photon torpedo object that a ship can fire"""

    def __init__(self, start_pos, start_ang, start_vel) -> None:
        surf = Surface([12, 12]).convert_alpha()
        torpedo_x_pos = start_pos[0] + 36 * math.cos(start_ang * math.pi / 180)
        torpedo_y_pos = start_pos[1] + 36 * math.sin(start_ang * math.pi / 180)
        BaseWeapon.__init__(self, duration=TORPEDO_MAX_FLIGHT_MS)
        SpaceEntity.__init__(
            self,
            entity_type=SpaceEntityType.TORPEDO,
            surf=surf,
            start_pos=(torpedo_x_pos, torpedo_y_pos),
            start_ang=start_ang,
            start_vel=start_vel,
        )

        # Draw on the surface of what the torpedo looks like
        pygame.draw.polygon(self.image, "white", [[5, 0], [3, 5], [7, 5]], 1)
        pygame.draw.polygon(self.image, "white", [[0, 10], [3, 9], [3, 5]], 1)
        pygame.draw.polygon(self.image, "white", [[7, 5], [7, 9], [11, 10]], 1)
        pygame.draw.line(self.image, "white", (3, 9), (7, 9))
        pygame.draw.line(self.image, "white", (5, 5), (5, 11))
        # Drawn like a christmas tree, so need to rotate it by 90 degrees.
        self.surf = pygame.transform.rotate(self.surf, -90)

        # Apply torpedoes velocity on ship's velocity
        x_vel, y_vel = self.vel
        x_vel += TORPEDO_SPEED * math.cos(self.ang * math.pi / 180)
        y_vel += TORPEDO_SPEED * math.sin(self.ang * math.pi / 180)
        self.vel = (x_vel, y_vel)

    def update(self, *args, **kwargs):
        SpaceEntity.update(self, *args, **kwargs)
        BaseWeapon.update(self, *args, **kwargs)

        # group and collision management
        for sprite in kwargs["target_group"].sprites():
            if sprite != self and self.rect.colliderect(sprite.rect):
                sprite.kill()
                self.kill()
