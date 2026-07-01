package repo

import (
	"context"
	"errors"
	"fmt"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/usuario/ensayos-paes/internal/domain"
)

type Items struct {
	pool *pgxpool.Pool
}

func NewItems(pool *pgxpool.Pool) *Items {
	return &Items{pool: pool}
}

func (r *Items) Crear(ctx context.Context, it domain.Item) (domain.Item, error) {
	tx, err := r.pool.Begin(ctx)
	if err != nil {
		return domain.Item{}, err
	}
	defer tx.Rollback(ctx)

	// Los ítems siempre nacen en borrador (RN-04); publicar es un paso explícito.
	const qItem = `INSERT INTO items (examen_fuente_id, enunciado, imagen_url, eje, nivel, dificultad, origen, estado, peso, explicacion)
	               VALUES ($1,$2,$3,$4,$5,$6,$7,'borrador',$8,$9)
	               RETURNING id::text`
	origen := it.Origen
	if origen == "" {
		origen = domain.OrigenOficial
	}
	if err := tx.QueryRow(ctx, qItem, it.ExamenFuenteID, it.Enunciado, it.ImagenURL, string(it.Eje), string(it.Nivel), string(it.Dificultad), string(origen), it.Peso, it.Explicacion).Scan(&it.ID); err != nil {
		return domain.Item{}, err
	}
	if err := insertarAlternativas(ctx, tx, it.ID, it.Alternativas); err != nil {
		return domain.Item{}, err
	}
	if err := tx.Commit(ctx); err != nil {
		return domain.Item{}, err
	}
	return r.PorID(ctx, it.ID)
}

func insertarAlternativas(ctx context.Context, tx pgx.Tx, itemID string, alts []domain.Alternativa) error {
	const q = `INSERT INTO alternativas (item_id, etiqueta, texto, imagen_url, es_correcta) VALUES ($1,$2,$3,$4,$5)`
	for _, a := range alts {
		if _, err := tx.Exec(ctx, q, itemID, string(a.Etiqueta), a.Texto, a.ImagenURL, a.EsCorrecta); err != nil {
			return err
		}
	}
	return nil
}

func (r *Items) PorID(ctx context.Context, id string) (domain.Item, error) {
	var it domain.Item
	var eje, nivel, dificultad, origen, estado string
	const q = `SELECT id::text, examen_fuente_id::text, enunciado, imagen_url, eje::text, nivel::text, dificultad::text, origen::text, estado::text, peso, explicacion, fecha_creacion
	           FROM items WHERE id = $1`
	err := r.pool.QueryRow(ctx, q, id).Scan(&it.ID, &it.ExamenFuenteID, &it.Enunciado, &it.ImagenURL, &eje, &nivel, &dificultad, &origen, &estado, &it.Peso, &it.Explicacion, &it.FechaCreacion)
	if errors.Is(err, pgx.ErrNoRows) {
		return domain.Item{}, ErrNoEncontrado
	}
	if err != nil {
		return domain.Item{}, err
	}
	it.Eje = domain.Eje(eje)
	it.Nivel = domain.Nivel(nivel)
	it.Dificultad = domain.Dificultad(dificultad)
	it.Origen = domain.OrigenItem(origen)
	it.Estado = domain.EstadoItem(estado)

	alts, err := r.alternativasDe(ctx, id)
	if err != nil {
		return domain.Item{}, err
	}
	it.Alternativas = alts
	return it, nil
}

