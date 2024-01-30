"""Collection of Ship Classes"""

import math
import platform
import uuid
from pathlib import Path
from threading import Thread
from typing import Union

import pygame

from space_war.sim.base import SpaceEntity
from space_war.sim.conf import (
    MAX_TORPEDOES_PER_SHIP,
    MAX_VEL,
    MOVEMENT_TIME_DELAY_MS,
    PHASER_FIRE_CD,
    TORPEDO_FIRE_CD,
    SpaceEntityType,
)
from space_war.sim.util import check_overlapping_sprites, sign
from space_war.sim.weapon import Phaser, PhotonTorpedo

# TODO: refactor the interaction logic into "actions"
# The human ship would call these action functions in handle_events


def patch_timer():
    """Custom monkey patch of pygame.time.set_timer function so it works in the
    pygame-wasm environment.

    """
    # pylint: disable-next=import-outside-toplevel
    import asyncio

    # pylint: disable-next=import-error,import-outside-toplevel,unused-import
    import aio.gthread

    # Global var to keep track of timer threads
    #   - key: event type
    #   - value: thread uuid
    timer_threads_dict = {}

    def patch_set_timer(
        event: Union[int, pygame.event.Event], millis: int, loops: int = 0
    ):
        """Patches the pygame.time.set_timer function to use gthreads"""

        dlay = float(millis) / 1000
        cevent = pygame.event.Event(event)
        event_loop = asyncio.get_event_loop()

        async def fire_event(thread_uuid):
            """The thread's target function to handle the timer

            Early exit conditions:
              - event loop is closed
              - event type is no longer in timer_threads_dict
              - the thread's uuid is not the latest one
              - Max loop iterations if loops param is not zero
            """
            loop_counter = 0
            while True:
                await asyncio.sleep(dlay)
                if (
                    event_loop.is_closed()
                    or event not in timer_threads_dict
                    or timer_threads_dict[event] != thread_uuid
                    or (loops and loop_counter >= loops)
                ):
                    break

                pygame.event.post(cevent)
                loop_counter += 1 if loops else 0

        if dlay > 0:
            # uuid is used to track the latest thread,
            # stale threads will be terminated
            thread_uuid = uuid.uuid4()
            Thread(target=fire_event, args=[thread_uuid]).start()
            timer_threads_dict[event] = thread_uuid

        else:
            # This cancels the timer for the event
            if event in timer_threads_dict:
                del timer_threads_dict[event]

    pygame.time.set_timer = patch_set_timer


if platform.system().lower() == "emscripten":
    patch_timer()


