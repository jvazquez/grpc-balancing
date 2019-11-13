BUILD_ARG = $(if $(filter  $(NOCACHE), 1),--no-cache)
DOCKER = $(if $(DOCKER_BINARY),$(DOCKER_BINARY),/usr/bin/docker)

local_all: grpc_server grpc_client

local_up:
	docker-compose up -d
local_down:
	docker-compose stop
	docker-compose down --volumes
grpc_server:
	$(DOCKER) build $(BUILD_ARG) -f images/server/Dockerfile -t grpc-server .
grpc_client:
	$(DOCKER) build $(BUILD_ARG) -f images/client/Dockerfile -t grpc-client .
