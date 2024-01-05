"""Collection of Base Sprite Classes
     - SpaceEntity
"""
import pygame

from space_war.sim.conf import SCREEN_HEIGHT, SCREEN_WIDTH, SpaceEntityType


class SpaceEntity(pygame.sprite.Sprite):
    """A base class for visible objects that move in space, like ships and projectiles.

    Features screen wrap-around, frictionless/zero gravity physics, and
    rotation. Subclasses should implement collision handling.

    Attributes
    ----------
    entity_type: The type of space entity
    surf: The reference to the original Surface, used for rotation
    pos: The x,y of the rect's center position on the screen
    vel: The velocity of the space entity
    ang: The angle in degrees representing the direction the ship is facing
    """

    entity_type: SpaceEntityType
    surf: pygame.surface.Surface
    pos: tuple[int, int]
    vel: tuple[float, float]
    ang: float

    def __init__(
        self,
        entity_type,
        surf,
        start_pos,
        start_ang=0,
        start_vel=(0, 0),
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.entity_type = entity_type
        self.surf = surf
        self.image = surf
        self.pos = start_pos
        self.rect = surf.get_rect(center=start_pos)
        self.vel = start_vel
        self.ang = start_ang

    def update(self, *_args, **_kwargs):
        """Entrypoint for updating the player state each frame

        screen_wrap, pos, and rotation updates can be disabled if set to False
        """
        x_pos, y_pos = self.pos
        x_vel, y_vel = self.vel

        # conditions for wrapping around the screen
        if x_pos >= SCREEN_WIDTH:
            x_pos = 0
        elif x_pos <= 0:
            x_pos = SCREEN_WIDTH
        if y_pos >= SCREEN_HEIGHT:
            y_pos = 0
        elif y_pos <= 0:
            y_pos = SCREEN_HEIGHT

        # apply velocity to position
        x_pos += x_vel
        y_pos += y_vel
        self.pos = (x_pos, y_pos)
        self.rect.center = self.pos

        # update rotation to surface
        self.ang %= 360
        self.image = pygame.transform.rotate(self.surf, -self.ang)
        self.rect = self.image.get_rect(center=self.pos)
