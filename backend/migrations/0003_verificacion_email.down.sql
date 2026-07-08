-- 0003_verificacion_email.down.sql

DROP TABLE verificaciones_email;
ALTER TABLE usuarios DROP COLUMN email_verificado;
