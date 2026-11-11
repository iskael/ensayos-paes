package domain

import "testing"

func TestRolesRegistrablesYAsignables(t *testing.T) {
	casos := []struct {
		rol         Rol
		registrable bool
		asignable   bool
	}{
		{RolEstudiante, true, true},
		{RolProfesor, true, true},
		{RolApoderado, true, true},
		{RolInstitucion, true, true},
		{RolEditor, false, true},
		{RolAdmin, false, false},
		{Rol("superusuario"), false, false},
	}
	for _, c := range casos {
		if got := c.rol.RegistrablePorSiMismo(); got != c.registrable {
			t.Errorf("%s registrable = %v, se esperaba %v", c.rol, got, c.registrable)
		}
		if got := c.rol.AsignablePorAdmin(); got != c.asignable {
			t.Errorf("%s asignable = %v, se esperaba %v", c.rol, got, c.asignable)
		}
	}
}
