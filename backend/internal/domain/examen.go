package domain

import "time"

type ExamenFuente struct {
	ID               string     `json:"id"`
	Nombre           string     `json:"nombre"`
	AnioAdmision     int        `json:"anio_admision"`
	Tipo             TipoExamen `json:"tipo"`
	Nivel            Nivel      `json:"nivel"`
	Edicion          *string    `json:"edicion,omitempty"`
	URLPdf           *string    `json:"url_pdf,omitempty"`
	FechaPublicacion *time.Time `json:"fecha_publicacion,omitempty"`
}
