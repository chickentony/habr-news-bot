#!make
SHELL:=/bin/bash

build:
	@echo "Building docker image"
	@docker build -t habr-new-bot .

test:
	@echo "Testing with pytest"
	@pytest -v

lint:
	@echo "Check code quality with pylint"
	@pylint app --ignore-patterns=test_ --exit-zero