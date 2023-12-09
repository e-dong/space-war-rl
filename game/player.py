"""Collection of Player Classes"""
import math
from pathlib import Path

import pygame

from game.base import SpaceEntity
from game.conf import CHECK_KEYS_TIME_DELAY_MS, WEAPON_FIRE_TIME_DEPLAY_MS
from game.projectile import PhotonTorpedo


class HumanPlayer(SpaceEntity):
    """Represents the human player."""

    projectile_group: pygame.sprite.Group
    rotate_ccw_lock: bool
    check_rotate_cc_repeat_event: pygame.USEREVENT
    check_rotate_cw_repeat_event: pygame.USEREVENT
    check_acc_repeat_event: pygame.USEREVENT
    check_fire_torpedoes_event: pygame.USEREVENT

    def __init__(
        self,
        image_path: Path,
        start_pos: tuple[int, int],
        projectile_group: pygame.sprite.Group,
    ) -> None:
        super().__init__(
            pygame.image.load(image_path).convert_alpha(),
            start_pos,
        )
        self.projectile_group = projectile_group
        self.rotate_ccw_lock = False

        # create custom event to check user input
        self.check_rotate_cc_repeat_event = pygame.USEREVENT + 1
        self.check_rotate_cw_repeat_event = pygame.USEREVENT + 2
        self.check_acc_repeat_event = pygame.USEREVENT + 3
        self.check_fire_torpedoes_event = pygame.USEREVENT + 4

    def handle_events(self, event: pygame.event.Event):
        """Handles keyboard input to update ship's rotation and position
        state. This method should be called from the event loop to pass the
        event object.
        """
        if event.type == pygame.KEYDOWN:
            # Handle ship movement and rotation
            if event.key == pygame.constants.K_a:
                self.rotate_ccw_lock = True
                self.ang -= 22.5
                pygame.time.set_timer(
                    self.check_rotate_cc_repeat_event, CHECK_KEYS_TIME_DELAY_MS
                )

            if event.key == pygame.constants.K_d:
                self.rotate_ccw_lock = False
                self.ang += 22.5
                pygame.time.set_timer(
                    self.check_rotate_cw_repeat_event, CHECK_KEYS_TIME_DELAY_MS
                )
            if event.key == pygame.constants.K_s:
                x_vel, y_vel = self.vel
                x_vel += math.cos(self.ang * math.pi / 180)
                y_vel += math.sin(self.ang * math.pi / 180)
                self.vel = (x_vel, y_vel)
                pygame.time.set_timer(
                    self.check_acc_repeat_event, CHECK_KEYS_TIME_DELAY_MS
                )
            if event.key == pygame.constants.K_e:
                self.projectile_group.add(
                    PhotonTorpedo(
                        start_pos=self.pos,
                        start_ang=self.ang,
                        start_vel=self.vel,
                    )
                )
                pygame.time.set_timer(
                    self.check_fire_torpedoes_event, WEAPON_FIRE_TIME_DEPLAY_MS
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
        if event.type == self.check_fire_torpedoes_event:
            self.projectile_group.add(
                PhotonTorpedo(
                    start_pos=self.pos, start_ang=self.ang, start_vel=self.vel
                )
            )
