package repo

import (
	"context"

	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/usuario/ensayos-paes/internal/domain"
)

type Clave struct {
	pool *pgxpool.Pool
}

func NewClave(pool *pgxpool.Pool) *Clave {
	return &Clave{pool: pool}
}

type PesoItem struct {
	ItemID string
	Peso   int
}

type ClaveEstado struct {
	SumaPesosPublicados int
	Valida              bool
	Pesos               []PesoItem
}

// ActualizarPesos aplica el peso a cada ítem indicado, verificando que
// pertenezca al examen dado. Si algún ítem no pertenece, retorna ErrNoEncontrado.
func (r *Clave) ActualizarPesos(ctx context.Context, examenID string, pesos []PesoItem) error {
	tx, err := r.pool.Begin(ctx)
	if err != nil {
		return err
	}
	defer tx.Rollback(ctx)

	for _, p := range pesos {
		ct, err := tx.Exec(ctx, `UPDATE items SET peso = $1 WHERE id = $2 AND examen_fuente_id = $3`, p.Peso, p.ItemID, examenID)
		if err != nil {
			return err
		}
		if ct.RowsAffected() == 0 {
			return ErrNoEncontrado
		}
	}
	return tx.Commit(ctx)
}

// Obtener retorna el estado de la clave: suma de pesos de ítems PUBLICADOS
// (para validar RN-03) y el detalle de pesos de todos los ítems del examen.
func (r *Clave) Obtener(ctx context.Context, examenID string) (ClaveEstado, error) {
	var ce ClaveEstado
	const qSuma = `SELECT COALESCE(SUM(peso), 0) FROM items WHERE examen_fuente_id = $1 AND estado = 'publicado'`
	if err := r.pool.QueryRow(ctx, qSuma, examenID).Scan(&ce.SumaPesosPublicados); err != nil {
		return ClaveEstado{}, err
	}
	ce.Valida = ce.SumaPesosPublicados == domain.PesoTotalClave

	rows, err := r.pool.Query(ctx, `SELECT id::text, COALESCE(peso, 0) FROM items WHERE examen_fuente_id = $1 ORDER BY fecha_creacion`, examenID)
	if err != nil {
		return ClaveEstado{}, err
	}
	defer rows.Close()
	for rows.Next() {
		var p PesoItem
		if err := rows.Scan(&p.ItemID, &p.Peso); err != nil {
			return ClaveEstado{}, err
		}
		ce.Pesos = append(ce.Pesos, p)
	}
	return ce, rows.Err()
}
