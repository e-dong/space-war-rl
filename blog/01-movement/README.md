## Selecting the Appropriate Simulator

I was deciding whether I should use game engines like Godot, Unity, or Unreal, but ended using `pygame`. ML libraries are primarily in python, so `pygame` and OpenAI `gym` are a good choice. Space War also has simple graphics, so I don't need the overhead of the game engine. I ended up going with `pygame` because I only used `gym` at work and wanted to try something new. `pygame` also seemed easier to add my own graphics, add human controls, and manage collisions (e.g. implement damage dealt to player from weapons) compared to `gym`. However if I want to make the simulation more complex and add game-like features, I will revisit game engines. I think having a level editor would be helpful if I want to test if RL agents can generalize to different environments. I may also try using a game engine to train RL agents in 3D environments, but that's for a future project!

## Selecting the Appropriate ML Framework

I will be using `pytorch` because I used that ML framework in the past. Others have said `pytorch` is more [pythonic](https://stackify.com/tensorflow-vs-pytorch-which-deep-learning-framework-is-right-for-you/) than `tensorflow` as well.

## Learning Pygame

I first discovered `pygame` when I found this pygame [project](https://github.com/1391819/MA-seek) using tensorflow at work, but ran out of time to dig deeper into his implementation. These are the steps I took to start learning more about `pygame`.

1. The pygame documentation recommend this [video tutorial](https://youtu.be/AY9MnQ4x3zk?si=nBiH5ge5GTc0mov_) and I totally agree. The content is well organized and presented clearly. I didn’t code along with the author, but I looked at what parts were relevant and applied it to my own game.
1. Looked up documentation on the `Sprite` [module](https://www.pygame.org/docs/tut/SpriteIntro.html).
1. Used the quick-start code from the [pygame documentation](https://www.pygame.org/docs/)

```python
# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.circle(screen, "white", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
```

### Demo

![quick start](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1i14jtxxgxbcjneax83e.gif) <figcaption>Using quickstart code to move a white circle using the W-A-S-D keys.

## Adding Player One Pixel Art

Since the graphics in space war is simple (all white, no shaders), I drew my own pixel art by copying what player 1 looked like.

I'm no artist, so I just searched reddit to see pixel art apps that supports Linux and stumbled upon [mtpaint](https://mtpaint.sourceforge.net/). The player ships were symmetric, so I just drew the top half and mirrored it to make the bottom half. Let me know if you have a favorite pixel art tool!

![pixel art](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/cugk2wrfwlmf9fls0o4h.png) <figcaption>Screenshot of player one ship in mtpaint</figcaption>

## Replacing Circle with Ship Image

I added a separate `Player` class that extends from the `Sprite` class to manage its state.

```python
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
            y_pos -= 0.05 * SCREEN_HEIGHT * self.delta_time
        if keys[K_s]:
            y_pos += 0.05 * SCREEN_HEIGHT * self.delta_time
        if keys[K_a]:
            x_pos -= 0.05 * SCREEN_WIDTH * self.delta_time
        if keys[K_d]:
            x_pos += 0.05 * SCREEN_WIDTH * self.delta_time
        self.pos = (x_pos, y_pos)
        self.rect.x = x_pos
        self.rect.y = y_pos

    def update(self):
        """Entrypoint for updating the player state each frame"""
        self.handle_input()
```

main game loop:

```python
def main():
    """Entrypoint for starting up the pygame"""
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # delta time in seconds since last frame, used for framerate-
    # independent physics.
    clock = pygame.time.Clock()
    delta_time = clock.tick(MAX_FPS) / 1000

    # Groups
    player_single_group = pygame.sprite.GroupSingle()
    player_single_group.add(
        Player(
            delta_time=delta_time,
            image_path=module_path() / "assets" / "player_1.png",
            start_pos=(screen.get_width() / 2, screen.get_height() / 2),
        )
    )

    running = True

    while running:
        # event loop
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        player_single_group.draw(screen)
        player_single_group.update()

        pygame.display.update()

    pygame.quit()
```

### Demo of [v0.1](https://github.com/e-dong/space-war-rl/tree/v0.1)

![Replace circle with ship image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ermzlputlgt0g3o8vnlo.gif) <figcaption>Using a sprite to replace the white circle with the ship image</figcaption>

## Updating Player Movement

The ship should be able to rotate and only move in the direction it is facing.

I added a field to keep track of the angle of the ship and updated the `if` statements like so:

```python
if keys[K_a]:
    self.ang -= 50 * self.delta_time
if keys[K_d]:
    self.ang += 50 * self.delta_time
...
self.ang = self.ang % 360
```

Next, the surface needs to be rotated so we can update the sprite's image.

```python
# Update rotation
current_rect = self.surf.get_rect()
newsurf = transform.rotate(self.surf, -self.ang)
newrect = newsurf.get_rect()
# put new surface rect center on same spot as old surface rect center
self.rect.x += current_rect.centerx - newrect.centerx
self.rect.y += current_rect.centery - newrect.centery
self.image = newsurf
```

For forward movement, I removed the handler for the `w` key and updated the `s` key.

```python
x_pos, y_pos = self.pos
if keys[K_s]:
    x_pos += 30 * self.delta_time * math.cos(self.ang * math.pi / 180)
    y_pos += 30 * self.delta_time * math.sin(self.ang * math.pi / 180)
...
self.pos = (x_pos, y_pos)
self.rect.x = x_pos
self.rect.y = y_pos
```

The formula is derived from [SOHCAHTOA](https://mathworld.wolfram.com/SOHCAHTOA.html). The `sine` of `theta` (the angle) is `the length of opposite side / length of hypotenuse` and the `cosine` of `theta` is `length of adjacent side / length of hypotenuse`.

In the context of this simulation:

- `theta` is the angle the player is facing (0 - 359)
- `opposite side` is the change in `y`
- `adjacent side` is the change in `x`
- `hypotenuse` is the distance traveled.

Therefore I can calculate the new player's relative position via

- `delta_y = dist * sin(angle)`
- `delta_x = dist * cos(angle)`

The angle is multiplied by `pi/180` to convert to radians.

I'm glad I remembered my high school trigonometry!

### Demo of [v0.2](https://github.com/e-dong/space-war-rl/tree/v0.2)

![proper movement](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tjtjkdk234451ml2rkk0.gif) <figcaption>Ship can rotate with A-D keys (counterclockwise and clockwise respectively) and move in the current direction it is facing with the 'S' key. When 'S' is released, the ship stops moving forward.</figcaption>

Thank you for reading my blog! The next blog post will be on adding zero gravity physics to the environment.
