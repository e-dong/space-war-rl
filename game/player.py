"""Collection of Player Classes"""
import math

from pygame import KEYDOWN, KEYUP, image, key, transform
from pygame.constants import K_a, K_d, K_s
from pygame.event import Event
from pygame.sprite import Sprite

from game.conf import SCREEN_HEIGHT, SCREEN_WIDTH


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

    def handle_events(self, event: Event, check_key_event: Event):
        """Handles keyboard input to update ship's rotation and position
        state
        """
        if event.type == KEYDOWN:
            # Handle ship movement and rotation
            if event.key == K_a:
                self.rotate_ccw_lock = True
                self.ang -= 22.5
            if event.key == K_d:
                self.rotate_ccw_lock = False
                self.ang += 22.5
            if event.key == K_s:
                self.x_vel += math.cos(self.ang * math.pi / 180)
                self.y_vel += math.sin(self.ang * math.pi / 180)
        if event.type == KEYUP:
            if event.key == K_a:
                self.rotate_ccw_lock = False
            if event.key == K_d:
                self.rotate_ccw_lock = True
        if event.type == check_key_event:
            keys = key.get_pressed()
            rotate_ccw = keys[K_a] and self.rotate_ccw_lock
            rotate_cc = keys[K_d] and not self.rotate_ccw_lock
            accelerate = keys[K_s]

            # Update acceleration
            if accelerate:
                self.x_vel += math.cos(self.ang * math.pi / 180)
                self.y_vel += math.sin(self.ang * math.pi / 180)
            # Update rotation
            if rotate_ccw:
                self.ang -= 22.5
            elif rotate_cc:
                self.ang += 22.5
            self.ang %= 360

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
