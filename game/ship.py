"""Collection of Ship Classes"""
import math
from pathlib import Path

import pygame

from game.base import SpaceEntity
from game.conf import (
    CHECK_KEYS_TIME_DELAY_MS,
    MAX_TORPEDOES_PER_SHIP,
    MOVEMENT_TIME_DELAY_MS,
    PHASER_FIRE_TIME_DELAY_MS,
    TORPEDO_FIRE_TIME_DELAY_MS,
)
from game.projectile import Phaser, PhotonTorpedo

# TODO: Create a bass class for ship,
# refactor the interaction logic into "actions"

# TODO: Refactor weapon cooldown period in ship instead of in projectile class
# Currently torpedoes does not have a cooldown, shoots as fast as your press E
# Phasers are implemented via the Phaser.check_active function


class HumanShip(SpaceEntity):
    """Represents the ship controlled by a human player"""

    torpedo_group: pygame.sprite.Group
    rotate_ccw_lock: bool
    check_rotate_cc_repeat_event: pygame.USEREVENT
    check_rotate_cw_repeat_event: pygame.USEREVENT
    check_acc_repeat_event: pygame.USEREVENT
    check_fire_torpedoes_event: pygame.USEREVENT

    def __init__(
        self, image_path: Path, start_pos: tuple[int, int], start_ang: float
    ) -> None:
        super().__init__(
            pygame.image.load(image_path).convert_alpha(), start_pos, start_ang
        )
        self.torpedo_group = pygame.sprite.Group()
        self.phaser_group = pygame.sprite.GroupSingle()
        self.phaser = None
        self.rotate_ccw_lock = False

        # create custom event to check user input
        self.check_rotate_cc_repeat_event = pygame.USEREVENT + 1
        self.check_rotate_cw_repeat_event = pygame.USEREVENT + 2
        self.check_acc_repeat_event = pygame.USEREVENT + 3
        self.check_fire_torpedoes_event = pygame.USEREVENT + 4
        self.check_fire_phaser_event = pygame.USEREVENT + 5

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
                        self.check_fire_phaser_event,
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
                        self.check_fire_torpedoes_event,
                        TORPEDO_FIRE_TIME_DELAY_MS,
                    )
        if event.type == pygame.KEYUP:
            if event.key == pygame.constants.K_a:
                self.rotate_ccw_lock = False
                pygame.time.set_timer(self.check_rotate_cc_repeat_event, 0)

            if event.key == pygame.constants.K_d:
                self.rotate_ccw_lock = True
                pygame.time.set_timer(self.check_rotate_cw_repeat_event, 0)
            if event.key == pygame.constants.K_s:
                pygame.time.set_timer(self.check_acc_repeat_event, 0)
            if event.key == pygame.constants.K_q:
                pygame.time.set_timer(self.check_fire_phaser_event, 0)
            if event.key == pygame.constants.K_e:
                pygame.time.set_timer(self.check_fire_torpedoes_event, 0)
        if event.type == self.check_rotate_cc_repeat_event:
            # Update rotation
            if self.rotate_ccw_lock:
                self.ang -= 22.5
            self.ang %= 360
        if event.type == self.check_rotate_cw_repeat_event:
            if not self.rotate_ccw_lock:
                self.ang += 22.5
            self.ang %= 360
        if event.type == self.check_acc_repeat_event:
            x_vel, y_vel = self.vel
            x_vel += math.cos(self.ang * math.pi / 180)
            y_vel += math.sin(self.ang * math.pi / 180)
            self.vel = (x_vel, y_vel)
        if event.type == self.check_fire_phaser_event:
            self.phaser = Phaser(
                source_ship=self,
                start_pos=self.pos,
                start_vel=self.vel,
                start_ang=self.ang,
            )
            self.phaser_group.add(self.phaser)
        if event.type == self.check_fire_torpedoes_event:
            if len(self.torpedo_group) < MAX_TORPEDOES_PER_SHIP:
                self.torpedo_group.add(
                    PhotonTorpedo(
                        start_pos=self.pos,
                        start_ang=self.ang,
                        start_vel=self.vel,
                    )
                )
