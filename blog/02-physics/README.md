---
title: Adding Physics and Finalizing Player Movement
series: Space War RL Dev Blog
published: false
description:
tags: reinforcementlearning,ai, pygame, spacewar
cover_image: https://res.cloudinary.com/practicaldev/image/fetch/s--24gbx7Fs--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_66%2Cw_800/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/mr8wm4n8vtzvzbsy33ck.gif
# cover_image: https://direct_url_to_image.jpg
# Use a ratio of 100:42 for best results.
# published_at: 2023-10-29 14:31 +0000
---

_This is an update for v0.3 of Space War RL! I made more updates to the player movement._

## Making Ship Rotation more Discrete

In the emulator, I noticed each keypress of the rotation keybinding would rotate the ship by 22.5 degrees (4 key presses for a 90 degree turn).
The current rotation handling logic is being called from the player's `update` function, which gets called every frame. I was using `pygame.key.get_pressed`, which is only used to check which keys are currently pressed down. What I want is to detect _when_ the rotation key is pressed down and increment or decrement the angle by 22.5. I will need to check the rotation keybinding in the event loop.

[main.py](https://github.com/e-dong/space-war-rl/blob/db4938d3a20472fe546ec5ad35a68be2e9497553/game/main.py)

```python
while running:
    # event loop
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        player_1.handle_events(event)
        if event.type == pygame.QUIT:
            running = False
```

[player.py](https://github.com/e-dong/space-war-rl/blob/db4938d3a20472fe546ec5ad35a68be2e9497553/game/player.py)

```python
def handle_events(self, event: Event):
    """Handles keyboard input to update ship's rotation and position state"""
    if event.type == KEYDOWN:
        ...
        if event.key == K_a:
            self.ang -= 22.5
        if event.key == K_d:
            self.ang += 22.5
        self.ang = self.ang % 360
```

I also added `pygame.key.set_repeat(100, 100)` in [main.py#L14](https://github.com/e-dong/space-war-rl/blob/db4938d3a20472fe546ec5ad35a68be2e9497553/game/main.py#L14) to allow the `KEYDOWN` event to be repeated every 100ms, so I can hold down the rotation keybinding, otherwise it is only triggered once per keypress.

### Demo

![discrete rotation ](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/q565w6t52yybolpy662i.gif) <figcaption>Made ship rotation more discrete, rotations are made in 22.5 degree increments</figcaption>

A possible alternate implementation is using `numpy` and indexing through the array.

```
>>> import numpy as np
>>> np.arange(0, 360, 22.5)
array([  0. ,  22.5,  45. ,  67.5,  90. , 112.5, 135. , 157.5, 180. ,
       202.5, 225. , 247.5, 270. , 292.5, 315. , 337.5])
```

I noticed my implementation didn't handle multiple keypresses and release correctly. I took a look at the emulator and it's not perfect either.

![emulator rotation bug](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/hi4f24rqeoi2bnh9pkbz.gif) <figcaption>Holding down 'A' first and then holding down 'D' correctly switches the player's rotation from counterclockwise to clockwise. Holding down 'D' first and then pressing 'A' <b>DOES NOT</b> switch the rotation from clockwise to counterclockwise</figcaption>

It looks like the check for 'D' is overriding the check for 'A'. This is the pseudocode I'm thinking that's causing this behavior in the emulator.

```
IF (D is down) THEN
    rotate clockwise
ELSE IF (A is down) THEN
    rotate counterclockwise
```

The check for D appears to be first causing inconsistent behavior. I want to see if I can check my Dad's computer to see if this is in the original game.

I decided not to copy this behavior and fixed it in my implementation.

This is the code that fixes this bug.

```python
def handle_events(self, event: Event, check_key_event: Event):
    """Handles keyboard input to update ship's rotation and position
    state
    """
    if event.type == KEYDOWN:
        # Handle ship movement and rotation
        if event.key == K_a:
            self.rotate_ccw_lock = True
        if event.key == K_d:
            self.rotate_ccw_lock = False
    if event.type == KEYUP:
        if event.key == K_a:
            self.rotate_ccw_lock = False
        if event.key == K_d:
            self.rotate_ccw_lock = True
    if event.type == check_key_event:
        keys = key.get_pressed()
        rotate_ccw = keys[K_a] and self.rotate_ccw_lock
        rotate_cc = keys[K_d] and not self.rotate_ccw_lock
        ...
        # Update rotation
        if rotate_ccw:
            self.ang -= 22.5
        elif rotate_cc:
            self.ang += 22.5
        self.ang %= 360
```

I am using the the `self.rotate_ccw_lock` field as a way to detect when the `A` or `D` is first pressed or released.

For input check throttling, I replaced the `pygame.key.set_repeat` function with a custom user event to check user input.

```python
# create custom event to check user input
check_key_event = pygame.USEREVENT + 1
pygame.time.set_timer(check_key_event, CHECK_KEYS_TIME_DELAY_MS)
...

while running:
    # event loop
    for event in pygame.event.get():
        player_one.handle_events(event, check_key_event)
```

### Demo

![Rotation Fix](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/qzlenmcydmacnd3mydum.gif) <figcaption>Rotation Fix</figcaption>

---

## Adding Zero Gravity Physics

From my [previous blog post](https://dev.to/edong/space-war-rl-1-getting-started-and-adding-player-movement-h7h#updating-player-movement), I discovered this formula to calculate the new relative `x` and `y` coordinates:

```
delta_y = dist * sin(angle)
delta_x = dist * cos(angle)
```

To add velocity, the player just needs to keep track of its net `x` and `y` velocity and each frame would add the net velocities to the player's current position.

```python
def handle_events(self, event: Event, check_key_event: Event):
    """Handles keyboard input to update ship's rotation and position
    state
    """
    ...
    if event.type == check_key_event:
        keys = key.get_pressed()
        ...
        accelerate = keys[K_s]

        # Update acceleration
        if accelerate:
            self.x_vel += math.cos(self.ang * math.pi / 180)
            self.y_vel += math.sin(self.ang * math.pi / 180)
    ...

def update(self, *args, **kwargs):
    """Entrypoint for updating the player state each frame"""
    x_pos, y_pos = self.pos

    ...

    # Apply velocity to position
    x_pos += self.x_vel
    y_pos += self.y_vel
    self.rect.x = x_pos
    self.rect.y = y_pos
    self.pos = (x_pos, y_pos)

    ...
```

After making these changes, I noticed a design pattern has emerged.

1. In the event loop, the `handle_events` function is used to update the player's internal state from user input. E.g. calculate changes in the net `x` and `y` velocity as well as the `angle`.
1. The `update` function is used to apply the values of the internal state variables to the environment. E.g. updating the player's position from net velocity and applying rotation to the surface from the angle.

### Demo

![zero gravity physics](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vz0ygb4hzezet17zlojy.gif) <figcaption>Applying velocity instead of a fixed distance for movement. At the end of the gif, the player moves to the upper right and then out of bounds.</figcaption>

Whoops, it is easy to go out of bounds now! I will be adding screen wrap-around for this for now, since that is present in the original game. In other environment simulations, the bounds are restricted, so it is like the agent is in a box. Trying to move beyond the boundaries will place the agent at the boundary. Another method in RL is to punish the agent from going out of bounds via a negative reward. The agent can still go out of bounds, but hopefully it learns not to do that with training. The latter is more realistic.

## Adding Screen Wrap-Around

```python
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
```

### Demo

![screen wrap-around](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ol4iz6za1089up3mduxe.gif) <figcaption>Added screen wrap-around to prevent the ship from going out of bounds</figcaption>

Thank you for reading my blog! My next blog post will discuss adding weapons to the agent.
