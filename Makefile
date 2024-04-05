all: clean build run

build:
	docker build -t current-album-art .

run:
	docker run -it -d -p 8080:8080 --env-file .env --name current-album-art current-album-art:latest

clean:
	docker stop current-album-art || true && docker rm current-album-art || true
