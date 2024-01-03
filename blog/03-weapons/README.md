_This is the weapon's update for v0.4 of Space War RL! I added phasers and photon torpedoes_

## Making a Common Base Class

The `HumanShip` class contains the logic for applying screen wrap-around, velocity, and rotation.
Since I want the other objects to have this same logic, I can extract this into a base class.

```python
import pygame

from space_war.sim.conf import SCREEN_HEIGHT, SCREEN_WIDTH, SpaceEntityType


class SpaceEntity(pygame.sprite.Sprite):
    """A base class for objects that move in space, like ships and projectiles.

    Features screen wrap-around, frictionless/zero gravity physics, and
    rotation. Subclasses should implement collision handling.

    Attributes
    ----------
    entity_type: The type of space entity
    surf: The reference to the original Surface, used for rotation
    image: The reference to the latest surface based on the other
           state vars
    pos: The x,y of the position on the screen
    rect: The rect object
    vel: The velocity of the space entity
    ang: The angle in degrees representing the direction the ship is facing
    """

    entity_type: SpaceEntityType
    surf: pygame.surface.Surface
    image: pygame.surface.Surface
    pos: tuple[int, int]
    rect: pygame.rect.Rect
    vel: tuple[float, float]
    ang: float

    def __init__(
        self,
        entity_type,
        surf,
        start_pos,
        start_ang=0,
        start_vel=(0, 0),
        rotation_point=None,
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.entity_type = entity_type
        self.surf = surf
        self.image = surf
        self.pos = start_pos
        self.rotation_point = rotation_point
        if self.rotation_point:
            self.rect = surf.get_rect(center=self.rotation_point)
        else:
            self.rect = surf.get_rect(center=start_pos)

        self.vel = start_vel
        self.ang = start_ang

    def update(self, *_args, **kwargs):
        """Entrypoint for updating the player state each frame

        screen_wrap, pos, and rotation updates can be disabled if set to False
        """
        x_pos, y_pos = self.pos
        x_vel, y_vel = self.vel

        screen_wrap = kwargs["screen_wrap"] if "screen_wrap" in kwargs else True
        # conditions for wrapping around the screen
        if screen_wrap:
            if x_pos >= SCREEN_WIDTH:
                x_pos = 0
            elif x_pos <= 0:
                x_pos = SCREEN_WIDTH
            if y_pos >= SCREEN_HEIGHT:
                y_pos = 0
            elif y_pos <= 0:
                y_pos = SCREEN_HEIGHT

        # apply velocity to position
        update_pos = kwargs["update_pos"] if "update_pos" in kwargs else True
        if update_pos:
            x_pos += x_vel
            y_pos += y_vel
            self.pos = (x_pos, y_pos)
            self.rect.center = self.pos

        # update rotation to surface
        rotation = kwargs["rotation"] if "rotation" in kwargs else True
        if rotation:
            self.ang %= 360
            self.image = pygame.transform.rotate(self.surf, -self.ang)
            rotation_point = (
                self.rotation_point if self.rotation_point else self.pos
            )
            self.rect = self.image.get_rect(center=rotation_point)
```

## Adding Photon Torpedoes

<div align="center">
    <img width="100%" src="photon_torpedo_closeup.png"/>
    <figcaption>Closeup of firing Photon Torpedoes</figcaption>
</div>

## Adding Phasers

<div align="center">
    <img width="100%" src="phasers_closeup.png" />
    <figcaption>Closeup of firing Phasers</figcaption>
</div>

## Next Steps

I was originally planning to start training agents after implementing energy and shields management, but I have enough features implemented to get started.
