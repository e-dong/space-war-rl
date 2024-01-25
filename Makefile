
.PHONY: game dev prod

# User CLI Targets
# Default target
game:
	venv/bin/python -m space_war.main

########################################################
# Dependencies
########################################################

dev: venv/dev_installed
prod: venv/wheel_installed

web-dev: pre-web
	venv/bin/pygbag --width 800 --height 600 --ume_block=0 tmp

web-pack: pre-web
	venv/bin/pygbag \
	  --width 800 \
	  --height 600 \
	  --ume_block=0 \
	  --archive \
	  tmp
	cp tmp/space_war/sim/assets/player_0.png tmp/build/web/favicon.png


pre-web: dev
	rm -rf tmp
	mkdir tmp
	cp -r space_war tmp
	mv tmp/space_war/main.py tmp

# venv setup and requirements.txt installed
venv/venv_created: requirements.txt
	test -d venv || python -m venv venv
	touch venv/venv_created

# Install requirements.txt to venv
venv/dev_installed: venv/venv_created requirements-dev.txt setup.py
	venv/bin/pip install -e .[dev]
	touch venv/dev_installed

# Install the wheel in "production"
venv/wheel_installed: venv/venv_created setup.py space_war/**/*.py space_war/sim/assets/**
	venv/bin/pip install .[build]
	touch venv/wheel_installed
	
clean:
	rm -rf ./**/*/__pycache__
	rm -rf ./build
	rm -rf ./tmp
	rm -rf ./venv
	rm -rf *.egg-info

########################################################
# Development
########################################################
format: dev
	venv/bin/black --line-length 80 space_war

lint: dev
	venv/bin/pylint --extension-pkg-whitelist=pygame space_war
	venv/bin/flake8 space_war
	venv/bin/isort space_war
