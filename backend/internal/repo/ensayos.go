package repo

import (
	"context"
	"errors"
	"math/rand"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/usuario/ensayos-paes/internal/domain"
)

var ErrStockInsuficiente = errors.New("stock insuficiente")

type StockInsuficienteError struct {
	MaxDisponible     int
	DisponiblesPorEje map[domain.Eje]int
}

func (e *StockInsuficienteError) Error() string { return "stock insuficiente para generar el ensayo" }
func (e *StockInsuficienteError) Unwrap() error  { return ErrStockInsuficiente }

type Ensayos struct {
	pool *pgxpool.Pool
}

func NewEnsayos(pool *pgxpool.Pool) *Ensayos {
	return &Ensayos{pool: pool}
}

type RespuestaInput struct {
	EnsayoItemID string
	Respuesta    domain.EtiquetaAlternativa
}

type EnsayoItemDetalle struct {
	EnsayoItemID          string
	Orden                 int
	ItemID                string
	Enunciado             string
	ImagenURL             *string
	Eje                   domain.Eje
	Explicacion           *string
	PesoSnapshot          int
	Alternativas          []domain.Alternativa
	RespuestaSeleccionada *domain.EtiquetaAlternativa
	EsCorrecta            *bool
}

type EnsayoDetalle struct {
	Ensayo domain.Ensayo
	Items  []EnsayoItemDetalle
}

func (r *Ensayos) disponibilidadPorEje(ctx context.Context, nivel domain.Nivel, ejes []domain.Eje) (map[domain.Eje]int, error) {
	disp := make(map[domain.Eje]int, len(ejes))
	ejesStr := make([]string, len(ejes))
	for i, e := range ejes {
		disp[e] = 0
		ejesStr[i] = string(e)
	}
	const q = `SELECT eje::text, COUNT(*) FROM items
	           WHERE estado = 'publicado' AND nivel = $1 AND eje = ANY($2)
	           GROUP BY eje`
	rows, err := r.pool.Query(ctx, q, string(nivel), ejesStr)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	for rows.Next() {
		var eje string
		var n int
		if err := rows.Scan(&eje, &n); err != nil {
			return nil, err
		}
		disp[domain.Eje(eje)] = n
	}
	return disp, rows.Err()
}

// GenerarAleatorio aplica RN-01: filtra por publicado+nivel+eje, distribuye
// por eje (domain.DistribuirCantidad) y, si falta stock, no crea el ensayo.
func (r *Ensayos) GenerarAleatorio(ctx context.Context, estudianteID string, nivel domain.Nivel, ejes []domain.Eje, cantidad int, modo domain.ModoEnsayo) (EnsayoDetalle, error) {
	disp, err := r.disponibilidadPorEje(ctx, nivel, ejes)
	if err != nil {
		return EnsayoDetalle{}, err
	}
	seleccion, faltante := domain.DistribuirCantidad(cantidad, ejes, disp)
	if faltante > 0 {
		total := 0
		for _, n := range disp {
			total += n
		}
		return EnsayoDetalle{}, &StockInsuficienteError{MaxDisponible: total, DisponiblesPorEje: disp}
	}

	tx, err := r.pool.Begin(ctx)
	if err != nil {
		return EnsayoDetalle{}, err
	}
	defer tx.Rollback(ctx)

	type itemSel struct {
		id   string
		peso int
	}
	var seleccionados []itemSel
	for _, eje := range ejes {
		n := seleccion[eje]
		if n == 0 {
			continue
		}
		const q = `SELECT id::text, peso FROM items
		           WHERE estado = 'publicado' AND nivel = $1 AND eje = $2
		           ORDER BY random() LIMIT $3`
		rows, err := tx.Query(ctx, q, string(nivel), string(eje), n)
		if err != nil {
			return EnsayoDetalle{}, err
		}
		for rows.Next() {
			var s itemSel
			if err := rows.Scan(&s.id, &s.peso); err != nil {
				rows.Close()
				return EnsayoDetalle{}, err
			}
			seleccionados = append(seleccionados, s)
		}
		rows.Close()
		if err := rows.Err(); err != nil {
			return EnsayoDetalle{}, err
		}
	}

	rand.Shuffle(len(seleccionados), func(i, j int) {
		seleccionados[i], seleccionados[j] = seleccionados[j], seleccionados[i]
	})

	ejesTexto := make([]string, len(ejes))
	for i, e := range ejes {
		ejesTexto[i] = string(e)
	}
	var ensayoID string
	const qEnsayo = `INSERT INTO ensayos (estudiante_id, nivel, ejes, cantidad, modo, estado)
	                  VALUES ($1,$2,$3,$4,$5,'en_progreso') RETURNING id::text`
	if err := tx.QueryRow(ctx, qEnsayo, estudianteID, string(nivel), ejesTexto, cantidad, string(modo)).Scan(&ensayoID); err != nil {
		return EnsayoDetalle{}, err
	}

	const qEI = `INSERT INTO ensayo_items (ensayo_id, item_id, orden, peso_snapshot) VALUES ($1,$2,$3,$4)`
	for i, s := range seleccionados {
		if _, err := tx.Exec(ctx, qEI, ensayoID, s.id, i+1, s.peso); err != nil {
			return EnsayoDetalle{}, err
		}
	}

	if err := tx.Commit(ctx); err != nil {
		return EnsayoDetalle{}, err
	}
	return r.ObtenerDetalle(ctx, ensayoID)
}

