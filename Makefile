all: build run

build:
	docker build -t current-album-art .

run:
	docker run --rm -it -p 8080:8080 --env-file .env --name current-album-art current-album-art:latest
