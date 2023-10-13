.PHONY: game

venv/bin/activate: requirements.txt
	python -m venv venv
	venv/bin/pip install -r requirements.txt

dev: venv/bin/activate requirements-dev.txt
	venv/bin/pip install -r requirements-dev.txt

game: venv/bin/activate
	venv/bin/python -m game

clean:
	rm -rf __pycache__
	rm -rf venv
