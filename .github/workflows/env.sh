#!/bin/bash

echo "version=$(python setup.py --version)-dev-test" >> "$GITHUB_ENV"