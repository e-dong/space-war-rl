_This is my blog part 2 of 3 for the v0.4 release of Space War RL!_

## Making a Common Base Class

The `HumanShip` class contains logic for applying screen wrap-around, velocity, and rotation.
Since I want the other objects to have this same logic, I can extract this into a common base class.

```python
class SpaceEntity(pygame.sprite.Sprite):
   ...

    def update(self, *_args, **kwargs):
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

```

<div align="center">
  <figcaption><i>The <code>SpaceEntity</code> base class represents flying objects in space. See <a href="">space_war/sim/base.py</a> for the full source</i>
  </figcaption>
</div>

I also have a base class to represent a weapon.

```python
class BaseWeapon(pygame.sprite.Sprite):
    """Simple base class for weapons. All weapons have a specific duration."""

    def __init__(self, duration) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.start_time = pygame.time.get_ticks()
        self.max_duration = duration

    def is_expired(self) -> bool:
        """Returns True if duration of weapon exceeds the max duration"""
        current_duration = pygame.time.get_ticks() - self.start_time
        return current_duration >= self.max_duration

    def update(self, *args: Any, **kwargs: Any):
        """Update entrypoint for weapons"""
        super().update(*args, **kwargs)
        if self.is_expired():
            self.kill()
```

<div align="center">
  <figcaption><i>See <a href="">space_war/sim/weapon.py</a> for the full source</i>
  </figcaption>
</div>

## Adding Photon Torpedoes

The photon torpedoes were pretty easy to implement, since I could inherit the logic from my base class.
The graphics in the original were boring, so I drew my own torpedo. Pygame comes with some utils to draw lines and polygons:

```python
pygame.draw.polygon(self.image, "white", [[5, 0], [3, 5], [7, 5]], 1)
pygame.draw.polygon(self.image, "white", [[0, 10], [3, 9], [3, 5]], 1)
pygame.draw.polygon(self.image, "white", [[7, 5], [7, 9], [11, 10]], 1)
pygame.draw.line(self.image, "white", (3, 9), (7, 9))
pygame.draw.line(self.image, "white", (5, 5), (5, 11))
```

<div align="center">
  <img width="100%" src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/39tr9okbnouwcx83xod4.png"/> <figcaption><i>Closeup of firing Photon Torpedoes</i></figcaption>
</div>

## Adding Phasers

Adding phasers on the other hand was more complicated than I initially thought. I ended up making 3 revisions of the implementation. I started off using the `SpaceEntity` base class and realized screen wrap around won't work correctly. The base class assumes there is one rectangle. This works fine to represent individual ships and torpedoes. For screen wrap around to work correctly, I need at least 2 rectangles. One is drawn to the edge of the screen and the rest continues on the other side of the screen.

My implementation consists of three steps:

1. Create invisible hit detector rectangles
1. Detect collisions with ships or other torpedoes
1. Draw the phaser line

<div align="center">
  <img width="100%" src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/w5f8r0ud9xxnhes98epn.png" /> <figcaption><i>Closeup of firing Phasers</i></figcaption>
</div>

## Putting Everything Together

The final step is to detect collisions between the weapons and ships. For this iteration, being hit with a weapon will result in death. Torpedoes can collide with other torpedoes and ships. Phasers can only collide with torpedoes and the other ship.

<div align="center">
  <img width="100%" src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/t6xz7amzim5g5vu6399v.gif" /> <figcaption><i>GIF of weapons demo</i></figcaption>
</div>

## Next Steps

My next blog will show some physics I added for ship on ship collisions! Thank you for reading.
