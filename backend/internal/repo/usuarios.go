package repo

import (
	"context"
	"errors"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgconn"
	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/usuario/ensayos-paes/internal/domain"
)

var (
	ErrNoEncontrado   = errors.New("no encontrado")
	ErrEmailDuplicado = errors.New("email duplicado")
)

type Usuarios struct {
	pool *pgxpool.Pool
}

func NewUsuarios(pool *pgxpool.Pool) *Usuarios {
	return &Usuarios{pool: pool}
}

func (r *Usuarios) Crear(ctx context.Context, nombre, email, hash string, rol domain.Rol) (domain.Usuario, error) {
	u := domain.Usuario{Nombre: nombre, Email: email, Rol: rol}
	const q = `INSERT INTO usuarios (nombre, email, password_hash, rol)
	           VALUES ($1, $2, $3, $4)
	           RETURNING id::text, fecha_creacion`
	err := r.pool.QueryRow(ctx, q, nombre, email, hash, string(rol)).Scan(&u.ID, &u.FechaCreacion)
	if err != nil {
		var pgErr *pgconn.PgError
		if errors.As(err, &pgErr) && pgErr.Code == "23505" {
			return domain.Usuario{}, ErrEmailDuplicado
		}
		return domain.Usuario{}, err
	}
	return u, nil
}

// PorEmail retorna el usuario y su hash de contraseña (para login).
func (r *Usuarios) PorEmail(ctx context.Context, email string) (domain.Usuario, string, error) {
	var u domain.Usuario
	var hash, rol string
	const q = `SELECT id::text, nombre, email, rol::text, fecha_creacion, password_hash
	           FROM usuarios WHERE email = $1`
	err := r.pool.QueryRow(ctx, q, email).Scan(&u.ID, &u.Nombre, &u.Email, &rol, &u.FechaCreacion, &hash)
	if errors.Is(err, pgx.ErrNoRows) {
		return domain.Usuario{}, "", ErrNoEncontrado
	}
	if err != nil {
		return domain.Usuario{}, "", err
	}
	u.Rol = domain.Rol(rol)
	return u, hash, nil
}

func (r *Usuarios) PorID(ctx context.Context, id string) (domain.Usuario, error) {
	var u domain.Usuario
	var rol string
	const q = `SELECT id::text, nombre, email, rol::text, fecha_creacion
	           FROM usuarios WHERE id = $1`
	err := r.pool.QueryRow(ctx, q, id).Scan(&u.ID, &u.Nombre, &u.Email, &rol, &u.FechaCreacion)
	if errors.Is(err, pgx.ErrNoRows) {
		return domain.Usuario{}, ErrNoEncontrado
	}
	if err != nil {
		return domain.Usuario{}, err
	}
	u.Rol = domain.Rol(rol)
	return u, nil
}
