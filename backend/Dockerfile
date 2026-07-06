FROM golang:1.24-alpine AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /out/api ./cmd/api
RUN CGO_ENABLED=0 go build -o /out/seed-admin ./cmd/seed-admin

FROM alpine:3.20
RUN apk add --no-cache ca-certificates
WORKDIR /app
COPY --from=build /out/api /out/seed-admin ./
COPY migrations ./migrations
RUN mkdir -p /app/uploads
EXPOSE 8080
ENTRYPOINT ["./api"]
