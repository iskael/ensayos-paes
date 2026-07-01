package config

import (
	"os"
	"strconv"
	"time"
)

type Config struct {
	Port          string
	DatabaseURL   string
	JWTSecret     string
	JWTTTL        time.Duration
	UploadsDir    string
	UploadsURL    string
	AllowedOrigin string
}

func Load() Config {
	return Config{
		Port:          getenv("PORT", "8080"),
		DatabaseURL:   getenv("DATABASE_URL", "postgres://localhost:5432/ensayos_paes?sslmode=disable"),
		JWTSecret:     getenv("JWT_SECRET", "cambiar-en-produccion"),
		JWTTTL:        time.Duration(getenvInt("JWT_TTL_HORAS", 24)) * time.Hour,
		UploadsDir:    getenv("UPLOADS_DIR", "./uploads"),
		UploadsURL:    getenv("UPLOADS_URL", "http://localhost:8080/uploads"),
		AllowedOrigin: getenv("CORS_ALLOWED_ORIGIN", "*"),
	}
}

func getenv(k, def string) string {
	if v := os.Getenv(k); v != "" {
		return v
	}
	return def
}

func getenvInt(k string, def int) int {
	if v := os.Getenv(k); v != "" {
		if n, err := strconv.Atoi(v); err == nil {
			return n
		}
	}
	return def
}
