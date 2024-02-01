# Space War RL

I will be remaking the 1985 version of Space War using Pygame and train deep reinforcement learning agents to battle it out. I will try to do everything from scratch as much as possible as a learning exercise!

<iframe frameborder="0" src="https://itch.io/embed/2449473" width="552" height="167"><a href="https://e-dong.itch.io/spacewar">SpaceWarRL (stable) by e-dong</a></iframe>

## Quickstart Demo

Run `make prod game` to startup the game in "production" mode.

If switching between dev/game, use the `clean` target to be safe.  
e.g. `make clean dev game` if switching from prod to dev.

## Development

_Note: I only tested this in x86_64 linux, so there might be linux specific dependencies in the requirements_

### First time setup

1. Install `python` on your system. At the time of writing this, python version `3.11.5` was used.
1. Setup virtual env and dependencies with `make dev`

### Starting the game

Start the game with `make`, _`game` is the default target, so you dont need to specify `make game` every time_

You can also run `make dev game` everytime, the requirements will installed when there is a change either requirement files.
