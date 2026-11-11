package repo

import (
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/usuario/ensayos-paes/internal/domain"
)

var ErrEstimuloEnUso = errors.New("el texto tiene preguntas asociadas")

type Estimulos struct {
	pool *pgxpool.Pool
}

func NewEstimulos(pool *pgxpool.Pool) *Estimulos {
	return &Estimulos{pool: pool}
}

type EstimuloBanco struct {
	ID                 string        `json:"id"`
	Clave              *string       `json:"clave,omitempty"`
	Nivel              *domain.Nivel `json:"nivel,omitempty"`
	Titulo             *string       `json:"titulo,omitempty"`
	Texto              string        `json:"texto"`
	ImagenURL          *string       `json:"imagen_url,omitempty"`
	Fuente             *string       `json:"fuente,omitempty"`
	CantidadItems      int           `json:"cantidad_items"`
	CantidadPublicados int           `json:"cantidad_publicados"`
	FechaCreacion      time.Time     `json:"fecha_creacion"`
	FechaEdicion       *time.Time    `json:"fecha_edicion,omitempty"`
}

type FiltrosEstimulos struct {
	Nivel  *domain.Nivel
	Buscar string
	Limit  int
	Offset int
}

const selectEstimulo = `SELECT e.id::text, e.clave, e.nivel::text, e.titulo, e.texto, e.imagen_url, e.fuente,
       (SELECT count(*) FROM items i WHERE i.estimulo_id = e.id),
       (SELECT count(*) FROM items i WHERE i.estimulo_id = e.id AND i.estado = 'publicado'),
       e.fecha_creacion, e.fecha_edicion
FROM estimulos e`

func escanearEstimulo(row pgx.Row) (EstimuloBanco, error) {
	var e EstimuloBanco
	var nivel *string
	err := row.Scan(&e.ID, &e.Clave, &nivel, &e.Titulo, &e.Texto, &e.ImagenURL, &e.Fuente,
		&e.CantidadItems, &e.CantidadPublicados, &e.FechaCreacion, &e.FechaEdicion)
	if nivel != nil {
		n := domain.Nivel(*nivel)
		e.Nivel = &n
	}
	return e, err
}

func (r *Estimulos) Listar(ctx context.Context, f FiltrosEstimulos) ([]EstimuloBanco, error) {
	q := selectEstimulo + ` WHERE 1=1`
	var args []any
	if f.Nivel != nil {
		args = append(args, string(*f.Nivel))
		q += fmt.Sprintf(" AND e.nivel = $%d", len(args))
	}
	if f.Buscar != "" {
		args = append(args, "%"+f.Buscar+"%")
		q += fmt.Sprintf(" AND (e.titulo ILIKE $%d OR e.texto ILIKE $%d)", len(args), len(args))
	}
	args = append(args, f.Limit, f.Offset)
	q += fmt.Sprintf(" ORDER BY e.titulo NULLS LAST, e.fecha_creacion LIMIT $%d OFFSET $%d", len(args)-1, len(args))

	rows, err := r.pool.Query(ctx, q, args...)
	if err != nil {
		return nil, fmt.Errorf("listar estímulos: %w", err)
	}
	defer rows.Close()
	out := []EstimuloBanco{}
	for rows.Next() {
		e, err := escanearEstimulo(rows)
		if err != nil {
			return nil, fmt.Errorf("leer estímulo: %w", err)
		}
		out = append(out, e)
	}
	return out, rows.Err()
}

func (r *Estimulos) PorID(ctx context.Context, id string) (EstimuloBanco, error) {
	e, err := escanearEstimulo(r.pool.QueryRow(ctx, selectEstimulo+` WHERE e.id = $1`, id))
	if errors.Is(err, pgx.ErrNoRows) {
		return EstimuloBanco{}, ErrNoEncontrado
	}
	return e, err
}

func (r *Estimulos) Crear(ctx context.Context, e EstimuloBanco) (EstimuloBanco, error) {
	const q = `INSERT INTO estimulos (nivel, titulo, texto, imagen_url, fuente, fecha_edicion)
	           VALUES ($1,$2,$3,$4,$5, now()) RETURNING id::text`
	var id string
	if err := r.pool.QueryRow(ctx, q, nivelTexto(e.Nivel), e.Titulo, e.Texto, e.ImagenURL, e.Fuente).Scan(&id); err != nil {
		return EstimuloBanco{}, fmt.Errorf("crear estímulo: %w", err)
	}
	return r.PorID(ctx, id)
}

// Actualizar marca fecha_edicion: desde ahí el generador ya no pisa el texto al recargar su SQL.
func (r *Estimulos) Actualizar(ctx context.Context, id string, e EstimuloBanco) (EstimuloBanco, error) {
	const q = `UPDATE estimulos SET nivel=$1, titulo=$2, texto=$3, imagen_url=$4, fuente=$5, fecha_edicion=now() WHERE id=$6`
	ct, err := r.pool.Exec(ctx, q, nivelTexto(e.Nivel), e.Titulo, e.Texto, e.ImagenURL, e.Fuente, id)
	if err != nil {
		return EstimuloBanco{}, fmt.Errorf("actualizar estímulo: %w", err)
	}
	if ct.RowsAffected() == 0 {
		return EstimuloBanco{}, ErrNoEncontrado
	}
	return r.PorID(ctx, id)
}

func (r *Estimulos) Eliminar(ctx context.Context, id string) error {
	ct, err := r.pool.Exec(ctx, `DELETE FROM estimulos e WHERE e.id = $1 AND NOT EXISTS (SELECT 1 FROM items i WHERE i.estimulo_id = e.id)`, id)
	if err != nil {
		return fmt.Errorf("eliminar estímulo: %w", err)
	}
	if ct.RowsAffected() == 1 {
		return nil
	}
	if _, err := r.PorID(ctx, id); err != nil {
		return err
	}
	return ErrEstimuloEnUso
}

func nivelTexto(n *domain.Nivel) *string {
	if n == nil {
		return nil
	}
	s := string(*n)
	return &s
}
