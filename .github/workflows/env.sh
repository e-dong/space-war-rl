#!/bin/bash

event_name="${1}"

if [[ -z "${event_name}" ]]; then
  echo "[ERROR]: event name param cannot be blank"
  exit 1
fi

echo "Setting up env vars for [${event_name}]"

ITCH_USERNAME=e-dong
ITCH_GAME_ID=spacewar
BUILD_NUM=$(python setup.py --version)

if [[ "${event_name}" == "pull_request" ]]; then
  short_commit_sha=$(git rev-parse --short HEAD)
  branch=$(git rev-parse --abbrev-ref HEAD)

  ITCH_GAME_ID="${ITCH_GAME_ID}-dev"
  BUILD_NUM="${BUILD_NUM}-${branch}-${short_commit_sha}"
fi

echo "build_num: ${BUILD_NUM}"

echo "BUILD_NUM=${BUILD_NUM}" >> "$GITHUB_ENV"
echo "ITCH_USERNAME=${ITCH_USERNAME}" >> "$GITHUB_ENV"
echo "ITCH_GAME_ID=${ITCH_GAME_ID}" >> "$GITHUB_ENV"