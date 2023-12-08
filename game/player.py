"""Collection of Player Classes"""
import math

import pygame
from pygame import KEYDOWN, KEYUP, image, transform
from pygame.constants import K_a, K_d, K_s
from pygame.event import Event
from pygame.sprite import Sprite

from game.conf import CHECK_KEYS_TIME_DELAY_MS, SCREEN_HEIGHT, SCREEN_WIDTH


class HumanPlayer(Sprite):
    """Represents the human player"""

    def __init__(self, image_path, start_pos, start_ang=0) -> None:
        super().__init__()
        self.surf = image.load(image_path).convert_alpha()
        self.image = self.surf
        self.pos = start_pos
        self.rect = self.surf.get_rect(center=self.pos)
        self.x_vel = 0
        self.y_vel = 0
        self.ang = start_ang
        self.rotate_ccw_lock = False

        # create custom event to check user input
        self.check_rotate_cc_repeat_event = pygame.USEREVENT + 1
        self.check_rotate_cw_repeat_event = pygame.USEREVENT + 2
        self.check_acc_repeat_event = pygame.USEREVENT + 3

    def handle_events(self, event: Event):
        """Handles keyboard input to update ship's rotation and position
        state
        """
        if event.type == KEYDOWN:
            # Handle ship movement and rotation
            if event.key == K_a:
                self.rotate_ccw_lock = True
                self.ang -= 22.5
                pygame.time.set_timer(
                    self.check_rotate_cc_repeat_event, CHECK_KEYS_TIME_DELAY_MS
                )

            if event.key == K_d:
                self.rotate_ccw_lock = False
                self.ang += 22.5
                pygame.time.set_timer(
                    self.check_rotate_cw_repeat_event, CHECK_KEYS_TIME_DELAY_MS
                )
            if event.key == K_s:
                self.x_vel += math.cos(self.ang * math.pi / 180)
                self.y_vel += math.sin(self.ang * math.pi / 180)
                pygame.time.set_timer(
                    self.check_acc_repeat_event, CHECK_KEYS_TIME_DELAY_MS
                )
        if event.type == KEYUP:
            if event.key == K_a:
                self.rotate_ccw_lock = False
                pygame.time.set_timer(self.check_rotate_cc_repeat_event, 0)

            if event.key == K_d:
                self.rotate_ccw_lock = True
                pygame.time.set_timer(self.check_rotate_cw_repeat_event, 0)
            if event.key == K_s:
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

    def update(self, *args, **kwargs):
        """Entrypoint for updating the player state each frame"""
        x_pos, y_pos = self.pos

        # Conditions for wrapping around the screen
        if x_pos >= SCREEN_WIDTH + 10:
            x_pos = 0
        elif x_pos <= -10:
            x_pos = SCREEN_WIDTH
        if y_pos >= SCREEN_HEIGHT + 10:
            y_pos = 0
        elif y_pos <= -10:
            y_pos = SCREEN_HEIGHT

        # Apply velocity to position
        x_pos += self.x_vel
        y_pos += self.y_vel
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.pos = (x_pos, y_pos)

        # Update rotation to surface
        newsurf = transform.rotate(self.surf, -self.ang)
        self.rect = newsurf.get_rect(center=self.pos)
        self.image = newsurf
