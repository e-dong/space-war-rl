"""Collection of Base Sprite Classes
     - SpaceEntity
"""
import pygame

from game.conf import SCREEN_HEIGHT, SCREEN_WIDTH


class SpaceEntity(pygame.sprite.Sprite):
    """A base class for objects that move in space,
    like ships and projectiles
    """

    def __init__(self, start_pos, start_ang, surf) -> None:
        super().__init__()
        self.surf = surf
        self.image = surf
        self.pos = start_pos
        self.rect = self.surf.get_rect(center=self.pos)
        self.x_vel = 0
        self.y_vel = 0
        self.ang = start_ang

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
        self.ang %= 360
        newsurf = pygame.transform.rotate(self.surf, -self.ang)
        self.rect = newsurf.get_rect(center=self.pos)
        self.image = newsurf
