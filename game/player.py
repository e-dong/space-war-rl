"""Collection of Player Classes"""
import math

from pygame import image, key, transform
from pygame.constants import K_a, K_d, K_s
from pygame.sprite import Sprite


class Player(Sprite):
    """Represents the human player"""

    def __init__(self, delta_time, image_path, start_pos, start_ang=0) -> None:
        super().__init__()
        self.surf = image.load(image_path).convert_alpha()
        self.ang = start_ang
        self.image = self.surf
        self.pos = start_pos
        self.rect = self.surf.get_rect(center=self.pos)
        self.delta_time = delta_time

    def handle_input(self):
        """Handles keyboard input to update ship's rotation and position"""
        keys = key.get_pressed()

        # Handle ship movement and rotation
        x_pos, y_pos = self.pos
        if keys[K_s]:
            x_pos += 30 * self.delta_time * math.cos(self.ang * math.pi / 180)
            y_pos += 30 * self.delta_time * math.sin(self.ang * math.pi / 180)
        if keys[K_a]:
            self.ang -= 50 * self.delta_time
        if keys[K_d]:
            self.ang += 50 * self.delta_time
        self.pos = (x_pos, y_pos)
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.ang = self.ang % 360

        # Update rotation
        current_rect = self.surf.get_rect()
        newsurf = transform.rotate(self.surf, -self.ang)
        newrect = newsurf.get_rect()
        # put new surface rect center on same spot as old surface rect center
        self.rect.x += current_rect.centerx - newrect.centerx
        self.rect.y += current_rect.centery - newrect.centery
        self.image = newsurf

    def update(self, *args, **kwargs):
        """Entrypoint for updating the player state each frame"""
        self.handle_input()