// ObtenerBase carga solo la fila de ensayos (sin preguntas), útil para
// chequeos de dueño/estado antes de operaciones más costosas.
func (r *Ensayos) ObtenerBase(ctx context.Context, id string) (domain.Ensayo, error) {
	var e domain.Ensayo
	var nivel, modo, estado string
	var ejes []string
	const q = `SELECT id::text, estudiante_id::text, nivel::text, ejes::text[], cantidad, modo, estado::text,
	                  fecha_inicio, fecha_fin, puntaje, puntos_obtenidos, puntos_posibles, correctas, total
	           FROM ensayos WHERE id = $1`
	err := r.pool.QueryRow(ctx, q, id).Scan(
		&e.ID, &e.EstudianteID, &nivel, &ejes, &e.Cantidad, &modo, &estado,
		&e.FechaInicio, &e.FechaFin, &e.Puntaje, &e.PuntosObtenidos, &e.PuntosPosibles, &e.Correctas, &e.Total,
	)
	if errors.Is(err, pgx.ErrNoRows) {
		return domain.Ensayo{}, ErrNoEncontrado
	}
	if err != nil {
		return domain.Ensayo{}, err
	}
	e.Nivel = domain.Nivel(nivel)
	e.Modo = domain.ModoEnsayo(modo)
	e.Estado = domain.EstadoEnsayo(estado)
	e.Ejes = make([]domain.Eje, len(ejes))
	for i, s := range ejes {
		e.Ejes[i] = domain.Eje(s)
	}
	return e, nil
}

func (r *Ensayos) ListarPorEstudiante(ctx context.Context, estudianteID string, limit, offset int) ([]domain.Ensayo, error) {
	const q = `SELECT id::text, estudiante_id::text, nivel::text, ejes::text[], cantidad, modo, estado::text,
	                  fecha_inicio, fecha_fin, puntaje, puntos_obtenidos, puntos_posibles, correctas, total
	           FROM ensayos WHERE estudiante_id = $1
	           ORDER BY fecha_inicio DESC LIMIT $2 OFFSET $3`
	rows, err := r.pool.Query(ctx, q, estudianteID, limit, offset)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	out := []domain.Ensayo{}
	for rows.Next() {
		var e domain.Ensayo
		var nivel, modo, estado string
		var ejes []string
		if err := rows.Scan(&e.ID, &e.EstudianteID, &nivel, &ejes, &e.Cantidad, &modo, &estado,
			&e.FechaInicio, &e.FechaFin, &e.Puntaje, &e.PuntosObtenidos, &e.PuntosPosibles, &e.Correctas, &e.Total); err != nil {
			return nil, err
		}
		e.Nivel = domain.Nivel(nivel)
		e.Modo = domain.ModoEnsayo(modo)
		e.Estado = domain.EstadoEnsayo(estado)
		e.Ejes = make([]domain.Eje, len(ejes))
		for i, s := range ejes {
			e.Ejes[i] = domain.Eje(s)
		}
		out = append(out, e)
	}
	return out, rows.Err()
}

func (r *Ensayos) ObtenerDetalle(ctx context.Context, id string) (EnsayoDetalle, error) {
	ensayo, err := r.ObtenerBase(ctx, id)
	if err != nil {
		return EnsayoDetalle{}, err
	}

	const q = `SELECT ei.id::text, ei.orden, ei.item_id::text, i.enunciado, i.imagen_url, i.eje::text, i.explicacion,
	                  ei.peso_snapshot, ei.respuesta_seleccionada::text, ei.es_correcta
	           FROM ensayo_items ei
	           JOIN items i ON i.id = ei.item_id
	           WHERE ei.ensayo_id = $1
	           ORDER BY ei.orden`
	rows, err := r.pool.Query(ctx, q, id)
	if err != nil {
		return EnsayoDetalle{}, err
	}
	var items []EnsayoItemDetalle
	var itemIDs []string
	for rows.Next() {
		var d EnsayoItemDetalle
		var eje string
		var respuesta *string
		if err := rows.Scan(&d.EnsayoItemID, &d.Orden, &d.ItemID, &d.Enunciado, &d.ImagenURL, &eje, &d.Explicacion, &d.PesoSnapshot, &respuesta, &d.EsCorrecta); err != nil {
			rows.Close()
			return EnsayoDetalle{}, err
		}
		d.Eje = domain.Eje(eje)
		if respuesta != nil {
			et := domain.EtiquetaAlternativa(*respuesta)
			d.RespuestaSeleccionada = &et
		}
		items = append(items, d)
		itemIDs = append(itemIDs, d.ItemID)
	}
	rows.Close()
	if err := rows.Err(); err != nil {
		return EnsayoDetalle{}, err
	}

	altsPorItem, err := r.alternativasPorItems(ctx, itemIDs)
	if err != nil {
		return EnsayoDetalle{}, err
	}
	for i := range items {
		items[i].Alternativas = altsPorItem[items[i].ItemID]
	}

	return EnsayoDetalle{Ensayo: ensayo, Items: items}, nil
}

