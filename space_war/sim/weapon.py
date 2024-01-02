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


class BaseWeapon(pygame.sprite.Sprite):
    """Simple base class for weapons. All weapons have a specific duration."""

    def __init__(self, duration) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.start_time = pygame.time.get_ticks()
        self.max_duration = duration

    def check_expired(self) -> bool:
        """Returns True if duration of weapon exceeds the max duration"""
        current_duration = pygame.time.get_ticks() - self.start_time
        return current_duration >= self.max_duration

    def update(self, *args: Any, **kwargs: Any):
        """Update entrypoint for weapons"""

        super().update(*args, **kwargs)
        if self.check_expired():
            self.kill()


class Phaser(BaseWeapon):
    """The phaser weapon, fires a straight line up to a fixed distance

    Attributes
    ----------
    source_ship: The ship that is firing the phaser
    active: Whether the phaser is actively being fired or not
    start_time: The start time used to check duration of the phaser
    ship_pos: The center position of the source_ship
    coords: List of coordinates to draw the phaser

    """

    source_ship: pygame.sprite.Sprite
    active: bool
    start_time: int
    ship_pos: tuple[float, float]
    coords: list[tuple[float, float]]

    def __init__(self, source_ship) -> None:
        super().__init__(duration=PHASER_MAX_FLIGHT_MS)
        self.source_ship = source_ship
        self.surf = Surface([SCREEN_WIDTH, SCREEN_HEIGHT]).convert_alpha()
        self.rect = self.surf.get_rect()
        self.image = self.surf

        self.target_pos = None
        self.active = True
        self.hit_detect_info = {
            "rect": [],
            "start_pos": [],
            "end_pos": [],
            "dist": [],
        }

        self.coords = []

    def draw_phaser(self):
        """Draws coordinates for the phaser"""
        for start_pos, end_pos in self.coords:
            pygame.draw.line(
                self.image,
                "white",
                start_pos=start_pos,
                end_pos=end_pos,
                width=PHASER_WIDTH,
            )

    def handle_collision(
        self,
        target_group: pygame.sprite.Group,
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
            rect_idx = None
            min_dist = PHASER_LENGTH
            dist = PHASER_LENGTH
            end_pos = self.hit_detect_info["end_pos"][-1]
            start_pos = self.hit_detect_info["start_pos"][-1]

            for sprite in target_group.sprites():
                if sprite != self and sprite != self.source_ship:
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
                target_group.sprites()[idx_to_kill].kill()

            self.coords.append((start_pos, end_pos))

            if rect_idx is None or rect_idx == 1:
                self.coords.append(
                    (
                        self.hit_detect_info["start_pos"][0],
                        self.hit_detect_info["end_pos"][0],
                    )
                )

            self.active = False

    def update_hit_detector_rects(self, ship_pos, ship_ang):
        """Creates hit detection rectangles for the phasers"""
        slope_ang = ship_ang % 180
        slope = (
            math.tan(slope_ang * (math.pi / 180))
            if slope_ang < 90
            else 1 / math.tan(slope_ang * (math.pi / 180))
        )

        intercept = (
            ship_pos[1] - slope * ship_pos[0]
            if slope_ang < 90
            else ship_pos[0] - slope * ship_pos[1]
        )

        # get y coordinate from x
        y_linear_eq = (
            (lambda x: slope * x + intercept)
            if slope_ang < 90
            else (lambda x: (x - intercept) / slope)
        )

        # get x coordinate from y
        x_linear_eq = (
            (lambda y: (y - intercept) / slope)
            if slope_ang < 90
            else (lambda y: slope * y + intercept)
        )

        # TODO: Make screen wrap around logic iterative

        self.target_pos = (
            ship_pos[0] + PHASER_LENGTH * math.cos(ship_ang * math.pi / 180),
            ship_pos[1] + PHASER_LENGTH * math.sin(ship_ang * math.pi / 180),
        )

        x_pos, y_pos = self.target_pos
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

        self.target_pos = (x_pos, y_pos)

        # Remove old lines
        self.image.fill("black")

        # Use this rect to detect collisions
        rect = pygame.draw.line(
            self.image,
            pygame.color.Color(0, 0, 0, 0),
            ship_pos,
            self.target_pos,
            PHASER_WIDTH,
        )
        dist = math.dist(ship_pos, self.target_pos)
        self.hit_detect_info["rect"].append(rect)
        self.hit_detect_info["start_pos"].append(ship_pos)
        self.hit_detect_info["end_pos"].append(self.target_pos)
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
        self.update_hit_detector_rects(kwargs["ship_pos"], kwargs["ship_ang"])
        self.handle_collision(target_group=kwargs["target_group"])
        self.draw_phaser()


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

        # Apply torpedoes velocity on ship's velocity
        x_vel, y_vel = self.vel
        x_vel += TORPEDO_SPEED * math.cos(self.ang * math.pi / 180)
        y_vel += TORPEDO_SPEED * math.sin(self.ang * math.pi / 180)
        self.vel = (x_vel, y_vel)

    def update(self, *args, **kwargs):
        SpaceEntity.update(self, *args, **kwargs)
        BaseWeapon.update(self, *args, **kwargs)
        # Torpedo needs to be rotated an additional 90 degrees
        # due to the orientation it was originally drawn
        self.image = pygame.transform.rotate(self.surf, -(self.ang + 90))
        self.rect = self.image.get_rect(center=self.pos)

        # group and collision management
        for sprite in kwargs["target_group"].sprites():
            if sprite != self and self.rect.colliderect(sprite.rect):
                sprite.kill()
                self.kill()
