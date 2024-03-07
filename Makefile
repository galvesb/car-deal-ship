# Monta o ambiente virtual
.PHONY: build-venv
build-venv:
	python3.9 -m venv venv

.PHONY: run-dev
run-dev:
	uvicorn --factory api_main:create_app --reload

# Instala o ambiente
.PHONY: requirements-dev
requirements-dev:
	python -m pip install --upgrade pip
	pip install wheel
	pip install -r requirements/develop.txt

.PHONY: coverage-command
coverage-command:
	@py.test --cov=app --cov-report=term-missing --cov-report=xml --cov-fail-under=90 ./tests/

.PHONY: coverage-html-command
coverage-html-command:
	@py.test --cov=app --cov-report=term-missing --cov-report=html --cov-fail-under=90 ./tests/

.PHONY: test
test: migrate
	@py.test

.PHONY: bandit
bandit:
	bandit -r -f custom app

.PHONY: flake8
flake8:
	flake8 --config ./devtools/config.ini

.PHONY: isort-check
isort-check:
	isort -c --py 38 --profile=black -l 79 .

.PHONY: isort
isort:
	isort --py 38 --profile=black -l 79 .

.PHONY: black
black:
	@venv/bin/black --config ./devtools/config.toml .

.PHONY: black-check
black-check:
	@venv/bin/black --config ./devtools/config.toml --check .

.PHONY: lint
lint: isort black flake8

.PHONY: check-lint
check-lint: isort-check black-check bandit flake8

.PHONY: migrate-command
migrate-command:
	mkdir -p migrations
	@venv/bin/mongodb-migrate --url ${APP_DB_DSN} --migrations migrations

.PHONY: safety
safety:
	cat requirements/base.txt | safety check --stdin

.PHONY: notify-slackbot
notify-slackbot:
	python slackbot.py

.PHONY: export-openapi
export-openapi:
	@venv/bin/python export_openapi.py

.PHONY: migration-generator
migration-generator:
	./devtools/scripts/migration-generator.sh $(name)

.PHONY: coverage-html
coverage-html:
	./devtools/scripts/run-coverage-html.sh

.PHONY: migrate
migrate:
	./devtools/scripts/run-migrate.sh

.PHONY: coverage
coverage:
	./devtools/scripts/run-coverage.sh
