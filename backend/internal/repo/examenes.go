package repo

import (
	"context"
	"errors"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/usuario/ensayos-paes/internal/domain"
)

type Examenes struct {
	pool *pgxpool.Pool
}

func NewExamenes(pool *pgxpool.Pool) *Examenes {
	return &Examenes{pool: pool}
}

func (r *Examenes) Crear(ctx context.Context, e domain.ExamenFuente) (domain.ExamenFuente, error) {
	const q = `INSERT INTO examenes_fuente (nombre, anio_admision, tipo, nivel, edicion, url_pdf, fecha_publicacion)
	           VALUES ($1,$2,$3,$4,$5,$6,$7) RETURNING id::text`
	err := r.pool.QueryRow(ctx, q, e.Nombre, e.AnioAdmision, string(e.Tipo), string(e.Nivel), e.Edicion, e.URLPdf, e.FechaPublicacion).Scan(&e.ID)
	return e, err
}

func (r *Examenes) PorID(ctx context.Context, id string) (domain.ExamenFuente, error) {
	var e domain.ExamenFuente
	var tipo, nivel string
	const q = `SELECT id::text, nombre, anio_admision, tipo::text, nivel::text, edicion, url_pdf, fecha_publicacion
	           FROM examenes_fuente WHERE id = $1`
	err := r.pool.QueryRow(ctx, q, id).Scan(&e.ID, &e.Nombre, &e.AnioAdmision, &tipo, &nivel, &e.Edicion, &e.URLPdf, &e.FechaPublicacion)
	if errors.Is(err, pgx.ErrNoRows) {
		return domain.ExamenFuente{}, ErrNoEncontrado
	}
	if err != nil {
		return domain.ExamenFuente{}, err
	}
	e.Tipo = domain.TipoExamen(tipo)
	e.Nivel = domain.Nivel(nivel)
	return e, nil
}

func (r *Examenes) Listar(ctx context.Context, limit, offset int) ([]domain.ExamenFuente, error) {
	const q = `SELECT id::text, nombre, anio_admision, tipo::text, nivel::text, edicion, url_pdf, fecha_publicacion
	           FROM examenes_fuente ORDER BY anio_admision DESC, nombre LIMIT $1 OFFSET $2`
	rows, err := r.pool.Query(ctx, q, limit, offset)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	out := []domain.ExamenFuente{}
	for rows.Next() {
		var e domain.ExamenFuente
		var tipo, nivel string
		if err := rows.Scan(&e.ID, &e.Nombre, &e.AnioAdmision, &tipo, &nivel, &e.Edicion, &e.URLPdf, &e.FechaPublicacion); err != nil {
			return nil, err
		}
		e.Tipo = domain.TipoExamen(tipo)
		e.Nivel = domain.Nivel(nivel)
		out = append(out, e)
	}
	return out, rows.Err()
}

func (r *Examenes) Actualizar(ctx context.Context, id string, e domain.ExamenFuente) (domain.ExamenFuente, error) {
	const q = `UPDATE examenes_fuente
	           SET nombre=$1, anio_admision=$2, tipo=$3, nivel=$4, edicion=$5, url_pdf=$6, fecha_publicacion=$7
	           WHERE id=$8`
	ct, err := r.pool.Exec(ctx, q, e.Nombre, e.AnioAdmision, string(e.Tipo), string(e.Nivel), e.Edicion, e.URLPdf, e.FechaPublicacion, id)
	if err != nil {
		return domain.ExamenFuente{}, err
	}
	if ct.RowsAffected() == 0 {
		return domain.ExamenFuente{}, ErrNoEncontrado
	}
	return r.PorID(ctx, id)
}

func (r *Examenes) Eliminar(ctx context.Context, id string) error {
	ct, err := r.pool.Exec(ctx, `DELETE FROM examenes_fuente WHERE id = $1`, id)
	if err != nil {
		return err
	}
	if ct.RowsAffected() == 0 {
		return ErrNoEncontrado
	}
	return nil
}
