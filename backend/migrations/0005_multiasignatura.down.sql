-- 0005_multiasignatura.down.sql — los valores de los ENUM no se pueden quitar en PostgreSQL; se quitan tablas y columnas.

ALTER TABLE ensayo_items DROP COLUMN IF EXISTS revisada;
DROP INDEX IF EXISTS idx_items_estimulo;
ALTER TABLE items DROP COLUMN IF EXISTS orden_estimulo;
ALTER TABLE items DROP COLUMN IF EXISTS estimulo_id;
DROP TABLE IF EXISTS estimulos;
