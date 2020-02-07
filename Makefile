.PHONY: up down restart prod dev build lint watch containers-build build-dev build-frontend lint-frontend lint-backend build-dev-frontend refresh-backend

init:
	bash .scripts/init

up:
	docker/compose up -d

down:
	docker/compose down

restart: down up

prod: containers-build install build up

dev: up watch down

build: build-frontend

lint: lint-backend lint-frontend

watch:
	# The `exit 0` is here because
	# yarn watch returns a non-zero
	# code when it's sent a SIGINT
	docker/yarn watch || exit 0

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
