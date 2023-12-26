"""Collection of Ship Classes"""
import math
from pathlib import Path

import pygame

from game.base import SpaceEntity
from game.conf import (
    MAX_TORPEDOES_PER_SHIP,
    MOVEMENT_TIME_DELAY_MS,
    PHASER_FIRE_TIME_DELAY_MS,
    TORPEDO_FIRE_TIME_DELAY_MS,
)
from game.projectile import Phaser, PhotonTorpedo

# TODO: refactor the interaction logic into "actions"

# TODO: Refactor weapon cooldown period in ship instead of in projectile class
# Currently torpedoes does not have a cooldown, shoots as fast as your press E
# Phasers are implemented via the Phaser.check_active function


class BaseShip(SpaceEntity):
    player_id: int
    torpedo_group: pygame.sprite.Group
    phaser_group: pygame.sprite.GroupSingle
    phaser: pygame.sprite.Sprite
    rotate_ccw_lock: bool

    def __init__(
        self,
        player_id: int,
        image_path: Path,
        start_pos: tuple[int, int],
        start_ang: float,
    ) -> None:
        super().__init__(
            pygame.image.load(image_path).convert_alpha(), start_pos, start_ang
        )

        self.player_id = player_id
        self.torpedo_group = pygame.sprite.Group()
        self.phaser_group = pygame.sprite.GroupSingle()
        self.phaser = None

    def draw_groups(self, surface):
        self.torpedo_group.draw(surface)
        self.phaser_group.draw(surface)

    def update_groups(self, target_group):
        self.torpedo_group.update(target_group)
        self.phaser_group.update(target_group)


class HumanShip(BaseShip):
    """Represents the ship controlled by a human player"""

    rotate_cc_repeat_event: pygame.USEREVENT
    rotate_cw_repeat_event: pygame.USEREVENT
    acc_repeat_event: pygame.USEREVENT
    fire_torpedoes_repeat_event: pygame.USEREVENT
    fire_phaser_repeat_event: pygame.USEREVENT

    def __init__(
        self,
        player_id: int,
        image_path: Path,
        start_pos: tuple[int, int],
        start_ang: float,
    ) -> None:
        super().__init__(player_id, image_path, start_pos, start_ang)

        self.rotate_ccw_lock = False

        # create custom event to check user input
        self.rotate_cc_repeat_event = pygame.USEREVENT + player_id + 1
        self.rotate_cw_repeat_event = pygame.USEREVENT + player_id + 2
        self.acc_repeat_event = pygame.USEREVENT + player_id + 3
        self.fire_torpedoes_repeat_event = pygame.USEREVENT + player_id + 4
        self.fire_phaser_repeat_event = pygame.USEREVENT + player_id + 5

    def handle_events(self, event: pygame.event.Event):
        """Handles keyboard input to update ship's rotation and position
        state. This method should be called from the event loop to pass the
        event object.
        """
        if not self.alive():
            return
        if event.type == pygame.KEYDOWN:
            # Handle ship movement and rotation
            if event.key == pygame.constants.K_a:
                self.rotate_ccw_lock = True
                self.ang -= 22.5
                pygame.time.set_timer(
                    self.rotate_cc_repeat_event, MOVEMENT_TIME_DELAY_MS
                )

            if event.key == pygame.constants.K_d:
                self.rotate_ccw_lock = False
                self.ang += 22.5
                pygame.time.set_timer(
                    self.rotate_cw_repeat_event, MOVEMENT_TIME_DELAY_MS
                )
            if event.key == pygame.constants.K_s:
                x_vel, y_vel = self.vel
                x_vel += math.cos(self.ang * math.pi / 180)
                y_vel += math.sin(self.ang * math.pi / 180)
                self.vel = (x_vel, y_vel)
                pygame.time.set_timer(
                    self.acc_repeat_event, MOVEMENT_TIME_DELAY_MS
                )
            if event.key == pygame.constants.K_q:
                if not self.phaser or not self.phaser.check_active():
                    self.phaser = Phaser(
                        source_ship=self,
                        start_pos=self.pos,
                        start_vel=self.vel,
                        start_ang=self.ang,
                    )
                    self.phaser_group.add(self.phaser)
                    pygame.time.set_timer(
                        self.fire_phaser_repeat_event,
                        PHASER_FIRE_TIME_DELAY_MS,
                    )
            if event.key == pygame.constants.K_e:
                if len(self.torpedo_group) < MAX_TORPEDOES_PER_SHIP:
                    self.torpedo_group.add(
                        PhotonTorpedo(
                            start_pos=self.pos,
                            start_ang=self.ang,
                            start_vel=self.vel,
                        )
                    )
                    pygame.time.set_timer(
                        self.fire_torpedoes_repeat_event,
                        TORPEDO_FIRE_TIME_DELAY_MS,
                    )
        if event.type == pygame.KEYUP:
            if event.key == pygame.constants.K_a:
                self.rotate_ccw_lock = False
                pygame.time.set_timer(self.rotate_cc_repeat_event, 0)

            if event.key == pygame.constants.K_d:
                self.rotate_ccw_lock = True
                pygame.time.set_timer(self.rotate_cw_repeat_event, 0)
            if event.key == pygame.constants.K_s:
                pygame.time.set_timer(self.acc_repeat_event, 0)
            if event.key == pygame.constants.K_q:
                pygame.time.set_timer(self.fire_phaser_repeat_event, 0)
            if event.key == pygame.constants.K_e:
                pygame.time.set_timer(self.fire_torpedoes_repeat_event, 0)
        if event.type == self.rotate_cc_repeat_event:
            # Update rotation
            if self.rotate_ccw_lock:
                self.ang -= 22.5
            self.ang %= 360
        if event.type == self.rotate_cw_repeat_event:
            if not self.rotate_ccw_lock:
                self.ang += 22.5
            self.ang %= 360
        if event.type == self.acc_repeat_event:
            x_vel, y_vel = self.vel
            x_vel += math.cos(self.ang * math.pi / 180)
            y_vel += math.sin(self.ang * math.pi / 180)
            self.vel = (x_vel, y_vel)
        if event.type == self.fire_phaser_repeat_event:
            self.phaser = Phaser(
                source_ship=self,
                start_pos=self.pos,
                start_vel=self.vel,
                start_ang=self.ang,
            )
            self.phaser_group.add(self.phaser)
        if event.type == self.fire_torpedoes_repeat_event:
            if len(self.torpedo_group) < MAX_TORPEDOES_PER_SHIP:
                self.torpedo_group.add(
                    PhotonTorpedo(
                        start_pos=self.pos,
                        start_ang=self.ang,
                        start_vel=self.vel,
                    )
                )
