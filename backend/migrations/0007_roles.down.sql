ALTER TABLE usuarios DROP COLUMN institucion_id;
DROP TABLE instituciones;
DROP TABLE apoderado_estudiantes;
DROP TABLE codigos_apoderado;
-- Los valores 'apoderado', 'institucion' y 'editor' del enum rol quedan: PostgreSQL no permite quitarlos.
