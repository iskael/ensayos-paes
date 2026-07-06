.PHONY: run test tidy proto db-up db-down stack-up stack-down

run:
	cd backend && go run ./cmd/api

test:
	cd backend && go test ./...

# Solo Postgres, para desarrollo local (backend/frontend corren fuera de Docker)
db-up:
	docker compose up -d db

db-down:
	docker compose stop db

# Stack completo (db + migraciones + api + web), para despliegue
stack-up:
	docker compose up -d --build

stack-down:
	docker compose down

tidy:
	cd backend && go mod tidy

proto:
	cd prototipo-ia && python3 genera_preguntas.py
