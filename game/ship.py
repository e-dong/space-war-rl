"""Collection of Ship Classes"""
import math
from pathlib import Path

import pygame

from game.base import SpaceEntity
from game.conf import (
    CHECK_KEYS_TIME_DELAY_MS,
    MAX_TORPEDOES_PER_SHIP,
    WEAPON,
    WEAPON_FIRE_TIME_DEPLAY_MS,
)
from game.projectile import Phaser, PhotonTorpedo


# TODO: Create a bass class for ship,
# refactor the interaction logic into "actions"
class HumanShip(SpaceEntity):
    """Represents the ship controlled by a human player"""

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
            if event.key == pygame.constants.K_q:
                if not self.phaser or not self.phaser.check_active():
                    phaser_x_pos = self.pos[0] + 40 * math.cos(
                        self.ang * math.pi / 180
                    )
                    phaser_y_pos = self.pos[1] + 40 * math.sin(
                        self.ang * math.pi / 180
                    )
                    self.phaser = Phaser(
                        start_pos=(phaser_x_pos, phaser_y_pos),
                        start_vel=self.vel,
                        start_ang=self.ang,
                        projectile_group=self.projectile_group,
                    )
                    self.projectile_group.add(self.phaser)
                    pygame.time.set_timer(
                        self.check_fire_phaser_event,
                        300,
                    )
            if event.key == pygame.constants.K_e:
                if len(self.projectile_group) < MAX_TORPEDOES_PER_SHIP:
                    torpedo_x_pos = self.pos[0] + 30 * math.cos(
                        self.ang * math.pi / 180
                    )
                    torpedo_y_pos = self.pos[1] + 30 * math.sin(
                        self.ang * math.pi / 180
                    )
                    self.projectile_group.add(
                        PhotonTorpedo(
                            start_pos=(torpedo_x_pos, torpedo_y_pos),
                            start_ang=self.ang,
                            start_vel=self.vel,
                            projectile_group=self.projectile_group,
                        )
                    )
                    pygame.time.set_timer(
                        self.check_fire_torpedoes_event,
                        WEAPON_FIRE_TIME_DEPLAY_MS,
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
            phaser_x_pos = self.pos[0] + 40 * math.cos(self.ang * math.pi / 180)
            phaser_y_pos = self.pos[1] + 40 * math.sin(self.ang * math.pi / 180)
            self.phaser = Phaser(
                start_pos=(phaser_x_pos, phaser_y_pos),
                start_vel=self.vel,
                start_ang=self.ang,
                projectile_group=self.projectile_group,
            )
            self.projectile_group.add(self.phaser)
        if event.type == self.check_fire_torpedoes_event:
            if len(self.projectile_group) < MAX_TORPEDOES_PER_SHIP:
                torpedo_x_pos = self.pos[0] + 30 * math.cos(
                    self.ang * math.pi / 180
                )
                torpedo_y_pos = self.pos[1] + 30 * math.sin(
                    self.ang * math.pi / 180
                )
                self.projectile_group.add(
                    PhotonTorpedo(
                        start_pos=(torpedo_x_pos, torpedo_y_pos),
                        start_ang=self.ang,
                        start_vel=self.vel,
                        projectile_group=self.projectile_group,
                    )
                )

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        for sprite in self.projectile_group.sprites():
            if (
                self.rect.colliderect(sprite.rect)
                and sprite.type == WEAPON.TORPEDO
            ):
                self.projectile_group.remove(sprite)
                # TODO: apply damage to the ship for every collision
