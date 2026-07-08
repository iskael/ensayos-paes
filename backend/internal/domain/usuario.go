package domain

import "time"

type Rol string

const (
	RolEstudiante Rol = "estudiante"
	RolProfesor   Rol = "profesor"
	RolAdmin      Rol = "admin"
)

func (r Rol) Valido() bool {
	switch r {
	case RolEstudiante, RolProfesor, RolAdmin:
		return true
	}
	return false
}

type Usuario struct {
	ID              string    `json:"id"`
	Nombre          string    `json:"nombre"`
	Email           string    `json:"email"`
	Rol             Rol       `json:"rol"`
	EmailVerificado bool      `json:"email_verificado"`
	FechaCreacion   time.Time `json:"fecha_creacion"`
}
