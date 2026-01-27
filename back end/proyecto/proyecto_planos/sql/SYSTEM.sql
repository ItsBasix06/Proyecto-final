-- Contenido del archivo SYSTEM.sql adaptado para Ubuntu 25.04 con Oracle 23c Free
-- Ejecutar como SYS (sqlplus / as sysdba)
-- Asegúrate de crear la carpeta: sudo mkdir -p /opt/oracle/oradata/FREE/bdies
-- y permisos: sudo chown -R oracle:oinstall /opt/oracle/oradata/FREE/bdies

-- Verificar contenedor actual
SHOW CON_NAME;

-- Cambiar a la PDB (ajusta si tu PDB es diferente, e.g., FREEPDB1)
ALTER SESSION SET CONTAINER=FREEPDB1;

-- Obtener información sobre tablespaces y datafiles
SELECT file_name, file_id, blocks, tablespace_name, bytes FROM dba_data_files;

-- Crear un tablespace
CREATE TABLESPACE admin
DATAFILE '/opt/oracle/oradata/FREE/admin/admin01.dbf' SIZE 100M
AUTOEXTEND ON NEXT 50M MAXSIZE 1G;

-- Crear un tablespace temporal
CREATE TEMPORARY TABLESPACE admin_01_temp
TEMPFILE '/opt/oracle/oradata/FREE/admin/admin_01_temp.dbf'
SIZE 100M;

-- Redimensionar un tablespace: Añadir datafile
ALTER TABLESPACE bdies
ADD DATAFILE '/opt/oracle/oradata/FREE/bdies/bdies_02.dbf' SIZE 100M;

-- Redimensionar un tablespace: Resize datafile
ALTER DATABASE
DATAFILE '/opt/oracle/oradata/FREE/bdies/bdies_01.dbf' RESIZE 400M;

-- Borrar un tablespace
DROP TABLESPACE bdies
INCLUDING CONTENTS AND DATAFILES CASCADE CONSTRAINTS;

-- Borrar un datafile
ALTER TABLESPACE bdies
DROP DATAFILE '/opt/oracle/oradata/FREE/bdies/bdies_02.dbf';

-- Crear el usuario 'admin' con contraseña, tablespace default y quota ilimitada

CREATE USER admin IDENTIFIED BY "1528Jav992#$"
DEFAULT TABLESPACE admin 
QUOTA UNLIMITED ON admin
TEMPORARY TABLESPACE admin_01_temp;
GRANT DBA TO admin;