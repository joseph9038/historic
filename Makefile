PORT=9090

debug:
	@export FLASK_APP=app.py; export FLASK_ENV=development; flask run --port $(PORT)

venv:
	@python -m venv venv

freeze:
	@pip freeze > requirements.txt

install:
	@pip install -r requirements.txt

build:
	@docker-compose up --build -d

start:
	@docker-compose up -d

restart:
	@docker-compose restart

stop:
	@docker-compose stop

shell:
	@ipython

dbshell:
	@docker exec -it postgresdb /bin/bash

db:
	@docker exec -it postgresdb psql -U sambrannan -d historic

logs:
	@docker-compose logs -f

clean:
	@docker-compose stop
	@docker-compose rm -vf
	@docker volume prune -f
