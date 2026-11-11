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

var ErrYaExiste = errors.New("ya existe")

type Instituciones struct {
	pool *pgxpool.Pool
}

func NewInstituciones(pool *pgxpool.Pool) *Instituciones {
	return &Instituciones{pool: pool}
}

type Institucion struct {
	ID               string    `json:"id"`
	Nombre           string    `json:"nombre"`
	CodigoInvitacion string    `json:"codigo_invitacion,omitempty"`
	FechaCreacion    time.Time `json:"fecha_creacion"`
}

type ProfesorInstitucion struct {
	ID          string `json:"id"`
	Nombre      string `json:"nombre"`
	Email       string `json:"email"`
	Grupos      int    `json:"grupos"`
	Estudiantes int    `json:"estudiantes"`
}

type GrupoInstitucion struct {
	ID             string `json:"id"`
	Nombre         string `json:"nombre"`
	ProfesorNombre string `json:"profesor_nombre"`
	Miembros       int    `json:"miembros"`
}

func conCodigoUnico(intentar func(codigo string) error) error {
	for intento := 0; intento < 5; intento++ {
		codigo, err := generarCodigo(7)
		if err != nil {
			return err
		}
		err = intentar(codigo)
		var pgErr *pgconn.PgError
		if errors.As(err, &pgErr) && pgErr.Code == "23505" && pgErr.ConstraintName == "instituciones_codigo_invitacion_key" {
			continue
		}
		return err
	}
	return errors.New("no se pudo generar un código de invitación único")
}

func (r *Instituciones) Crear(ctx context.Context, nombre, responsableID string) (Institucion, error) {
	inst := Institucion{Nombre: nombre}
	err := conCodigoUnico(func(codigo string) error {
		inst.CodigoInvitacion = codigo
		return r.pool.QueryRow(ctx, `INSERT INTO instituciones (nombre, responsable_id, codigo_invitacion) VALUES ($1,$2,$3)
		                             RETURNING id::text, fecha_creacion`, nombre, responsableID, codigo).Scan(&inst.ID, &inst.FechaCreacion)
	})
	var pgErr *pgconn.PgError
	if errors.As(err, &pgErr) && pgErr.Code == "23505" {
		return Institucion{}, ErrYaExiste
	}
	if err != nil {
		return Institucion{}, fmt.Errorf("crear institución: %w", err)
	}
	return inst, nil
}

func (r *Instituciones) unica(ctx context.Context, q string, arg any) (Institucion, error) {
	var i Institucion
	err := r.pool.QueryRow(ctx, q, arg).Scan(&i.ID, &i.Nombre, &i.CodigoInvitacion, &i.FechaCreacion)
	if errors.Is(err, pgx.ErrNoRows) {
		return Institucion{}, ErrNoEncontrado
	}
	if err != nil {
		return Institucion{}, fmt.Errorf("leer institución: %w", err)
	}
	return i, nil
}

func (r *Instituciones) DeResponsable(ctx context.Context, responsableID string) (Institucion, error) {
	return r.unica(ctx, `SELECT id::text, nombre, codigo_invitacion, fecha_creacion FROM instituciones WHERE responsable_id = $1`, responsableID)
}

// DeProfesor no expone el código de invitación: solo lo ve el responsable.
func (r *Instituciones) DeProfesor(ctx context.Context, profesorID string) (Institucion, error) {
	i, err := r.unica(ctx, `SELECT i.id::text, i.nombre, '', i.fecha_creacion FROM instituciones i
	                        JOIN usuarios u ON u.institucion_id = i.id WHERE u.id = $1`, profesorID)
	return i, err
}

func (r *Instituciones) Renombrar(ctx context.Context, id, nombre string) error {
	_, err := r.pool.Exec(ctx, `UPDATE instituciones SET nombre = $1 WHERE id = $2`, nombre, id)
	return err
}

