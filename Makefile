SHELL := /bin/bash

runserver:
	docker exec -it backend python ./src/manage.py runserver 0:9000

makemigrations:
	docker exec -it backend python ./src/manage.py makemigrations

migrate:
	docker exec -it backend python ./src/manage.py migrate

mm: makemigrations migrate

collectstatic:
	docker exec -it backend python ./src/manage.py collectstatic --noinput && \
	sudo docker cp backend:/tmp/static_content/static /tmp/static && \
	sudo docker cp /tmp/static nginx:/etc/nginx/static

start:
	docker-compose down && \
	cp -n .env .env && docker-compose up --build

build: start migrate collectstatic

shell: 
	docker exec -it backend python3 ./src/manage.py shell_plus --print-sql

wtf:
	docker logs --tail all backend

urls:
	docker exec -it backend python3 src/manage.py show_urls

test:
	docker exec -it backend pytest ./src/tests

freeze:
	docker exec -it backend pip freeze > requirements.txt

flake8:
	docker exec -it backend flake8 src
