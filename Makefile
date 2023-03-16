make:#!make
include .env
export

install_requirements:
	pip3 install -r requirements.txt

run_postgres:
	docker compose \
		-f docker-compose.yml \
		-f docker-compose_pg_develop.yml \
		-f docker-compose.override.yml \
		up -d postgres pgadmin

drop_postgres:
	docker stop postgres_container && docker rm --force postgres_container
	docker volume rm graduate_project_postgres

drop_postgres_test:
	docker compose \
 		-f docker-compose.yml \
		-f docker-compose_pg_tests.yml \
		-f docker-compose.override.yml \
 		rm --force


run_admin_panel_local:
	cd admin_panel && python3 manage.py migrate
	cd admin_panel && python3 manage.py createsuperuser --noinput || true
	cd admin_panel && python3 manage.py makemessages -l en -l ru
	cd admin_panel && python3 manage.py runserver

run_admin_panel_service:
	cd admin_panel && python3 manage.py collectstatic --noinput
	docker compose \
 		-f docker-compose.yml \
		-f docker-compose_pg_develop.yml \
		-f docker-compose.override.yml \
 		up --build admin

run_billing_service:
	cd admin_panel && python3 manage.py collectstatic --noinput
	docker compose \
 		-f docker-compose.yml \
		-f docker-compose_pg_develop.yml \
		-f docker-compose.override.yml \
 		up --build billing

run_etl_service:
	docker compose \
 		-f docker-compose.yml \
		-f docker-compose_pg_develop.yml \
		-f docker-compose.override.yml \
 		up --build etl

run_pay-api_service:
	docker compose \
		-f docker-compose.yml \
		-f docker-compose_pg_develop.yml \
		-f docker-compose.override.yml \
		 up --build pay-api

down:
	docker compose \
	-f docker-compose.yml \
	-f docker-compose_pg_develop.yml \
	-f docker-compose.override.yml \
	down --remove-orphans

run_usersapi_local:
	cd users_api && python3 main.py

run_rabbit:
	docker compose \
		-f docker-compose.yml \
		-f docker-compose.override.yml \
		 up -d rabbitmq

run_redis:
	docker compose \
		-f docker-compose.yml \
		-f docker-compose.override.yml \
		 up -d redis


run_billingapi_local:
	cd billing_api && python3 main.py

run_test_environment:
	docker compose \
 		-f docker-compose.yml \
		-f docker-compose_pg_tests.yml \
		-f docker-compose.override.yml \
 		up -d --build billing pay-api

stop_test_service:
	docker compose \
 		-f docker-compose.yml \
		-f docker-compose_pg_tests.yml \
		-f docker-compose.override.yml \
 		stop billing postgres pay-api

run_test_local: stop_test_service drop_postgres_test run_test_environment
	cd integration_test && pytest -s

run_test_service: stop_test_service drop_postgres_test
		docker compose \
 		-f docker-compose.yml \
		-f docker-compose_pg_tests.yml \
		-f docker-compose.override.yml \
 		up --build integration_test
