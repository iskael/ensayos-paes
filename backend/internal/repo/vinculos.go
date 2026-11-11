package repo

import (
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgconn"
	"github.com/jackc/pgx/v5/pgxpool"
)

const vigenciaCodigoApoderado = 7 * 24 * time.Hour

type Vinculos struct {
	pool *pgxpool.Pool
}

func NewVinculos(pool *pgxpool.Pool) *Vinculos {
	return &Vinculos{pool: pool}
}

type CodigoApoderado struct {
	Codigo   string    `json:"codigo"`
	ExpiraEn time.Time `json:"expira_en"`
}

type PersonaVinculada struct {
	ID           string    `json:"id"`
	Nombre       string    `json:"nombre"`
	Email        string    `json:"email,omitempty"`
	FechaVinculo time.Time `json:"fecha_vinculo"`
}

// CodigoVigente devuelve el código del estudiante si sigue vigente; si no existe o venció, genera uno nuevo.
func (r *Vinculos) CodigoVigente(ctx context.Context, estudianteID string) (CodigoApoderado, error) {
	var c CodigoApoderado
	err := r.pool.QueryRow(ctx, `SELECT codigo, expira_en FROM codigos_apoderado WHERE estudiante_id = $1 AND expira_en > now()`, estudianteID).
		Scan(&c.Codigo, &c.ExpiraEn)
	if err == nil {
		return c, nil
	}
	if !errors.Is(err, pgx.ErrNoRows) {
		return CodigoApoderado{}, fmt.Errorf("leer código de apoderado: %w", err)
	}
	return r.NuevoCodigo(ctx, estudianteID)
}

func (r *Vinculos) NuevoCodigo(ctx context.Context, estudianteID string) (CodigoApoderado, error) {
	for intento := 0; intento < 5; intento++ {
		codigo, err := generarCodigo(8)
		if err != nil {
			return CodigoApoderado{}, err
		}
		c := CodigoApoderado{Codigo: codigo, ExpiraEn: time.Now().Add(vigenciaCodigoApoderado).UTC().Truncate(time.Second)}
		_, err = r.pool.Exec(ctx, `INSERT INTO codigos_apoderado (estudiante_id, codigo, expira_en) VALUES ($1,$2,$3)
		                          ON CONFLICT (estudiante_id) DO UPDATE SET codigo = EXCLUDED.codigo, expira_en = EXCLUDED.expira_en`,
			estudianteID, c.Codigo, c.ExpiraEn)
		if err == nil {
			return c, nil
		}
		var pgErr *pgconn.PgError
		if errors.As(err, &pgErr) && pgErr.Code == "23505" {
			continue
		}
		return CodigoApoderado{}, fmt.Errorf("guardar código de apoderado: %w", err)
	}
	return CodigoApoderado{}, errors.New("no se pudo generar un código único")
}

// Vincular une al apoderado con el estudiante dueño del código vigente. Es idempotente.
func (r *Vinculos) Vincular(ctx context.Context, apoderadoID, codigo string) (PersonaVinculada, error) {
	var p PersonaVinculada
	err := r.pool.QueryRow(ctx, `SELECT u.id::text, u.nombre FROM codigos_apoderado c JOIN usuarios u ON u.id = c.estudiante_id
	                             WHERE c.codigo = $1 AND c.expira_en > now()`, codigo).Scan(&p.ID, &p.Nombre)
	if errors.Is(err, pgx.ErrNoRows) {
		return PersonaVinculada{}, ErrNoEncontrado
	}
	if err != nil {
		return PersonaVinculada{}, fmt.Errorf("buscar código: %w", err)
	}
	err = r.pool.QueryRow(ctx, `INSERT INTO apoderado_estudiantes (apoderado_id, estudiante_id) VALUES ($1,$2)
	                            ON CONFLICT (apoderado_id, estudiante_id) DO UPDATE SET fecha_vinculo = apoderado_estudiantes.fecha_vinculo
	                            RETURNING fecha_vinculo`, apoderadoID, p.ID).Scan(&p.FechaVinculo)
	if err != nil {
		return PersonaVinculada{}, fmt.Errorf("vincular apoderado: %w", err)
	}
	return p, nil
}

func (r *Vinculos) Pupilos(ctx context.Context, apoderadoID string) ([]PersonaVinculada, error) {
	return r.listar(ctx, `SELECT u.id::text, u.nombre, '', v.fecha_vinculo FROM apoderado_estudiantes v JOIN usuarios u ON u.id = v.estudiante_id
	                      WHERE v.apoderado_id = $1 ORDER BY u.nombre`, apoderadoID)
}

func (r *Vinculos) Apoderados(ctx context.Context, estudianteID string) ([]PersonaVinculada, error) {
	return r.listar(ctx, `SELECT u.id::text, u.nombre, u.email, v.fecha_vinculo FROM apoderado_estudiantes v JOIN usuarios u ON u.id = v.apoderado_id
	                      WHERE v.estudiante_id = $1 ORDER BY v.fecha_vinculo`, estudianteID)
}

func (r *Vinculos) listar(ctx context.Context, q, id string) ([]PersonaVinculada, error) {
	rows, err := r.pool.Query(ctx, q, id)
	if err != nil {
		return nil, fmt.Errorf("listar vínculos: %w", err)
	}
	defer rows.Close()
	out := []PersonaVinculada{}
	for rows.Next() {
		var p PersonaVinculada
		if err := rows.Scan(&p.ID, &p.Nombre, &p.Email, &p.FechaVinculo); err != nil {
			return nil, fmt.Errorf("leer vínculo: %w", err)
		}
		out = append(out, p)
	}
	return out, rows.Err()
}

func (r *Vinculos) EsApoderadoDe(ctx context.Context, apoderadoID, estudianteID string) (bool, error) {
	var ok bool
	err := r.pool.QueryRow(ctx, `SELECT EXISTS (SELECT 1 FROM apoderado_estudiantes WHERE apoderado_id = $1 AND estudiante_id = $2)`,
		apoderadoID, estudianteID).Scan(&ok)
	return ok, err
}

func (r *Vinculos) Desvincular(ctx context.Context, apoderadoID, estudianteID string) error {
	ct, err := r.pool.Exec(ctx, `DELETE FROM apoderado_estudiantes WHERE apoderado_id = $1 AND estudiante_id = $2`, apoderadoID, estudianteID)
	if err != nil {
		return fmt.Errorf("desvincular: %w", err)
	}
	if ct.RowsAffected() == 0 {
		return ErrNoEncontrado
	}
	return nil
}
