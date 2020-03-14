PORT=9090

start:
	@python app.py

debug:
	@export FLASK_APP=app.py; export FLASK_ENV=development; flask run --port $(PORT)

venv:
	@python -m venv venv

freeze:
	@pip freeze > requirements.txt

install:
	@pip install -r requirements.txt

create:
	@docker-compose up -d

shell:
	@ipython

dbshell:
	@docker exec -it postgresdb /bin/bash

db:
	@docker exec -it postgresdb psql -U sambrannan -d historic

dblogs:
	@docker-compose logs -f

clean:
	@docker-compose stop
	@docker-compose rm -vf
	@docker volume prune -f
