-- 0002_terminos.up.sql — historial de aceptación de Términos y Condiciones

CREATE TABLE terminos_aceptados (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id       UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    version          TEXT NOT NULL,
    fecha_aceptacion TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_terminos_aceptados_usuario ON terminos_aceptados(usuario_id);
