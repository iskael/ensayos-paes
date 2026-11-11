-- 0007_roles.up.sql — apoderados que siguen a un estudiante, instituciones que agrupan profesores y editores del banco

ALTER TYPE rol ADD VALUE IF NOT EXISTS 'apoderado';
ALTER TYPE rol ADD VALUE IF NOT EXISTS 'institucion';
ALTER TYPE rol ADD VALUE IF NOT EXISTS 'editor';

CREATE TABLE codigos_apoderado (
    estudiante_id UUID PRIMARY KEY REFERENCES usuarios(id) ON DELETE CASCADE,
    codigo        TEXT NOT NULL UNIQUE,
    expira_en     TIMESTAMPTZ NOT NULL
);

CREATE TABLE apoderado_estudiantes (
    apoderado_id  UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    estudiante_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    fecha_vinculo TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (apoderado_id, estudiante_id)
);
CREATE INDEX idx_apoderado_estudiantes_estudiante ON apoderado_estudiantes(estudiante_id);

CREATE TABLE instituciones (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre            TEXT NOT NULL,
    responsable_id    UUID NOT NULL UNIQUE REFERENCES usuarios(id) ON DELETE CASCADE,
    codigo_invitacion TEXT NOT NULL UNIQUE,
    fecha_creacion    TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE usuarios ADD COLUMN institucion_id UUID REFERENCES instituciones(id) ON DELETE SET NULL;
CREATE INDEX idx_usuarios_institucion ON usuarios(institucion_id);