class BaseShip(SpaceEntity):
    """Defines common ship functionality.

    Attributes
    ----------
    player_id: Used uniquely identify the ship
    torpedo_group: Group containing its fired torpedoes
    phaser_group: Group containing its fired phaser
    phaser_last_fired: The number of ticks since firing a phaser
    torpedo_last_fired: The number of ticks since firing a torpedo

    """

    player_id: int
    torpedo_group: pygame.sprite.Group
    phaser_group: pygame.sprite.GroupSingle
    phaser: pygame.sprite.Sprite
    phaser_last_fired: int
    torpedo_last_fired: int

    def __init__(
        self,
        player_id: int,
        image_path: Path,
        start_pos: tuple[int, int],
        start_ang: float,
    ) -> None:
        super().__init__(
            SpaceEntityType.SHIP,
            pygame.image.load(image_path).convert_alpha(),
            start_pos,
            start_ang,
        )

        self.player_id = player_id
        self.torpedo_group = pygame.sprite.Group()
        self.phaser_group = pygame.sprite.GroupSingle()
        self.phaser = None
        self.phaser_last_fired = None
        self.torpedo_last_fired = None

    def draw_groups(self, surface: pygame.Surface):
        """Draws the torpedo and phaser group to the surface"""

        self.phaser_group.draw(surface)
        self.torpedo_group.draw(surface)

    def update_groups(self, target_group: pygame.sprite.Group):
        """Calls update on the torpedo and phaser group"""
        self.torpedo_group.update(target_group=target_group)
        self.phaser_group.update(
            target_group=target_group, ship_ang=self.ang, ship_pos=self.pos
        )

    def _check_phaser_on_cooldown(self) -> bool:
        """Checks if the phaser is actively being fired"""
        if not self.phaser_last_fired:
            return False
        flight_time = pygame.time.get_ticks() - self.phaser_last_fired
        if flight_time >= PHASER_FIRE_CD:
            return False
        return True

    def _check_torpedo_on_cooldown(self) -> bool:
        """Checks if the phaser is actively being fired"""
        if not self.torpedo_last_fired:
            return False
        flight_time = pygame.time.get_ticks() - self.torpedo_last_fired

        if flight_time >= TORPEDO_FIRE_CD:
            return False
        return True

    def _handle_ship_collisions(self, target_group):
        """Updates velocity based on ship on ship collisions"""
        for sprite in target_group.sprites():
            if (
                sprite != self
                and self.rect.colliderect(sprite.rect)
                and sprite.entity_type == SpaceEntityType.SHIP
            ):
                self_vel_x, self_vel_y = self.vel
                other_vel_x, other_vel_y = sprite.vel

                # preserve 20% velocity and gain 75% of the other ship's
                # velocity
                new_self_vel_x = (self_vel_x * 0.2) + (other_vel_x * 0.75)
                new_self_vel_y = (self_vel_y * 0.2) + (other_vel_y * 0.75)
                new_other_vel_x = (other_vel_x * 0.2) + (self_vel_x * 0.75)
                new_other_vel_y = (other_vel_y * 0.2) + (self_vel_y * 0.75)

                self.vel = (new_self_vel_x, new_self_vel_y)
                sprite.vel = (new_other_vel_x, new_other_vel_y)

                # detect any overlap and move the ships
                overlap_x, overlap_y = check_overlapping_sprites(self, sprite)

                if overlap_x:
                    sprite.pos = (sprite.pos[0] + sprite.vel[0], sprite.pos[1])
                if overlap_y:
                    sprite.pos = (
                        sprite.pos[0],
                        sprite.pos[1] + sprite.vel[1],
                    )

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._handle_ship_collisions(kwargs["target_group"])


