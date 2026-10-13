-- ==============================================================================
-- SISTEMA DE GESTIÓN OPERATIVA - PARQUEADERO AUTOS COLOMBIA
-- Script de Datos Semilla (Seed Data) para Pruebas
-- ==============================================================================

USE parqueadero_autos_colombia;

-- 1. Usuarios: Administrador, Operarios y Clientes
INSERT INTO usuarios (id, documento_identidad, nombres, apellidos, telefono, email, rol, password_hash, estado) VALUES
(1, '1020304050', 'Carlos', 'Gómez', '3001234567', 'admin@autoscolombia.com', 'ADMIN', '$2b$12$e80MvK2iL4h8D7Oa8XvQde7zR8m5V3p1N5e7G6k0pL9qW4z8y1B2a', 'ACTIVO'),
(2, '1030405060', 'Andrés', 'López', '3109876543', 'operario1@autoscolombia.com', 'OPERARIO', '$2b$12$e80MvK2iL4h8D7Oa8XvQde7zR8m5V3p1N5e7G6k0pL9qW4z8y1B2a', 'ACTIVO'),
(3, '1040506070', 'Laura', 'Martínez', '3157654321', 'operario2@autoscolombia.com', 'OPERARIO', '$2b$12$e80MvK2iL4h8D7Oa8XvQde7zR8m5V3p1N5e7G6k0pL9qW4z8y1B2a', 'ACTIVO'),
(4, '71234567', 'Mauricio', 'Restrepo', '3201122334', 'mauricio.restrepo@gmail.com', 'CLIENTE', '', 'ACTIVO'),
(5, '43567890', 'Camila', 'Fernández', '3004455667', 'camila.fernandez@outlook.com', 'CLIENTE', '', 'ACTIVO'),
(6, '98765432', 'Javier', 'Vargas', '3118899001', 'javier.vargas@yahoo.com', 'CLIENTE', '', 'ACTIVO');

-- 2. Celdas de Parqueo
INSERT INTO celdas (id, codigo, tipo_permitido, estado, zona_piso, observaciones) VALUES
(1, 'A-01', 'CARRO', 'DISPONIBLE', 'Piso 1 - Zona Norte', 'Cerca a la entrada principal'),
(2, 'A-02', 'CARRO', 'DISPONIBLE', 'Piso 1 - Zona Norte', 'Celda estándar'),
(3, 'A-03', 'CARRO', 'DISPONIBLE', 'Piso 1 - Zona Norte', 'Celda estándar'),
(4, 'A-04', 'CARRO', 'DISPONIBLE', 'Piso 1 - Zona Norte', 'Celda estándar'),
(5, 'A-05', 'CARRO', 'MANTENIMIENTO', 'Piso 1 - Zona Norte', 'Pintura y demarcación en proceso'),
(6, 'B-01', 'CAMIONETA', 'DISPONIBLE', 'Piso 1 - Zona Sur', 'Espacio amplio para SUV o Camioneta'),
(7, 'B-02', 'CAMIONETA', 'DISPONIBLE', 'Piso 1 - Zona Sur', 'Espacio amplio'),
(8, 'M-01', 'MOTO', 'DISPONIBLE', 'Piso 1 - Zona Motos', 'Bahía techada'),
(9, 'M-02', 'MOTO', 'DISPONIBLE', 'Piso 1 - Zona Motos', 'Bahía techada'),
(10, 'E-01', 'ESPECIAL', 'DISPONIBLE', 'Piso 1 - Zona Accesible', 'Celda para personas con movilidad reducida');

-- 3. Vehículos
INSERT INTO vehiculos (id, placa, tipo_vehiculo, marca, modelo, color, cliente_id, estado_actual) VALUES
(1, 'HJR542', 'CARRO', 'Mazda', 'Mazda 3 2021', 'Rojo Diamante', 4, 'FUERA'),
(2, 'TKL890', 'CARRO', 'Renault', 'Duster 2020', 'Gris Estrella', 5, 'FUERA'),
(3, 'WXY12C', 'MOTO', 'Yamaha', 'MT-03 2022', 'Negro Mate', 6, 'FUERA'),
(4, 'QWE345', 'CARRO', 'Chevrolet', 'Onix 2019', 'Blanco', 4, 'FUERA');

-- 4. Mensualidades
-- Mensualidad 1: Activa y vigente (Mauricio - HJR542)
INSERT INTO mensualidades (id, codigo_contrato, cliente_id, vehiculo_id, celda_preferida_id, fecha_inicio, fecha_fin, valor_mensual, estado, observaciones) VALUES
(1, 'CTR-2026-001', 4, 1, 1, '2026-10-01', '2026-11-01', 180000.00, 'ACTIVA', 'Contrato mensual estándar diurno y nocturno');

-- Mensualidad 2: Próxima a vencer en pocos días (Camila - TKL890)
INSERT INTO mensualidades (id, codigo_contrato, cliente_id, vehiculo_id, celda_preferida_id, fecha_inicio, fecha_fin, valor_mensual, estado, observaciones) VALUES
(2, 'CTR-2026-002', 5, 2, 6, '2026-09-16', '2026-10-16', 220000.00, 'ACTIVA', 'Camioneta zona sur');

-- Mensualidad 3: Vencida (Javier - WXY12C)
INSERT INTO mensualidades (id, codigo_contrato, cliente_id, vehiculo_id, celda_preferida_id, fecha_inicio, fecha_fin, valor_mensual, estado, observaciones) VALUES
(3, 'CTR-2026-003', 6, 3, 8, '2026-09-01', '2026-10-01', 80000.00, 'VENCIDA', 'Pendiente pago de renovación de octubre');

-- 5. Pagos Registrados
INSERT INTO pagos_mensualidad (id, mensualidad_id, monto, fecha_pago, metodo_pago, referencia_comprobante, operario_id) VALUES
(1, 1, 180000.00, '2026-10-01 08:30:00', 'TRANSFERENCIA', 'NEQUI-TRX-998822', 2),
(2, 2, 220000.00, '2026-09-16 09:15:00', 'EFECTIVO', 'REC-CAJA-00431', 2);
