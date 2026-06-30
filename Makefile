.PHONY: run test tidy proto

run:
	cd backend && go run ./cmd/api

test:
	cd backend && go test ./...

tidy:
	cd backend && go mod tidy

proto:
	cd prototipo-ia && python3 genera_preguntas.py
