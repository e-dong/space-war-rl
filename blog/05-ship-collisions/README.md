_This is my blog part 3 of 3 for the v0.4 release of Space War RL! This concludes the simulation updates for now. My future development and posts will transition more into Reinforcement Learning_

<hr>

The general process is to first detect when the ship collides with another ship and to adjust their velocities.

My first thought is to swap their velocities.

```python
self_vel_x, self_vel_y = self.vel
other_vel_x, other_vel_y = sprite.vel

# Swap velocities
new_self_vel_x = other_vel_x
new_self_vel_y = other_vel_y
new_other_vel_x = self_vel_x
new_other_vel_y = self_vel_y

self.vel = (new_self_vel_x, new_self_vel_y)
sprite.vel = (new_other_vel_x, new_other_vel_y)
```

<div align="center">
  <img width="100%" src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/gtm8dw809up68ell0e2k.gif" /> <figcaption><i><b>Ship collisions v0</b>: Represents a perfect system with no energy loss.</i></figcaption>
</div>

I decided to add some energy loss due to collision. So lets multiply the other's velocity by a percent.

```python
new_self_vel_x = other_vel_x * 0.50
new_self_vel_y = other_vel_y * 0.50
new_other_vel_x = self_vel_x * 0.50
new_other_vel_y = self_vel_y * 0.50
```

<div align="center">
  <img width="100%" src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/zuoz2c5gcq9jkvigkcts.gif" /> <figcaption><i><b>Ship collisions v1</b>: Gain 50% of the other ship's velocity</i></figcaption>
</div>

My physics friend corrected me and said momentum needs to be conserved. This means that the ship should still move forward after colliding with the ship. This looks more natural!

```python
new_self_vel_x = (self_vel_x * 0.2) + (other_vel_x * 0.75)
new_self_vel_y = (self_vel_y * 0.2) + (other_vel_y * 0.75)
new_other_vel_x = (other_vel_x * 0.2) + (self_vel_x * 0.75)
new_other_vel_y = (other_vel_y * 0.2) + (self_vel_y * 0.75)
```

<div align="center">
  <img width="100%" src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/yokxs0dhivrwszmzjc7s.gif" /> <figcaption><i><b>Ship collisions v2</b>: Maintain 20% of original velocity and gain 75% of the other ship's velocity</i></figcaption>
</div>

One major problem I ran into is when the ship overlaps with each other.

<div align="center">
  <img width="100%" src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/bb9albudy8rxiijlqtwy.gif" /> <figcaption><i>Sprite overlap issue</i></figcaption>
</div>

I created this util function to determine the amount of overlap.

```python
def check_overlapping_sprites(
    sprite: pygame.sprite.Sprite, sprite_other: pygame.sprite.Sprite
):
    """Returns the amount of overlap between 2 sprites"""
    overlap_x, overlap_y = (0, 0)
    if sprite.rect.centerx < sprite_other.rect.centerx:
        overlap_x = sprite.rect.right - sprite_other.rect.left
    elif sprite.rect.centerx > sprite_other.rect.centerx:
        overlap_x = -(sprite_other.rect.right - sprite.rect.left)

    if sprite.rect.centery < sprite_other.rect.centery:
        overlap_y = sprite.rect.bottom - sprite_other.rect.top
    elif sprite.rect.centery > sprite_other.rect.centery:
        overlap_y = -(sprite_other.rect.bottom - sprite.rect.top)

    return overlap_x, overlap_y
```

If I update the position of the sprites to not overlap, it is a bit jarring and unnatural.

```python
 # detect any overlap and move the ships
 overlap_x, overlap_y = check_overlapping_sprites(self, sprite)

sprite.pos = (sprite.pos[0] + overlap_x, sprite.pos[1] + overlap_y)
```

<div align="center">
  <img width="100%" src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/xne368jlpi39kylgfwq7.gif" /> <figcaption><i>Sprite overlap fix v1</i></figcaption>
</div>

Looking at the emulator for comparison and I noticed it is doing something similar. Looks like both ships' positions are adjusted.

<div align="center">
  <img width="100%" src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vzta61m1wcwctc1z979s.gif" /> <figcaption><i>Ship collisions in Emulator</i></figcaption>
</div>

To make this more natural, if there is any overlap, move the sprites naturally by using their velocities.

```python
# detect any overlap and move the ships
overlap_x, overlap_y = check_overlapping_sprites(self, sprite)

if overlap_x:
    sprite.pos = (sprite.pos[0] + sprite.vel[0], sprite.pos[1])
if overlap_y:
    sprite.pos = (
        sprite.pos[0],
        sprite.pos[1] + sprite.vel[1],
    )
```

<div align="center">
  <img width="100%" src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/g9pzhgcqivub34z6wafz.gif" /> <figcaption><i>Sprite overlap fix v2</i></figcaption>
</div>

My goal isn't to make a physics accurate simulation, so this will be good enough. I may use Unreal or Unity in the future to take advantage of the physics engine.

## Next Up

I will be doing a mini-post on using github actions to automate deployment of my simulation to itch.io. After that, I will be drawing pixel art for the player 2 ship and preparing to train my agent using the DQN algorithm. I will see how far I can learn and implement from trying to derive everything from [Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602).