func (r *Items) alternativasDe(ctx context.Context, itemID string) ([]domain.Alternativa, error) {
	const q = `SELECT id::text, etiqueta::text, texto, imagen_url, es_correcta FROM alternativas WHERE item_id = $1 ORDER BY etiqueta`
	rows, err := r.pool.Query(ctx, q, itemID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	out := []domain.Alternativa{}
	for rows.Next() {
		var a domain.Alternativa
		var etq string
		if err := rows.Scan(&a.ID, &etq, &a.Texto, &a.ImagenURL, &a.EsCorrecta); err != nil {
			return nil, err
		}
		a.Etiqueta = domain.EtiquetaAlternativa(etq)
		out = append(out, a)
	}
	return out, rows.Err()
}

func (r *Items) Actualizar(ctx context.Context, id string, it domain.Item) (domain.Item, error) {
	tx, err := r.pool.Begin(ctx)
	if err != nil {
		return domain.Item{}, err
	}
	defer tx.Rollback(ctx)

	const q = `UPDATE items SET examen_fuente_id=$1, enunciado=$2, imagen_url=$3, eje=$4, nivel=$5, dificultad=$6, peso=$7, explicacion=$8
	           WHERE id=$9`
	ct, err := tx.Exec(ctx, q, it.ExamenFuenteID, it.Enunciado, it.ImagenURL, string(it.Eje), string(it.Nivel), string(it.Dificultad), it.Peso, it.Explicacion, id)
	if err != nil {
		return domain.Item{}, err
	}
	if ct.RowsAffected() == 0 {
		return domain.Item{}, ErrNoEncontrado
	}
	if _, err := tx.Exec(ctx, `DELETE FROM alternativas WHERE item_id = $1`, id); err != nil {
		return domain.Item{}, err
	}
	if err := insertarAlternativas(ctx, tx, id, it.Alternativas); err != nil {
		return domain.Item{}, err
	}
	if err := tx.Commit(ctx); err != nil {
		return domain.Item{}, err
	}
	return r.PorID(ctx, id)
}

func (r *Items) Eliminar(ctx context.Context, id string) error {
	ct, err := r.pool.Exec(ctx, `DELETE FROM items WHERE id = $1`, id)
	if err != nil {
		return err
	}
	if ct.RowsAffected() == 0 {
		return ErrNoEncontrado
	}
	return nil
}

func (r *Items) CambiarEstado(ctx context.Context, id string, estado domain.EstadoItem) (domain.Item, error) {
	ct, err := r.pool.Exec(ctx, `UPDATE items SET estado = $1 WHERE id = $2`, string(estado), id)
	if err != nil {
		return domain.Item{}, err
	}
	if ct.RowsAffected() == 0 {
		return domain.Item{}, ErrNoEncontrado
	}
	return r.PorID(ctx, id)
}

type FiltrosItems struct {
	Nivel      *domain.Nivel
	Eje        *domain.Eje
	Dificultad *domain.Dificultad
	Estado     *domain.EstadoItem
	ExamenID   *string
	Limit      int
	Offset     int
}

// Listar aplica filtros opcionales. Para el volumen esperado en el MVP se
// resuelve con una consulta de IDs + lectura individual (PorID); si el banco
// crece mucho conviene una consulta con JOIN a alternativas.
func (r *Items) Listar(ctx context.Context, f FiltrosItems) ([]domain.Item, error) {
	q := `SELECT id::text FROM items WHERE 1=1`
	var args []any
	i := 1
	add := func(cond string, val any) {
		q += fmt.Sprintf(" AND %s $%d", cond, i)
		args = append(args, val)
		i++
	}
	if f.Nivel != nil {
		add("nivel =", string(*f.Nivel))
	}
	if f.Eje != nil {
		add("eje =", string(*f.Eje))
	}
	if f.Dificultad != nil {
		add("dificultad =", string(*f.Dificultad))
	}
	if f.Estado != nil {
		add("estado =", string(*f.Estado))
	}
	if f.ExamenID != nil {
		add("examen_fuente_id =", *f.ExamenID)
	}
	q += fmt.Sprintf(" ORDER BY fecha_creacion DESC LIMIT $%d OFFSET $%d", i, i+1)
	args = append(args, f.Limit, f.Offset)

	rows, err := r.pool.Query(ctx, q, args...)
	if err != nil {
		return nil, err
	}
	var ids []string
	for rows.Next() {
		var id string
		if err := rows.Scan(&id); err != nil {
			rows.Close()
			return nil, err
		}
		ids = append(ids, id)
	}
	rows.Close()
	if err := rows.Err(); err != nil {
		return nil, err
	}

	out := make([]domain.Item, 0, len(ids))
	for _, id := range ids {
		it, err := r.PorID(ctx, id)
		if err != nil {
			return nil, err
		}
		out = append(out, it)
	}
	return out, nil
}
