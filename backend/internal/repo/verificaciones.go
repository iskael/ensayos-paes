package repo

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"errors"
	"time"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

var ErrTokenInvalido = errors.New("token inválido o expirado")

type Verificaciones struct {
	pool *pgxpool.Pool
}

func NewVerificaciones(pool *pgxpool.Pool) *Verificaciones {
	return &Verificaciones{pool: pool}
}

func generarToken() (string, error) {
	b := make([]byte, 32)
	if _, err := rand.Read(b); err != nil {
		return "", err
	}
	return hex.EncodeToString(b), nil
}

// Crear genera un token nuevo para el usuario, válido 24 horas. Si ya
// existía un token para ese usuario, lo reemplaza (un usuario tiene a lo
// sumo un token activo a la vez).
func (r *Verificaciones) Crear(ctx context.Context, usuarioID string) (string, error) {
	token, err := generarToken()
	if err != nil {
		return "", err
	}
	const q = `INSERT INTO verificaciones_email (token, usuario_id, fecha_expiracion)
	           VALUES ($1, $2, now() + interval '24 hours')
	           ON CONFLICT (usuario_id) DO UPDATE
	           SET token = EXCLUDED.token, fecha_expiracion = EXCLUDED.fecha_expiracion, fecha_creacion = now()`
	if _, err := r.pool.Exec(ctx, q, token, usuarioID); err != nil {
		return "", err
	}
	return token, nil
}

// Consumir valida el token y, si es válido, marca la cuenta como
// verificada y borra el token (de un solo uso). ErrTokenInvalido cubre
// tanto "no existe" como "expiró" — la solución es la misma para el
// usuario: pedir un link nuevo.
func (r *Verificaciones) Consumir(ctx context.Context, token string) (string, error) {
	var usuarioID string
	var expiracion time.Time
	const qBuscar = `SELECT usuario_id::text, fecha_expiracion FROM verificaciones_email WHERE token = $1`
	err := r.pool.QueryRow(ctx, qBuscar, token).Scan(&usuarioID, &expiracion)
	if errors.Is(err, pgx.ErrNoRows) {
		return "", ErrTokenInvalido
	}
	if err != nil {
		return "", err
	}
	if time.Now().After(expiracion) {
		return "", ErrTokenInvalido
	}

	tx, err := r.pool.Begin(ctx)
	if err != nil {
		return "", err
	}
	defer tx.Rollback(ctx)

	if _, err := tx.Exec(ctx, `UPDATE usuarios SET email_verificado = TRUE WHERE id = $1`, usuarioID); err != nil {
		return "", err
	}
	if _, err := tx.Exec(ctx, `DELETE FROM verificaciones_email WHERE token = $1`, token); err != nil {
		return "", err
	}
	if err := tx.Commit(ctx); err != nil {
		return "", err
	}
	return usuarioID, nil
}
