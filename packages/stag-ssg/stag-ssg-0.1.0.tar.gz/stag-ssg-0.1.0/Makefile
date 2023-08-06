all: format test

init:
	pipenv install --dev --ignore-pipfile --skip-lock

format:
	pipenv run black .

test:
	pipenv run pytest

coverage:
	pipenv run py.test --cov=stag --cov-report xml --cov-report term --cov-report html

.PHONY: all format
