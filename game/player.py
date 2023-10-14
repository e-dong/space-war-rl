"""Collection of Player Classes"""
from pygame import image, key
from pygame.constants import K_a, K_d, K_s, K_w
from pygame.sprite import Sprite


class Player(Sprite):
    """Represents the human player"""

    def __init__(self, delta_time, image_path, start_pos) -> None:
        super().__init__()
        self.surf = image.load(image_path).convert_alpha()
        self.image = self.surf
        self.pos = start_pos
        self.rect = self.surf.get_rect(midbottom=self.pos)
        self.delta_time = delta_time

    def handle_input(self):
        """Handles keyboard input to update the player's position"""
        keys = key.get_pressed()
        x_pos, y_pos = self.pos
        if keys[K_w]:
            y_pos -= 30 * self.delta_time
        if keys[K_s]:
            y_pos += 30 * self.delta_time
        if keys[K_a]:
            x_pos -= 30 * self.delta_time
        if keys[K_d]:
            x_pos += 30 * self.delta_time
        self.pos = (x_pos, y_pos)
        self.rect.x = x_pos
        self.rect.y = y_pos

    def update(self):
        """Entrypoint for updating the player state each frame"""
        self.handle_input()