func (r *Ensayos) alternativasPorItems(ctx context.Context, itemIDs []string) (map[string][]domain.Alternativa, error) {
	out := map[string][]domain.Alternativa{}
	if len(itemIDs) == 0 {
		return out, nil
	}
	const q = `SELECT item_id::text, id::text, etiqueta::text, texto, imagen_url, es_correcta
	           FROM alternativas WHERE item_id = ANY($1) ORDER BY item_id, etiqueta`
	rows, err := r.pool.Query(ctx, q, itemIDs)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	for rows.Next() {
		var itemID string
		var a domain.Alternativa
		var etq string
		if err := rows.Scan(&itemID, &a.ID, &etq, &a.Texto, &a.ImagenURL, &a.EsCorrecta); err != nil {
			return nil, err
		}
		a.Etiqueta = domain.EtiquetaAlternativa(etq)
		out[itemID] = append(out[itemID], a)
	}
	return out, rows.Err()
}

func (r *Ensayos) GuardarRespuestas(ctx context.Context, ensayoID string, respuestas []RespuestaInput) error {
	tx, err := r.pool.Begin(ctx)
	if err != nil {
		return err
	}
	defer tx.Rollback(ctx)

	const q = `UPDATE ensayo_items SET respuesta_seleccionada = $1 WHERE id = $2 AND ensayo_id = $3`
	for _, resp := range respuestas {
		ct, err := tx.Exec(ctx, q, string(resp.Respuesta), resp.EnsayoItemID, ensayoID)
		if err != nil {
			return err
		}
		if ct.RowsAffected() == 0 {
			return ErrNoEncontrado
		}
	}
	return tx.Commit(ctx)
}

// Finalizar aplica RN-02: marca es_correcta por ítem (sin responder = falso),
// suma puntos por peso_snapshot y calcula el puntaje normalizado a 1000.
func (r *Ensayos) Finalizar(ctx context.Context, ensayoID string) (domain.Ensayo, error) {
	detalle, err := r.ObtenerDetalle(ctx, ensayoID)
	if err != nil {
		return domain.Ensayo{}, err
	}

	tx, err := r.pool.Begin(ctx)
	if err != nil {
		return domain.Ensayo{}, err
	}
	defer tx.Rollback(ctx)

	puntosObtenidos, puntosPosibles, correctas := 0, 0, 0
	const qMarcar = `UPDATE ensayo_items SET es_correcta = $1 WHERE id = $2`
	for _, it := range detalle.Items {
		correcta := respuestaEsCorrecta(it)
		if _, err := tx.Exec(ctx, qMarcar, correcta, it.EnsayoItemID); err != nil {
			return domain.Ensayo{}, err
		}
		puntosPosibles += it.PesoSnapshot
		if correcta {
			puntosObtenidos += it.PesoSnapshot
			correctas++
		}
	}
	puntaje := domain.CalcularPuntaje(puntosObtenidos, puntosPosibles)
	total := len(detalle.Items)

	const qEnsayo = `UPDATE ensayos SET estado = 'finalizado', fecha_fin = now(),
	                  puntaje = $1, puntos_obtenidos = $2, puntos_posibles = $3, correctas = $4, total = $5
	                  WHERE id = $6`
	if _, err := tx.Exec(ctx, qEnsayo, puntaje, puntosObtenidos, puntosPosibles, correctas, total, ensayoID); err != nil {
		return domain.Ensayo{}, err
	}
	if err := tx.Commit(ctx); err != nil {
		return domain.Ensayo{}, err
	}
	return r.ObtenerBase(ctx, ensayoID)
}

func respuestaEsCorrecta(it EnsayoItemDetalle) bool {
	if it.RespuestaSeleccionada == nil {
		return false
	}
	for _, a := range it.Alternativas {
		if a.Etiqueta == *it.RespuestaSeleccionada {
			return a.EsCorrecta
		}
	}
	return false
}
