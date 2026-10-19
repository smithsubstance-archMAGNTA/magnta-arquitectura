# Makefile for common tasks

.PHONY: build up down logs shell ps restart

IMAGE_NAME = magnta:dev
COMPOSE = docker compose

build:
	$(COMPOSE) build --no-cache

up:
	$(COMPOSE) up --build -d

down:
	$(COMPOSE) down -v

logs:
	$(COMPOSE) logs -f

ps:
	$(COMPOSE) ps

shell:
	$(COMPOSE) exec web /bin/bash

restart:
	$(COMPOSE) restart
