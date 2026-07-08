-- 0003_verificacion_email.up.sql — verificación de email en el registro

ALTER TABLE usuarios ADD COLUMN email_verificado BOOLEAN NOT NULL DEFAULT FALSE;

-- Las cuentas creadas antes de esta migración quedan verificadas: de lo
-- contrario, ningún usuario existente (incluido el admin) podría loguear.
UPDATE usuarios SET email_verificado = TRUE;

CREATE TABLE verificaciones_email (
    token             TEXT PRIMARY KEY,
    usuario_id        UUID NOT NULL UNIQUE REFERENCES usuarios(id) ON DELETE CASCADE,
    fecha_expiracion  TIMESTAMPTZ NOT NULL,
    fecha_creacion    TIMESTAMPTZ NOT NULL DEFAULT now()
);
