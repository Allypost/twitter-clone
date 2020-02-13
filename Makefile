.PHONY: up down restart prod dev build lint watch containers-build build-dev build-frontend lint-frontend lint-backend build-dev-frontend refresh-backend

init: _run-init-script containers-build install build up

up:
	docker/compose up -d

up-db:
	docker/compose up -d twitter-db

down:
	docker/compose down

restart: down up

prod: containers-build install build up

dev: migrate up watch down

build: build-frontend

lint: lint-backend lint-frontend

watch:
	# The `exit 0` is here because
	# yarn watch returns a non-zero
	# code when it's sent a SIGINT
	docker/yarn watch || exit 0

shell: up
	docker-compose exec backend flask shell

migration: up-db
	docker/python app/manage.py db migrate
	# This is required because the generated migration file
	# is owned by root (or the user running Docker)
	docker/backend chown $(shell id -u):$(shell id -g) migrations/versions/*

migrate: up-db
	docker/python app/manage.py db upgrade

migrate-down: up-db
	docker/python app/manage.py db downgrade

containers-build:
	docker/compose build

install:
	docker/yarn install

build-dev: build-dev-frontend

build-frontend:
	docker/yarn build

lint-frontend:
	docker/yarn lint

lint-backend:
	docker run --rm -v "$(shell pwd):/code" jbbarth/black main.py app migrations

build-dev-frontend:
	docker/yarn build --env=development

refresh-backend:
	touch frontend/dist/index.html

_run-init-script:
	bash .scripts/init
