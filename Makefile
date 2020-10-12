export

SHELL = /usr/bin/env bash

DEPLOY_ENV ?= local

local_DOCKER_HOST ?= unix:///var/run/docker.sock
farm_DOCKER_HOST ?= ssh://raspberrypi.farm
DOCKER_HOST ?= $($(DEPLOY_ENV)_DOCKER_HOST)

build:
	docker build -t clintmod/ubiquiti-monitor:latest .


check-env:
	@if [[ -z "$${SSHPASS}" ]]; then \
		echo "Expected env var SSHPASS to be set"; \
		exit 1; \
	fi;


run: check-env
	docker run --rm -it -e SSHPASS=$$SSHPASS clintmod/ubiquiti-monitor:latest


test:
	docker run --rm -it -v $$PWD:/app clintmod/ubiquiti-monitor:latest \
	pytest \
	--cov=ubiquiti_monitor \
	--cov-branch \
	--cov-report term-missing:skip-covered \
	.

push:
	docker push clintmod/ubiquiti-monitor:latest


deploy:
	docker stack deploy --resolve-image=never \
		-c stacks/$$DEPLOY_ENV/docker-compose.yml \
		ubiquiti-monitor


undeploy:
	docker stack rm ubiquiti-monitor
