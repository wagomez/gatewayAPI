# Filenames
GW_COMPOSE_FILE := docker/stage/docker-compose.yml

# Check and Inspect Logic
INSPECT := $$(docker-compose -p $$1 -f $$2 ps -q $$3 | xargs -I ARGS docker inspect -f "{{ .State.ExitCode }}" ARGS)

CHECK := @bash -c '\
  if [[ $(INSPECT) -ne 0 ]]; \
  then exit $(INSPECT); fi' VALUE


.PHONY: build

build:
	${INFO} "Creating build"
	@ docker-compose -f $(GW_COMPOSE_FILE) build