func (r *Instituciones) NuevoCodigo(ctx context.Context, id string) (string, error) {
	var nuevo string
	err := conCodigoUnico(func(codigo string) error {
		nuevo = codigo
		_, err := r.pool.Exec(ctx, `UPDATE instituciones SET codigo_invitacion = $1 WHERE id = $2`, codigo, id)
		return err
	})
	if err != nil {
		return "", fmt.Errorf("regenerar código: %w", err)
	}
	return nuevo, nil
}

func (r *Instituciones) UnirseProfesor(ctx context.Context, profesorID, codigo string) (Institucion, error) {
	i, err := r.unica(ctx, `SELECT id::text, nombre, '', fecha_creacion FROM instituciones WHERE codigo_invitacion = $1`, codigo)
	if err != nil {
		return Institucion{}, err
	}
	if _, err := r.pool.Exec(ctx, `UPDATE usuarios SET institucion_id = $1 WHERE id = $2`, i.ID, profesorID); err != nil {
		return Institucion{}, fmt.Errorf("unir profesor: %w", err)
	}
	return i, nil
}

func (r *Instituciones) QuitarProfesor(ctx context.Context, institucionID, profesorID string) error {
	ct, err := r.pool.Exec(ctx, `UPDATE usuarios SET institucion_id = NULL WHERE id = $1 AND institucion_id = $2`, profesorID, institucionID)
	if err != nil {
		return fmt.Errorf("quitar profesor: %w", err)
	}
	if ct.RowsAffected() == 0 {
		return ErrNoEncontrado
	}
	return nil
}

func (r *Instituciones) Profesores(ctx context.Context, institucionID string) ([]ProfesorInstitucion, error) {
	const q = `SELECT u.id::text, u.nombre, u.email,
	                  (SELECT count(*) FROM grupos g WHERE g.profesor_id = u.id),
	                  (SELECT count(DISTINCT m.estudiante_id) FROM grupos g JOIN grupo_miembros m ON m.grupo_id = g.id WHERE g.profesor_id = u.id)
	           FROM usuarios u WHERE u.institucion_id = $1 ORDER BY u.nombre`
	rows, err := r.pool.Query(ctx, q, institucionID)
	if err != nil {
		return nil, fmt.Errorf("listar profesores: %w", err)
	}
	defer rows.Close()
	out := []ProfesorInstitucion{}
	for rows.Next() {
		var p ProfesorInstitucion
		if err := rows.Scan(&p.ID, &p.Nombre, &p.Email, &p.Grupos, &p.Estudiantes); err != nil {
			return nil, fmt.Errorf("leer profesor: %w", err)
		}
		out = append(out, p)
	}
	return out, rows.Err()
}

func (r *Instituciones) Grupos(ctx context.Context, institucionID string) ([]GrupoInstitucion, error) {
	const q = `SELECT g.id::text, g.nombre, u.nombre, (SELECT count(*) FROM grupo_miembros m WHERE m.grupo_id = g.id)
	           FROM grupos g JOIN usuarios u ON u.id = g.profesor_id
	           WHERE u.institucion_id = $1 ORDER BY u.nombre, g.nombre`
	rows, err := r.pool.Query(ctx, q, institucionID)
	if err != nil {
		return nil, fmt.Errorf("listar grupos de la institución: %w", err)
	}
	defer rows.Close()
	out := []GrupoInstitucion{}
	for rows.Next() {
		var g GrupoInstitucion
		if err := rows.Scan(&g.ID, &g.Nombre, &g.ProfesorNombre, &g.Miembros); err != nil {
			return nil, fmt.Errorf("leer grupo: %w", err)
		}
		out = append(out, g)
	}
	return out, rows.Err()
}

func (r *Instituciones) TieneGrupo(ctx context.Context, institucionID, grupoID string) (bool, error) {
	var ok bool
	err := r.pool.QueryRow(ctx, `SELECT EXISTS (SELECT 1 FROM grupos g JOIN usuarios u ON u.id = g.profesor_id
	                             WHERE g.id = $1 AND u.institucion_id = $2)`, grupoID, institucionID).Scan(&ok)
	return ok, err
}
