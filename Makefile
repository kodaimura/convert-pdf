up:
	docker compose up -d

down:
	docker compose down

start:
	docker compose start

stop:
	docker compose stop

in:
	docker exec -i -t convert-pdf bash

build:
	docker compose build --no-cache

# Docker Container
run:
	python3 main.py
