package domain

import "time"

type Grupo struct {
	ID               string
	Nombre           string
	ProfesorID       string
	CodigoInvitacion string
	FechaCreacion    time.Time
}
