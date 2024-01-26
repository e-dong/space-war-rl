_This is my blog part 3 of 3 for the v0.4 release of Space War RL! This concludes the simulation updates for now. My future development and posts will transition more into Reinforcement Learning_

The general process is to first detect when the ship collides with another ship and to adjust their velocities.

My first thought is to swap their velocities.

```python
self_vel_x, self_vel_y = self.vel
other_vel_x, other_vel_y = sprite.vel

# preserve 20% velocity and gain 75% of the other ship's
# velocity
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

I decided to add some energy loss due to collision. So lets multiplying the other's velocity by a percent.

```python
new_self_vel_x = other_vel_x * 0.80
new_self_vel_y = other_vel_y * 0.80
new_other_vel_x = self_vel_x * 0.80
new_other_vel_y = self_vel_y * 0.80
```

<div align="center">
  <img width="100%" src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/zuoz2c5gcq9jkvigkcts.gif" /> <figcaption><i><b>Ship collisions v1</b>: Gain 80% of the other ship's velocity</i></figcaption>
</div>

My physics friend corrected me and said momentum needs to be conserved. This looks more natural!

```python
new_self_vel_x = (self_vel_x * 0.2) + (other_vel_x * 0.75)
new_self_vel_y = (self_vel_y * 0.2) + (other_vel_y * 0.75)
new_other_vel_x = (other_vel_x * 0.2) + (self_vel_x * 0.75)
new_other_vel_y = (other_vel_y * 0.2) + (self_vel_y * 0.75)
```

<div align="center">
  <img width="100%" src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/yokxs0dhivrwszmzjc7s.gif" /> <figcaption><i><b>Ship collisions v2</b>: Maintain 20% of original velocity and gain 75% of the other ship's velocity</i></figcaption>
</div>

My goal isn't to make a physics accurate simulation, so this will be good enough. I may use Unreal or Unity in the future to take advantage of the available physics modules.

## Next Up

I will be drawing pixel art for the player 2 ship and preparing to train my agent using the DQN algorithm.
I will see how far I can get without using tutorials and trying to derive everything from the paper.
