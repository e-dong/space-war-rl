"""Collection of Player Classes"""
import math

from pygame import KEYDOWN, image, transform
from pygame.constants import K_a, K_d, K_s
from pygame.event import Event
from pygame.sprite import Sprite

from game.conf import SCREEN_HEIGHT, SCREEN_WIDTH


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
        self.x_vel = 0
        self.y_vel = 0

    def handle_events(self, event: Event):
        """Handles keyboard input to update ship's rotation and position state"""
        if event.type == KEYDOWN:
            # Handle ship movement and rotation
            if event.key == K_s:
                self.x_vel += 0.2 * math.cos(self.ang * math.pi / 180)
                self.y_vel += 0.2 * math.sin(self.ang * math.pi / 180)
            if event.key == K_a:
                self.ang -= 22.5
            if event.key == K_d:
                self.ang += 22.5
            self.ang = self.ang % 360

    def update(self, *args, **kwargs):
        """Entrypoint for updating the player state each frame"""
        x_pos, y_pos = self.pos

        # Conditions for wrapping around the screen
        if x_pos >= SCREEN_WIDTH:
            x_pos = 0
        elif x_pos <= 0:
            x_pos = SCREEN_WIDTH
        if y_pos >= SCREEN_HEIGHT:
            y_pos = 0
        elif y_pos <= 0:
            y_pos = SCREEN_HEIGHT

        # Apply velocity to position
        x_pos += self.x_vel
        y_pos += self.y_vel

        self.rect.x = x_pos
        self.rect.y = y_pos
        self.pos = (x_pos, y_pos)
        # Update rotation
        current_rect = self.surf.get_rect()
        newsurf = transform.rotate(self.surf, -self.ang)
        newrect = newsurf.get_rect()

        # put new surface rect center on same spot as old surface rect center
        self.rect.x += current_rect.centerx - newrect.centerx
        self.rect.y += current_rect.centery - newrect.centery
        self.image = newsurf
