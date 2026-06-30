-- 0001_init.up.sql — esquema inicial MVP Ensayos PAES

CREATE TYPE rol AS ENUM ('estudiante', 'profesor', 'admin');
CREATE TYPE nivel AS ENUM ('M1', 'M2');
CREATE TYPE eje AS ENUM ('numeros', 'algebra_funciones', 'geometria', 'probabilidad_estadistica');
CREATE TYPE dificultad AS ENUM ('baja', 'media', 'alta');
CREATE TYPE origen_item AS ENUM ('oficial', 'generado');
CREATE TYPE estado_item AS ENUM ('borrador', 'publicado', 'oculto');
CREATE TYPE tipo_examen AS ENUM ('PAES_Regular', 'PAES_Invierno', 'PDT');
CREATE TYPE etiqueta_alt AS ENUM ('A', 'B', 'C', 'D');
CREATE TYPE estado_ensayo AS ENUM ('en_progreso', 'finalizado');

CREATE TABLE usuarios (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre          TEXT NOT NULL,
    email           TEXT NOT NULL UNIQUE,
    password_hash   TEXT NOT NULL,
    rol             rol  NOT NULL,
    activo          BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE grupos (
    id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre             TEXT NOT NULL,
    profesor_id        UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    codigo_invitacion  TEXT NOT NULL UNIQUE,
    fecha_creacion     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE grupo_miembros (
    grupo_id      UUID NOT NULL REFERENCES grupos(id) ON DELETE CASCADE,
    estudiante_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    fecha_union   TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (grupo_id, estudiante_id)
);
CREATE INDEX idx_grupo_miembros_estudiante ON grupo_miembros(estudiante_id);

CREATE TABLE examenes_fuente (
    id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre             TEXT NOT NULL,
    anio_admision      INT  NOT NULL,
    tipo               tipo_examen NOT NULL,
    nivel              nivel NOT NULL,
    edicion            TEXT,
    url_pdf            TEXT,
    fecha_publicacion  DATE
);

CREATE TABLE items (
    id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    examen_fuente_id   UUID REFERENCES examenes_fuente(id) ON DELETE SET NULL,
    enunciado          TEXT NOT NULL,
    imagen_url         TEXT,
    eje                eje NOT NULL,
    nivel              nivel NOT NULL,
    dificultad         dificultad NOT NULL,
    origen             origen_item NOT NULL DEFAULT 'oficial',
    estado             estado_item NOT NULL DEFAULT 'borrador',
    peso               INT,
    explicacion        TEXT,
    fecha_creacion     TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_items_seleccion ON items(estado, nivel, eje);
CREATE INDEX idx_items_examen ON items(examen_fuente_id);

CREATE TABLE alternativas (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    item_id     UUID NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    etiqueta    etiqueta_alt NOT NULL,
    texto       TEXT NOT NULL,
    imagen_url  TEXT,
    es_correcta BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (item_id, etiqueta)
);
CREATE INDEX idx_alternativas_item ON alternativas(item_id);

CREATE TABLE ensayos (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    estudiante_id     UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    nivel             nivel NOT NULL,
    ejes              eje[] NOT NULL,
    cantidad          INT NOT NULL,
    modo              TEXT NOT NULL DEFAULT 'libre',
    estado            estado_ensayo NOT NULL DEFAULT 'en_progreso',
    fecha_inicio      TIMESTAMPTZ NOT NULL DEFAULT now(),
    fecha_fin         TIMESTAMPTZ,
    puntaje           INT,
    puntos_obtenidos  INT,
    puntos_posibles   INT,
    correctas         INT,
    total             INT
);
CREATE INDEX idx_ensayos_estudiante ON ensayos(estudiante_id, fecha_fin);

CREATE TABLE ensayo_items (
    id                     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ensayo_id              UUID NOT NULL REFERENCES ensayos(id) ON DELETE CASCADE,
    item_id                UUID NOT NULL REFERENCES items(id),
    orden                  INT NOT NULL,
    peso_snapshot          INT NOT NULL,
    respuesta_seleccionada etiqueta_alt,
    es_correcta            BOOLEAN,
    UNIQUE (ensayo_id, item_id)
);
CREATE INDEX idx_ensayo_items_ensayo ON ensayo_items(ensayo_id);
