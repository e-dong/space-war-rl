#!/bin/bash

ITCH_USERNAME=e-dong
ITCH_GAME_ID=spacewar-dev

echo "BUILD_NUM=$(python setup.py --version)-dev-test" >> "$GITHUB_ENV"
echo "ITCH_USERNAME=${ITCH_USERNAME}" >> "$GITHUB_ENV"
echo "ITCH_GAME_ID=${ITCH_GAME_ID}" >> "$GITHUB_ENV"