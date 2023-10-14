
.PHONY: game game-prod

# User CLI Targets
# Default target
game:
	venv/bin/python -m game.main

dev: venv/dev_installed
prod: venv/wheel_installed

# venv setup and requirements.txt installed
venv/requirements_installed: requirements.txt
	test -d venv || python -m venv venv
	. venv/bin/activate; pip install -r requirements.txt
	touch venv/requirements_installed

# Install requirements.txt to venv
venv/dev_installed: venv/requirements_installed requirements-dev.txt setup.py
	venv/bin/pip install -r requirements-dev.txt
	venv/bin/pip install -e .
	touch venv/dev_installed

# Install the wheel in "production"
venv/wheel_installed: venv/requirements_installed setup.py game/**.py game/assets/**
	venv/bin/pip install .
	touch venv/wheel_installed
	
clean:
	rm -rf __pycache__
	rm -rf venv
