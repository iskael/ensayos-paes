-- 0006_estimulos_editables.up.sql — los textos de Lectora se editan desde el banco

ALTER TABLE estimulos ADD COLUMN nivel nivel;
ALTER TABLE estimulos ADD COLUMN fecha_edicion TIMESTAMPTZ;

UPDATE estimulos e SET nivel = (SELECT i.nivel FROM items i WHERE i.estimulo_id = e.id LIMIT 1);
