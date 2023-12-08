"""Collection of Player Classes"""
import math

import pygame

from game.base import SpaceEntity
from game.conf import CHECK_KEYS_TIME_DELAY_MS


class HumanPlayer(SpaceEntity):
    """Represents the human player"""

    def __init__(self, image_path, start_pos, start_ang=0) -> None:
        super().__init__(
            start_pos, start_ang, pygame.image.load(image_path).convert_alpha()
        )

        self.rotate_ccw_lock = False

        # create custom event to check user input
        self.check_rotate_cc_repeat_event = pygame.USEREVENT + 1
        self.check_rotate_cw_repeat_event = pygame.USEREVENT + 2
        self.check_acc_repeat_event = pygame.USEREVENT + 3

    def handle_events(self, event: pygame.event.Event):
        """Handles keyboard input to update ship's rotation and position
        state
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
                self.x_vel += math.cos(self.ang * math.pi / 180)
                self.y_vel += math.sin(self.ang * math.pi / 180)
                pygame.time.set_timer(
                    self.check_acc_repeat_event, CHECK_KEYS_TIME_DELAY_MS
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
            self.x_vel += math.cos(self.ang * math.pi / 180)
            self.y_vel += math.sin(self.ang * math.pi / 180)
