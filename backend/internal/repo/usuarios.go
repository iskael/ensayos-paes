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

// Crear inserta el usuario y, en la misma transacción, su aceptación de los
// Términos y Condiciones vigentes (versionTerminos) — si una de las dos
// operaciones falla, no queda un usuario sin aceptación registrada.
func (r *Usuarios) Crear(ctx context.Context, nombre, email, hash string, rol domain.Rol, versionTerminos string) (domain.Usuario, error) {
	tx, err := r.pool.Begin(ctx)
	if err != nil {
		return domain.Usuario{}, err
	}
	defer tx.Rollback(ctx)

	u := domain.Usuario{Nombre: nombre, Email: email, Rol: rol}
	const qUsuario = `INSERT INTO usuarios (nombre, email, password_hash, rol)
	                   VALUES ($1, $2, $3, $4)
	                   RETURNING id::text, fecha_creacion`
	if err := tx.QueryRow(ctx, qUsuario, nombre, email, hash, string(rol)).Scan(&u.ID, &u.FechaCreacion); err != nil {
		var pgErr *pgconn.PgError
		if errors.As(err, &pgErr) && pgErr.Code == "23505" {
			return domain.Usuario{}, ErrEmailDuplicado
		}
		return domain.Usuario{}, err
	}

	const qTerminos = `INSERT INTO terminos_aceptados (usuario_id, version) VALUES ($1, $2)`
	if _, err := tx.Exec(ctx, qTerminos, u.ID, versionTerminos); err != nil {
		return domain.Usuario{}, err
	}

	if err := tx.Commit(ctx); err != nil {
		return domain.Usuario{}, err
	}
	return u, nil
}

// PorEmail retorna el usuario y su hash de contraseña (para login).
func (r *Usuarios) PorEmail(ctx context.Context, email string) (domain.Usuario, string, error) {
	var u domain.Usuario
	var hash, rol string
	const q = `SELECT id::text, nombre, email, rol::text, email_verificado, fecha_creacion, password_hash
	           FROM usuarios WHERE email = $1`
	err := r.pool.QueryRow(ctx, q, email).Scan(&u.ID, &u.Nombre, &u.Email, &rol, &u.EmailVerificado, &u.FechaCreacion, &hash)
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
	const q = `SELECT id::text, nombre, email, rol::text, email_verificado, fecha_creacion
	           FROM usuarios WHERE id = $1`
	err := r.pool.QueryRow(ctx, q, id).Scan(&u.ID, &u.Nombre, &u.Email, &rol, &u.EmailVerificado, &u.FechaCreacion)
	if errors.Is(err, pgx.ErrNoRows) {
		return domain.Usuario{}, ErrNoEncontrado
	}
	if err != nil {
		return domain.Usuario{}, err
	}
	u.Rol = domain.Rol(rol)
	return u, nil
}
