
.PHONY: game dev prod

# User CLI Targets
# Default target
game:
	venv/bin/python -m main

########################################################
# Dependencies
########################################################

dev: venv/dev_installed
prod: venv/wheel_installed

web-dev:
	venv/bin/pip install -e .[web]
	venv/bin/pygbag --width 800 --height 600 --ume_block=0 .

web-pack:
	venv/bin/pip install .[web]
	venv/bin/pygbag --width 800 --height 600 --ume_block=0 --archive .

# venv setup and requirements.txt installed
venv/venv_created: requirements.txt
	test -d venv || python -m venv venv
	touch venv/venv_created

# Install requirements.txt to venv
venv/dev_installed: venv/venv_created requirements-dev.txt setup.py
	venv/bin/pip install -e .[dev]
	touch venv/dev_installed

# Install the wheel in "production"
venv/wheel_installed: venv/venv_created setup.py space_war/**.py space_war/sim/assets/**
	venv/bin/pip install .[build]
	touch venv/wheel_installed
	
clean:
	git clean -fdx

########################################################
# Development
########################################################
format: dev
	venv/bin/black --line-length 80 space_war/**.py

lint: dev
	venv/bin/pylint space_war/**.py
	venv/bin/flake8 space_war/**.py
	venv/bin/isort space_war/**.py
