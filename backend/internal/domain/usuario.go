package domain

import "time"

type Rol string

const (
	RolEstudiante  Rol = "estudiante"
	RolProfesor    Rol = "profesor"
	RolAdmin       Rol = "admin"
	RolApoderado   Rol = "apoderado"
	RolInstitucion Rol = "institucion"
	RolEditor      Rol = "editor"
)

func (r Rol) Valido() bool {
	switch r {
	case RolEstudiante, RolProfesor, RolAdmin, RolApoderado, RolInstitucion, RolEditor:
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

// RegistrablePorSiMismo: roles que cualquiera puede elegir al registrarse. Admin y editor los asigna un admin.
func (r Rol) RegistrablePorSiMismo() bool {
	switch r {
	case RolEstudiante, RolProfesor, RolApoderado, RolInstitucion:
		return true
	}
	return false
}

// AsignablePorAdmin: un admin puede mover una cuenta a cualquier rol menos admin (los admin se crean con seed-admin).
func (r Rol) AsignablePorAdmin() bool {
	return r.Valido() && r != RolAdmin
}
