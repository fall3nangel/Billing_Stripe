#!make
include .env
export

install_requirements:
	pip3 install -r requirements.txt

run_postgres:
	docker compose \
		-f docker-compose.yml \
		-f docker-compose.override.yml \
		up -d postgres pgadmin

drop_postgres:
	docker stop postgres_container && docker rm --force postgres_container
	docker volume rm graduate_project_postgres

run_admin_panel_local:
	cd admin_panel && python3 manage.py migrate
	cd admin_panel && python3 manage.py createsuperuser --noinput || true
	cd admin_panel && python3 manage.py makemessages -l en -l ru
	cd admin_panel && python3 manage.py runserver

run_admin_panel_service:
	cd admin_panel && python3 manage.py collectstatic --noinput
	docker compose \
 		-f docker-compose.yml \
		-f docker-compose.override.yml \
 		up --build admin

run_billing_service:
	cd admin_panel && python3 manage.py collectstatic --noinput
	docker compose \
 		-f docker-compose.yml \
		-f docker-compose.override.yml \
 		up --build billing

make down:
	docker compose \
	-f docker-compose.yml \
	-f docker-compose.override.yml \
	down --remove-orphans