-- 0004_alternativa_e.down.sql — PostgreSQL no permite quitar un valor de un ENUM; se eliminan los datos que lo usan y el tipo conserva 'E'.

UPDATE ensayo_items SET respuesta_seleccionada = NULL WHERE respuesta_seleccionada = 'E';
DELETE FROM alternativas WHERE etiqueta = 'E';
