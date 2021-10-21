.PHONY: tests

VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python

freeze:
	${PYTHON} -m pip freeze > requirements.txt

prepare:
	python3 -m pip install --upgrade pip
	python3 -m venv $(VENV_NAME)
	cp .env.dist .env.dev
	sed -i -e 's/db/db_dev/' .env.dev
	make fixtures env=dev
	cp .env.dist .env.test
	sed -i -e 's/db/db_test/' .env.test
	make fixtures env=test


install:
	pip install --no-cache-dir wheel
	${PYTHON} -m pip install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf htmlcov

fix:
	$(PYTHON) -m black --line-length 120 ./src
	$(PYTHON) -m autopep8 --recursive --in-place --aggressive --max-line-length=120 ./src/*

analyse:
	$(PYTHON) -m flake8 --max-line-length=120 ./src
	$(PYTHON) -m pylint ./src
	$(PYTHON) -m pycodestyle --max-line-length=120 ./src

tests:
	make fixtures env=test
	$(PYTHON) -m pytest --cov=./src --cov-report=html -s

fixtures:
	touch db_$(env).json && rm db_$(env).json
	cp fixtures.json db_$(env).json

run:
	$(PYTHON) main.py
