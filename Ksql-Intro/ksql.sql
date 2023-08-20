-- Crear el stream stock_updates en KLSQL
CREATE STREAM stock_updates (
symbol VARCHAR, 
price DOUBLE, 
volume DOUBLE, 
timestamp VARCHAR) 
WITH (
kafka_topic='stock-updates', 
value_format='json');

-- Consultar los datos del stream,
SELECT * FROM stock_updates;

-- Crear la tabla de stock_resume en KLSQL,
 CREATE TABLE stock_resume AS SELECT 
symbol AS simbolo, 
MAX(price) AS maximo, 
MIN(price) AS minimo,
SUM(price*volume)/SUM(volume) AS promedio,
COUNT(*) AS cantidad
FROM stock_updates 
GROUP BY symbol ;

-- Consultar la tabla de resumen,
SELECT * FROM stock_resume EMIT CHANGES;

-- Eliminar tabla
DROP TABLE stock_resume;

-- Eliminar el stream
DROP STREAM stock_updates;
