-- ==============================================================================
-- SISTEMA DE GESTIÓN OPERATIVA - PARQUEADERO AUTOS COLOMBIA
-- Script DDL de Creación de Base de Datos y Tablas (MySQL 8.x)
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS parqueadero_autos_colombia
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE parqueadero_autos_colombia;

-- Desactivar temporalmente chequeo de llaves foráneas para orden de creación
SET FOREIGN_KEY_CHECKS = 0;

-- ------------------------------------------------------------------------------
-- 1. TABLA: usuarios (Administradores, Operarios de caseta y Clientes)
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS novedades;
DROP TABLE IF EXISTS movimientos;
DROP TABLE IF EXISTS pagos_mensualidad;
DROP TABLE IF EXISTS mensualidades;
DROP TABLE IF EXISTS celdas;
DROP TABLE IF EXISTS vehiculos;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    documento_identidad VARCHAR(20) NOT NULL UNIQUE,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    rol ENUM('ADMIN', 'OPERARIO', 'CLIENTE') NOT NULL DEFAULT 'CLIENTE',
    password_hash VARCHAR(255) NOT NULL,
    estado ENUM('ACTIVO', 'INACTIVO') NOT NULL DEFAULT 'ACTIVO',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_usuarios_documento (documento_identidad),
    INDEX idx_usuarios_rol (rol)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- 2. TABLA: vehiculos
-- ------------------------------------------------------------------------------
CREATE TABLE vehiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(10) NOT NULL UNIQUE,
    tipo_vehiculo ENUM('CARRO', 'MOTO', 'CAMIONETA', 'ESPECIAL') NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NULL,
    color VARCHAR(30) NOT NULL,
    cliente_id INT NOT NULL,
    estado_actual ENUM('DENTRO', 'FUERA') NOT NULL DEFAULT 'FUERA',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_vehiculos_cliente FOREIGN KEY (cliente_id) 
        REFERENCES usuarios (id) ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX idx_vehiculos_placa (placa),
    INDEX idx_vehiculos_estado (estado_actual)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- 3. TABLA: celdas (Espacios de parqueo)
-- ------------------------------------------------------------------------------
CREATE TABLE celdas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(10) NOT NULL UNIQUE,
    tipo_permitido ENUM('CARRO', 'MOTO', 'CAMIONETA', 'ESPECIAL') NOT NULL,
    estado ENUM('DISPONIBLE', 'OCUPADA', 'MANTENIMIENTO', 'RESERVADA') NOT NULL DEFAULT 'DISPONIBLE',
    zona_piso VARCHAR(50) NOT NULL DEFAULT 'Piso 1',
    observaciones VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_celdas_codigo (codigo),
    INDEX idx_celdas_estado_tipo (estado, tipo_permitido)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- 4. TABLA: mensualidades (Contratos suscritos)
-- ------------------------------------------------------------------------------
CREATE TABLE mensualidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_contrato VARCHAR(30) NOT NULL UNIQUE,
    cliente_id INT NOT NULL,
    vehiculo_id INT NOT NULL,
    celda_preferida_id INT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    valor_mensual DECIMAL(10, 2) NOT NULL,
    estado ENUM('ACTIVA', 'VENCIDA', 'CANCELADA', 'PENDIENTE_PAGO') NOT NULL DEFAULT 'ACTIVA',
    observaciones TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_mensualidades_cliente FOREIGN KEY (cliente_id) 
        REFERENCES usuarios (id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_mensualidades_vehiculo FOREIGN KEY (vehiculo_id) 
        REFERENCES vehiculos (id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_mensualidades_celda FOREIGN KEY (celda_preferida_id) 
        REFERENCES celdas (id) ON UPDATE CASCADE ON DELETE SET NULL,
    INDEX idx_mensualidades_fechas (fecha_inicio, fecha_fin),
    INDEX idx_mensualidades_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- 5. TABLA: pagos_mensualidad
-- ------------------------------------------------------------------------------
CREATE TABLE pagos_mensualidad (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mensualidad_id INT NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    fecha_pago DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    metodo_pago ENUM('EFECTIVO', 'TRANSFERENCIA', 'TARJETA') NOT NULL,
    referencia_comprobante VARCHAR(100) NULL,
    operario_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pagos_mensualidad FOREIGN KEY (mensualidad_id) 
        REFERENCES mensualidades (id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_pagos_operario FOREIGN KEY (operario_id) 
        REFERENCES usuarios (id) ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX idx_pagos_fecha (fecha_pago)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- 6. TABLA: movimientos (Entradas y Salidas de vehículos)
-- ------------------------------------------------------------------------------
CREATE TABLE movimientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehiculo_id INT NOT NULL,
    celda_id INT NOT NULL,
    operario_entrada_id INT NOT NULL,
    operario_salida_id INT NULL,
    fecha_hora_entrada DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_hora_salida DATETIME NULL,
    estado ENUM('ACTIVO', 'FINALIZADO') NOT NULL DEFAULT 'ACTIVO',
    kilometraje_entrada INT NULL,
    kilometraje_salida INT NULL,
    observaciones TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_movimientos_vehiculo FOREIGN KEY (vehiculo_id) 
        REFERENCES vehiculos (id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_movimientos_celda FOREIGN KEY (celda_id) 
        REFERENCES celdas (id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_movimientos_op_entrada FOREIGN KEY (operario_entrada_id) 
        REFERENCES usuarios (id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_movimientos_op_salida FOREIGN KEY (operario_salida_id) 
        REFERENCES usuarios (id) ON UPDATE CASCADE ON DELETE SET NULL,
    INDEX idx_movimientos_estado_vehiculo (estado, vehiculo_id),
    INDEX idx_movimientos_celda_estado (celda_id, estado),
    INDEX idx_movimientos_fechas (fecha_hora_entrada, fecha_hora_salida)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- 7. TABLA: novedades (Golpes, rayones, incidentes)
-- ------------------------------------------------------------------------------
CREATE TABLE novedades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movimiento_id INT NULL,
    vehiculo_id INT NOT NULL,
    tipo_novedad ENUM('RAYON', 'GOLPE', 'ESPEJO_ROTO', 'OBJETOS_VALOR', 'MECANICA', 'OTRO') NOT NULL,
    severidad ENUM('LEVE', 'MODERADA', 'GRAVE') NOT NULL DEFAULT 'LEVE',
    descripcion TEXT NOT NULL,
    evidencia_url VARCHAR(255) NULL,
    registrado_por_id INT NOT NULL,
    momento ENUM('ENTRADA', 'SALIDA', 'PERMANENCIA') NOT NULL DEFAULT 'ENTRADA',
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_novedades_movimiento FOREIGN KEY (movimiento_id) 
        REFERENCES movimientos (id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_novedades_vehiculo FOREIGN KEY (vehiculo_id) 
        REFERENCES vehiculos (id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_novedades_registrador FOREIGN KEY (registrado_por_id) 
        REFERENCES usuarios (id) ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX idx_novedades_vehiculo (vehiculo_id),
    INDEX idx_novedades_fecha (fecha_registro)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
