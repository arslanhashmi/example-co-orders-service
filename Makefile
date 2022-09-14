test-style:
	py.test

up-db:
	@docker-compose up -d

setup:
	@virtualenv venv --python py3.9
	@. venv/bin/activate; pip install --disable-pip-version-check --exists-action w -r requirements/base.txt -r requirements/dev.txt

upgrade-db:
	@. venv/bin/activate; alembic --config src/exampleco/migrations/database/alembic.ini upgrade heads

migration:
	@. venv/bin/activate; alembic --config src/exampleco/migrations/database/alembic.ini revision -m "${}" --autogenerate

downgrade-db:
	@. venv/bin/activate; alembic --config src/exampleco/migrations/database/alembic.ini downgrade ${}

serverless-offline:
	serverless offline \
			--host 0.0.0.0 \
			--httpPort 8080 \
			--lambdaPort 3000 \
			--region us-east-1 \

up: up-db setup upgrade-db serverless-offline

test: setup
	@. venv/bin/activate; pytest src/exampleco/tests --verbose;

ui:
	npm ci --prefix frontend/ && npm start --prefix frontend/
