package repo

import (
	"context"
	"crypto/rand"
	"errors"
	"time"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgconn"
	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/usuario/ensayos-paes/internal/domain"
)

type Grupos struct {
	pool *pgxpool.Pool
}

func NewGrupos(pool *pgxpool.Pool) *Grupos {
	return &Grupos{pool: pool}
}

// alfabetoCodigo evita 0/O/1/I/L para que el código sea fácil de leer y dictar.
var alfabetoCodigo = []byte("ABCDEFGHJKMNPQRSTUVWXYZ23456789")

func generarCodigo(n int) (string, error) {
	buf := make([]byte, n)
	if _, err := rand.Read(buf); err != nil {
		return "", err
	}
	out := make([]byte, n)
	for i, v := range buf {
		out[i] = alfabetoCodigo[int(v)%len(alfabetoCodigo)]
	}
	return string(out), nil
}

// Crear genera un código de invitación único (reintenta ante colisión, poco
// probable con 7 caracteres de un alfabeto de 32 símbolos).
func (r *Grupos) Crear(ctx context.Context, nombre, profesorID string) (domain.Grupo, error) {
	for intento := 0; intento < 5; intento++ {
		codigo, err := generarCodigo(7)
		if err != nil {
			return domain.Grupo{}, err
		}
		var g domain.Grupo
		const q = `INSERT INTO grupos (nombre, profesor_id, codigo_invitacion)
		           VALUES ($1,$2,$3) RETURNING id::text, fecha_creacion`
		err = r.pool.QueryRow(ctx, q, nombre, profesorID, codigo).Scan(&g.ID, &g.FechaCreacion)
		if err == nil {
			g.Nombre = nombre
			g.ProfesorID = profesorID
			g.CodigoInvitacion = codigo
			return g, nil
		}
		var pgErr *pgconn.PgError
		if errors.As(err, &pgErr) && pgErr.Code == "23505" {
			continue
		}
		return domain.Grupo{}, err
	}
	return domain.Grupo{}, errors.New("no se pudo generar un código de invitación único")
}

func (r *Grupos) PorID(ctx context.Context, id string) (domain.Grupo, error) {
	var g domain.Grupo
	const q = `SELECT id::text, nombre, profesor_id::text, codigo_invitacion, fecha_creacion
	           FROM grupos WHERE id = $1`
	err := r.pool.QueryRow(ctx, q, id).Scan(&g.ID, &g.Nombre, &g.ProfesorID, &g.CodigoInvitacion, &g.FechaCreacion)
	if errors.Is(err, pgx.ErrNoRows) {
		return domain.Grupo{}, ErrNoEncontrado
	}
	return g, err
}

func (r *Grupos) ListarPorProfesor(ctx context.Context, profesorID string) ([]domain.Grupo, error) {
	const q = `SELECT id::text, nombre, profesor_id::text, codigo_invitacion, fecha_creacion
	           FROM grupos WHERE profesor_id = $1 ORDER BY fecha_creacion DESC`
	rows, err := r.pool.Query(ctx, q, profesorID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	out := []domain.Grupo{}
	for rows.Next() {
		var g domain.Grupo
		if err := rows.Scan(&g.ID, &g.Nombre, &g.ProfesorID, &g.CodigoInvitacion, &g.FechaCreacion); err != nil {
			return nil, err
		}
		out = append(out, g)
	}
	return out, rows.Err()
}

// UnirsePorCodigo es idempotente: si el estudiante ya pertenece al grupo, no falla.
func (r *Grupos) UnirsePorCodigo(ctx context.Context, estudianteID, codigo string) (domain.Grupo, error) {
	var g domain.Grupo
	const qGrupo = `SELECT id::text, nombre, profesor_id::text, codigo_invitacion, fecha_creacion
	                FROM grupos WHERE codigo_invitacion = $1`
	err := r.pool.QueryRow(ctx, qGrupo, codigo).Scan(&g.ID, &g.Nombre, &g.ProfesorID, &g.CodigoInvitacion, &g.FechaCreacion)
	if errors.Is(err, pgx.ErrNoRows) {
		return domain.Grupo{}, ErrNoEncontrado
	}
	if err != nil {
		return domain.Grupo{}, err
	}

	const qJoin = `INSERT INTO grupo_miembros (grupo_id, estudiante_id) VALUES ($1,$2)
	               ON CONFLICT (grupo_id, estudiante_id) DO NOTHING`
	if _, err := r.pool.Exec(ctx, qJoin, g.ID, estudianteID); err != nil {
		return domain.Grupo{}, err
	}
	return g, nil
}

type MiembroBasico struct {
	EstudianteID string
	Nombre       string
	FechaUnion   time.Time
}

func (r *Grupos) Miembros(ctx context.Context, grupoID string) ([]MiembroBasico, error) {
	const q = `SELECT u.id::text, u.nombre, gm.fecha_union
	           FROM grupo_miembros gm
	           JOIN usuarios u ON u.id = gm.estudiante_id
	           WHERE gm.grupo_id = $1
	           ORDER BY gm.fecha_union`
	rows, err := r.pool.Query(ctx, q, grupoID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	out := []MiembroBasico{}
	for rows.Next() {
		var m MiembroBasico
		if err := rows.Scan(&m.EstudianteID, &m.Nombre, &m.FechaUnion); err != nil {
			return nil, err
		}
		out = append(out, m)
	}
	return out, rows.Err()
}

// EsMiembro autoriza la consulta de progreso individual (RN-06: el profesor
// solo ve estudiantes que efectivamente pertenecen a su grupo).
func (r *Grupos) EsMiembro(ctx context.Context, grupoID, estudianteID string) (bool, error) {
	const q = `SELECT EXISTS(SELECT 1 FROM grupo_miembros WHERE grupo_id = $1 AND estudiante_id = $2)`
	var existe bool
	err := r.pool.QueryRow(ctx, q, grupoID, estudianteID).Scan(&existe)
	return existe, err
}
