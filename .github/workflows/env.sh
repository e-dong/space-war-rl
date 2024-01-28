#!/bin/bash

echo "version=$(python setup.py --version)-dev" >> "$GITHUB_OUTPUT"