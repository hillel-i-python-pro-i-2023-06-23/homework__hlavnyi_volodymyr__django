#!/usr/bin/env sh

make init-configs &&\
export UID &&\
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 \
		docker compose run --rm app python manage.py delete_contacts --all
