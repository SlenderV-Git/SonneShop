BACKEND_SERVICE = backend-service
DB_SERVICE = db-service
REDIS_SERVICE = redis

DC = docker compose
ENV_PATH = ./backend.env


build-backend:
	$(DC) --env-file $(ENV_PATH) build $(BACKEND_SERVICE)

up-all:
	docker compose --env-file $(ENV_PATH) up -d

up-all-echo:
	docker compose --env-file $(ENV_PATH) up

up-backend:
	docker compose --env-file $(ENV_PATH) up $(BACKEND_SERVICE) $(DB_SERVICE) $(REDIS_SERVICE)

up-db:
	docker compose --env-file $(ENV_PATH) up $(DB_SERVICE)

up-redis:
	docker compose --env-file $(ENV_PATH) up $(REDIS_SERVICE)

stop-all:
	docker stop $(BACKEND_SERVICE) $(DB_SERVICE) $(REDIS_SERVICE)

stop-db:
	docker stop $(DB_SERVICE)

stop-redis:
	docker stop $(REDIS_SERVICE)

redis-monitor:
	docker exec -it $(REDIS_SERVICE) redis-cli monitor

redis-cli:
	docker exec -it $(REDIS_SERVICE) redis-cli

create-certs-windows:
	powershell ./scripts/certs.ps1

create-certs-unix:
	bash ./scripts/certs.sh