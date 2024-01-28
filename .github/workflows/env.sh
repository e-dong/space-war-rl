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
  echo $GITHUB_SHA
  echo $GITHUB_REF
  echo $GITHUB_REF_NAME
  git_hash=$(git rev-parse --short "$GITHUB_SHA")
  git_branch=${GITHUB_REF#refs/heads/}

  ITCH_GAME_ID="${ITCH_GAME_ID}-dev"
  BUILD_NUM="${BUILD_NUM}-${git_branch}-${git_hash}"
fi

echo "build_num: ${BUILD_NUM}"

echo "BUILD_NUM=${BUILD_NUM}" >> "$GITHUB_ENV"
echo "ITCH_USERNAME=${ITCH_USERNAME}" >> "$GITHUB_ENV"
echo "ITCH_GAME_ID=${ITCH_GAME_ID}" >> "$GITHUB_ENV"

env