class HumanShip(BaseShip):
    """Represents the ship controlled by a human player.
    User input is captured using the event loop in handle_events.

    Attributes
    ----------
    rotate_cc_repeat_event: The event where rotate cc key is held down
    rotate_cw_repeat_event: The event where the rotate cw key is held down
    acc_repeat_event: The event where the accelerate key is held down
    fire_torpedoes_repeat_event: The event where the fire torpedoes key is held down
    fire_phaser_repeat_event: The event where the fire phasers key is held down

    """

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
        # ships should have unique player ids to ensure events get handled
        # correctly
        self.rotate_cc_repeat_event = pygame.USEREVENT + player_id + 1
        self.rotate_cw_repeat_event = pygame.USEREVENT + player_id + 2
        self.acc_repeat_event = pygame.USEREVENT + player_id + 3
        self.fire_torpedoes_repeat_event = pygame.USEREVENT + player_id + 4
        self.fire_phaser_repeat_event = pygame.USEREVENT + player_id + 5

    def _handle_movement_events(self, event: pygame.event.Event):
        """Handle ship movement and rotation.

        Keybindings are hard coded for now. It would be good to make this config
        driven.
        """
        if event.type == pygame.KEYDOWN:
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
            if event.key == pygame.constants.K_w:
                x_vel, y_vel = self.vel
                new_x_vel = x_vel + math.cos(self.ang * math.pi / 180)
                new_y_vel = y_vel + math.sin(self.ang * math.pi / 180)
                x_vel = (
                    new_x_vel
                    if abs(new_x_vel) < MAX_VEL
                    else sign(new_x_vel) * MAX_VEL
                )
                y_vel = (
                    new_y_vel
                    if abs(new_y_vel) < MAX_VEL
                    else sign(new_y_vel) * MAX_VEL
                )
                self.vel = (x_vel, y_vel)
                pygame.time.set_timer(
                    self.acc_repeat_event, MOVEMENT_TIME_DELAY_MS
                )

        if event.type == pygame.KEYUP:
            if event.key == pygame.constants.K_a:
                self.rotate_ccw_lock = False
                pygame.time.set_timer(self.rotate_cc_repeat_event, 0)
            if event.key == pygame.constants.K_d:
                self.rotate_ccw_lock = True
                pygame.time.set_timer(self.rotate_cw_repeat_event, 0)
            if event.key == pygame.constants.K_w:
                pygame.time.set_timer(self.acc_repeat_event, 0)

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
            new_x_vel = x_vel + math.cos(self.ang * math.pi / 180)
            new_y_vel = y_vel + math.sin(self.ang * math.pi / 180)
            x_vel = (
                new_x_vel
                if abs(new_x_vel) < MAX_VEL
                else sign(new_x_vel) * MAX_VEL
            )
            y_vel = (
                new_y_vel
                if abs(new_y_vel) < MAX_VEL
                else sign(new_y_vel) * MAX_VEL
            )
            self.vel = (x_vel, y_vel)

    def _handle_firing_weapon_events(self, event: pygame.event.Event):
        """Handles firing phasers and photon torpedoes.

        Keybindings are hard coded for now. It would be good to make this config
        driven.

        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.constants.K_q:
                pygame.time.set_timer(
                    self.fire_phaser_repeat_event,
                    PHASER_FIRE_CD,
                )
                if not self._check_phaser_on_cooldown():
                    self.phaser = Phaser(source_ship=self)
                    self.phaser_group.add(self.phaser)
                    self.phaser_last_fired = pygame.time.get_ticks()
            if event.key == pygame.constants.K_e:
                pygame.time.set_timer(
                    self.fire_torpedoes_repeat_event,
                    TORPEDO_FIRE_CD,
                )
                if (
                    len(self.torpedo_group) < MAX_TORPEDOES_PER_SHIP
                    and not self._check_torpedo_on_cooldown()
                ):
                    self.torpedo_group.add(
                        PhotonTorpedo(
                            start_pos=self.pos,
                            start_ang=self.ang,
                            start_vel=self.vel,
                        )
                    )
                    self.torpedo_last_fired = pygame.time.get_ticks()

        if event.type == pygame.KEYUP:
            if event.key == pygame.constants.K_q:
                pygame.time.set_timer(self.fire_phaser_repeat_event, 0)
            if event.key == pygame.constants.K_e:
                pygame.time.set_timer(self.fire_torpedoes_repeat_event, 0)

        if event.type == self.fire_phaser_repeat_event:
            self.phaser = Phaser(source_ship=self)
            self.phaser_last_fired = pygame.time.get_ticks()
            self.phaser_group.add(self.phaser)
        if event.type == self.fire_torpedoes_repeat_event:
            if len(self.torpedo_group) < MAX_TORPEDOES_PER_SHIP:
                self.torpedo_last_fired = pygame.time.get_ticks()
                self.torpedo_group.add(
                    PhotonTorpedo(
                        start_pos=self.pos,
                        start_ang=self.ang,
                        start_vel=self.vel,
                    )
                )

    def handle_events(self, event: pygame.event.Event):
        """Handles keyboard input to update movement and fire weapons.

        This method should be called from the event loop to pass the
        event object.

        """

        # cleanup timer events
        if not self.alive():
            pygame.time.set_timer(self.rotate_cc_repeat_event, 0)
            pygame.time.set_timer(self.rotate_cw_repeat_event, 0)
            pygame.time.set_timer(self.acc_repeat_event, 0)
            pygame.time.set_timer(self.fire_phaser_repeat_event, 0)
            pygame.time.set_timer(self.fire_torpedoes_repeat_event, 0)

            pygame.event.clear(
                (
                    self.rotate_cc_repeat_event,
                    self.rotate_cw_repeat_event,
                    self.acc_repeat_event,
                    self.fire_torpedoes_repeat_event,
                    self.fire_phaser_repeat_event,
                )
            )
            return

        self._handle_movement_events(event)
        self._handle_firing_weapon_events(event)
