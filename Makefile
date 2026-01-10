MANAGEPY = src/app/manage.py
RUN = uv run
DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker-compose/app.yaml
APP_CONTAINER = stripe-test-app

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} ${ENV} down

.PHONY: superuser
superuser:
	${EXEC} ${APP_CONTAINER} ${RUN} ${MANAGEPY} createsuperuser

.PHONY: migrations
migrations:
	${EXEC} ${APP_CONTAINER} ${RUN} ${MANAGEPY} makemigrations

.PHONY: migrate
migrate: 
	${EXEC} ${APP_CONTAINER} ${RUN} ${MANAGEPY} migrate

.PHONY: isort
isort:
	uv run isort ./src/ - --profile black