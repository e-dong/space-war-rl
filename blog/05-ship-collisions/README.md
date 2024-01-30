_This marks the final installment of my blog series covering the v0.4 release of Space War RL! With these simulation updates concluded, my focus will shift towards Reinforcement Learning in future posts._

<hr>

## Collision Resolution Process

The general process is to first detect when the ship collides with another ship and to adjust their velocities accordingly.

Initially, I attempted to resolve collisions by swapping the velocities of the colliding ships:

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

However, I later opted to introduce energy loss by reducing the other ship's velocity by 50%:

```python
new_self_vel_x = other_vel_x * 0.50
new_self_vel_y = other_vel_y * 0.50
new_other_vel_x = self_vel_x * 0.50
new_other_vel_y = self_vel_y * 0.50
```

<div align="center">
  <img width="100%" src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/zuoz2c5gcq9jkvigkcts.gif" /> <figcaption><i><b>Ship collisions v1</b>: Gain 50% of the other ship's velocity</i></figcaption>
</div>

My physics friend corrected me, explaining that momentum should be conserved, implying that the ship should continue moving forward after colliding with another ship. This looks more natural!

```python
new_self_vel_x = (self_vel_x * 0.2) + (other_vel_x * 0.75)
new_self_vel_y = (self_vel_y * 0.2) + (other_vel_y * 0.75)
new_other_vel_x = (other_vel_x * 0.2) + (self_vel_x * 0.75)
new_other_vel_y = (other_vel_y * 0.2) + (self_vel_y * 0.75)
```

<div align="center">
  <img width="100%" src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/yokxs0dhivrwszmzjc7s.gif" /> <figcaption><i><b>Ship collisions v2</b>: Maintain 20% of original velocity and gain 75% of the other ship's velocity</i></figcaption>
</div>

In the future, I may want to take mass into account for collisions.

## Handling Sprite Overlap

A major and unexpected problem I encountered was when the ships overlapped due to a "low-force" collision.

<div align="center">
  <img width="100%" src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/bb9albudy8rxiijlqtwy.gif" /> <figcaption><i><b>OH NO!</b></i></figcaption>
</div>

I created this util function to determine the amount of overlap. I compare the center point of each colliding sprites to compute the direction of collision.

```python
def check_overlapping_sprites(
    sprite: pygame.sprite.Sprite, sprite_other: pygame.sprite.Sprite
):
    """Returns the horizontal and vertical overlap between two sprites."""
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

<div align="center">
  <figcaption><i>Perhaps there is a better way, but this will work for now.</i></figcaption>
</div>

If I update the position of the sprites to avoid overlap, the sudden movement looks jarring and unnatural.

```python
# detect any overlap and move the ships
overlap_x, overlap_y = check_overlapping_sprites(self, sprite)

sprite.pos = (sprite.pos[0] + overlap_x, sprite.pos[1] + overlap_y)
```

<div align="center">
  <img width="100%" src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/xne368jlpi39kylgfwq7.gif" /> <figcaption><i>Sprite overlap fix v1</i></figcaption>
</div>

Looking at the emulator for comparison, I noticed it is doing something similar.

<div align="center">
  <img width="100%" src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vzta61m1wcwctc1z979s.gif" /> <figcaption><i>Ship collisions in Emulator</i></figcaption>
</div>

Both of the ships' positions are adjusted. I could do something similar where I apply half of the overlap to the first sprite and the other half to the second sprite, but I didn't want to do this.

For a more natural looking approach, if there is any overlap, move the sprites naturally by using their velocities.

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
  <img width="100%" src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/g9pzhgcqivub34z6wafz.gif" /> <figcaption><i>Sprite overlap fix v2. Note that angular velocities and collisions are not considered in this simulation.</i></figcaption>
</div>

This looks much better in my opinion. Instead of updating the ships' positions immediately, I can move them away from each other using their new velocities after collision. This continues until there is no overlap.

My goal is not to make a perfect physics simulation, so this is sufficient. I may use Unreal or Unity in the future to take advantage of the physics engine.

## Next Up

I will be doing a mini-post on using github actions to automate deployment of my simulation to itch.io. After that, I will be drawing pixel art for the player 2 ship and preparing to train my agent using the DQN algorithm. I will see how much I can learn and implement from attempting to derive everything from [Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602).
