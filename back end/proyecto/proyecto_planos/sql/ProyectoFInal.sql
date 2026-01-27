ALTER SESSION SET CONTAINER = FREEPDB1;

-- Borrado de tablas en orden inverso para evitar errores de claves foráneas
DROP TABLE Suscripciones CASCADE CONSTRAINTS;
DROP TABLE Planos CASCADE CONSTRAINTS;
DROP TABLE Clientes CASCADE CONSTRAINTS;
DROP TABLE Arquitectos CASCADE CONSTRAINTS;

-- 1. Tabla de Arquitectos (Usuarios en tu documento)
CREATE TABLE Arquitectos (
    Dni VARCHAR2(9) PRIMARY KEY,
    Nombre VARCHAR2(100) NOT NULL,
    Apellidos VARCHAR2(150) NOT NULL,
    Telefono VARCHAR2(20),
    Correo_electronico VARCHAR2(100) UNIQUE NOT NULL,
    Cuenta_bancaria VARCHAR2(24) NOT NULL
);

-- 2. Tabla de Clientes (Relacionada con el Arquitecto responsable)
CREATE TABLE Clientes (
    Nif VARCHAR2(9) PRIMARY KEY,
    Nom_empresa VARCHAR2(200) NOT NULL UNIQUE,
    Telefono VARCHAR2(20),
    Correo_electronico VARCHAR2(100) NOT NULL,
    Cuenta_bancaria VARCHAR2(24) NOT NULL,
    Dni_usuario VARCHAR2(9), 
    CONSTRAINT fk_cliente_arquitecto FOREIGN KEY (Dni_usuario) REFERENCES Arquitectos(Dni) ON DELETE SET NULL
);

-- 3. Tabla de Planos (Relacionada con el Arquitecto que los calcula)
CREATE TABLE Planos (
    Id_plano NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    Tamano NUMBER(10,2) NOT NULL,
    Formato VARCHAR2(50) NOT NULL,
    Fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Fecha_entrega DATE NOT NULL,
    Dni_usuario VARCHAR2(9) NOT NULL,
    CONSTRAINT fk_plano_arquitecto FOREIGN KEY (Dni_usuario) REFERENCES Arquitectos(Dni)
);

-- 4. Tabla de Suscripciones (Relacionada con el Cliente)
CREATE TABLE Suscripciones (
    Id_suscripcion NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    Tipo_suscripcion VARCHAR2(50) NOT NULL,
    Precio NUMBER(10,2) NOT NULL,
    Nif_cliente VARCHAR2(9) NOT NULL,
    CONSTRAINT fk_suscripcion_cliente FOREIGN KEY (Nif_cliente) REFERENCES Clientes(Nif)
);


SHOW USER;