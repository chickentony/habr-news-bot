#!make
SHELL := /bin/bash
BOT_TOKEN := ${BOT_TOKEN}
APP_DIR_NAME := "app"
LINT_LEVEL := 8
IMAGE_TAG := habr-news-bot
CONTAINER_NAME := habr-news-app

build:
	@echo "Building docker image"
	@docker build -t $(IMAGE_TAG) .

start:
	make build
	@echo "Run app container"
	@docker run -d -e BOT_TOKEN=$(BOT_TOKEN) --rm --name $(CONTAINER_NAME) $(IMAGE_TAG)

stop:
	@echo "Stop app container"
	@docker stop $(CONTAINER_NAME)

test:
	@echo "Run all tests with pytest"
	@pytest -v

lint:
	@echo "Check code quality with pylint"
	@pylint $(APP_DIR_NAME) --ignore-patterns=test_ --exit-zero --fail-under=$(LINT_LEVEL)
