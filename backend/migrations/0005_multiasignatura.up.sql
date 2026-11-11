-- 0005_multiasignatura.up.sql — pruebas de Lectora, Historia y Ciencias; textos compartidos por varias preguntas; modo práctica

ALTER TYPE nivel ADD VALUE IF NOT EXISTS 'CL';
ALTER TYPE nivel ADD VALUE IF NOT EXISTS 'HCS';
ALTER TYPE nivel ADD VALUE IF NOT EXISTS 'CIENCIAS';

ALTER TYPE eje ADD VALUE IF NOT EXISTS 'localizar';
ALTER TYPE eje ADD VALUE IF NOT EXISTS 'interpretar';
ALTER TYPE eje ADD VALUE IF NOT EXISTS 'evaluar';
ALTER TYPE eje ADD VALUE IF NOT EXISTS 'historia';
ALTER TYPE eje ADD VALUE IF NOT EXISTS 'formacion_ciudadana';
ALTER TYPE eje ADD VALUE IF NOT EXISTS 'sistema_economico';
ALTER TYPE eje ADD VALUE IF NOT EXISTS 'biologia';
ALTER TYPE eje ADD VALUE IF NOT EXISTS 'fisica';
ALTER TYPE eje ADD VALUE IF NOT EXISTS 'quimica';

CREATE TABLE estimulos (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clave          TEXT UNIQUE,
    titulo         TEXT,
    texto          TEXT NOT NULL,
    imagen_url     TEXT,
    fuente         TEXT,
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE items ADD COLUMN estimulo_id UUID REFERENCES estimulos(id) ON DELETE SET NULL;
ALTER TABLE items ADD COLUMN orden_estimulo INT;
CREATE INDEX idx_items_estimulo ON items(estimulo_id);

ALTER TABLE ensayo_items ADD COLUMN revisada BOOLEAN NOT NULL DEFAULT FALSE;
