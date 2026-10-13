# Modelado de Datos - Parqueadero Autos Colombia (Iteración 1)

Este documento detalla el diseño de la capa de persistencia para el sistema, adaptado específicamente al motor de base de datos **MySQL 8.x**. Incluye el Modelo Entidad-Relación (MER), el Modelo Relacional (MR) normalizado en Tercera Forma Normal (3FN), el diccionario de datos y las consideraciones de integridad.

---

## 1. Modelo Entidad-Relación (MER)

A continuación se presenta el diagrama Entidad-Relación mediante notación Mermaid (Crow's Foot):

```mermaid
erDiagram
    USUARIOS ||--o{ VEHICULOS : "posee"
    USUARIOS ||--o{ MENSUALIDADES : "suscribe"
    USUARIOS ||--o{ MOVIMIENTOS : "registra_entrada"
    USUARIOS ||--o{ NOVEDADES : "reporta"
    
    VEHICULOS ||--o{ MENSUALIDADES : "asociado_a"
    VEHICULOS ||--o{ MOVIMIENTOS : "realiza"
    VEHICULOS ||--o{ NOVEDADES : "presenta"
    
    CELDAS ||--o{ MENSUALIDADES : "asignada_fija"
    CELDAS ||--o{ MOVIMIENTOS : "alberga"
    
    MENSUALIDADES ||--o{ PAGOS_MENSUALIDAD : "genera"
    
    MOVIMIENTOS ||--o{ NOVEDADES : "asocia_durante"

    USUARIOS {
        int id PK
        varchar documento_identidad UK
        varchar nombres
        varchar apellidos
        varchar telefono
        varchar email UK
        enum rol
        varchar password_hash
        enum estado
        datetime created_at
    }

    VEHICULOS {
        int id PK
        varchar placa UK
        enum tipo_vehiculo
        varchar marca
        varchar modelo
        varchar color
        int cliente_id FK
        enum estado_actual
        datetime created_at
    }

    CELDAS {
        int id PK
        varchar codigo UK
        enum tipo_permitido
        enum estado
        varchar zona_piso
        varchar observaciones
    }

    MENSUALIDADES {
        int id PK
        varchar codigo_contrato UK
        int cliente_id FK
        int vehiculo_id FK
        int celda_preferida_id FK
        date fecha_inicio
        date fecha_fin
        decimal valor_mensual
        enum estado
        datetime created_at
    }

    PAGOS_MENSUALIDAD {
        int id PK
        int mensualidad_id FK
        decimal monto
        datetime fecha_pago
        enum metodo_pago
        varchar referencia_comprobante
        int operario_id FK
        datetime created_at
    }

    MOVIMIENTOS {
        int id PK
        int vehiculo_id FK
        int celda_id FK
        int operario_entrada_id FK
        int operario_salida_id FK
        datetime fecha_hora_entrada
        datetime fecha_hora_salida
        enum estado
        varchar observaciones
        datetime created_at
    }

    NOVEDADES {
        int id PK
        int movimiento_id FK
        int vehiculo_id FK
        enum tipo_novedad
        enum severidad
        text descripcion
        varchar evidencia_url
        int registrado_por_id FK
        enum momento
        datetime fecha_registro
    }
```

---

## 2. Modelo Relacional (MR) Normalizado (3FN)

A continuación se listan las relaciones en formato esquemático formal, destacando Llaves Primarias (**PK**), Llaves Foráneas (**FK**) y Claves Únicas (**UK**):

1. **`usuarios`** (  
   **id** [PK],  
   documento_identidad [UK],  
   nombres, apellidos, telefono, email [UK],  
   rol, password_hash, estado, created_at, updated_at  
)

2. **`vehiculos`** (  
   **id** [PK],  
   placa [UK],  
   tipo_vehiculo, marca, modelo, color,  
   **cliente_id** [FK -> usuarios.id],  
   estado_actual, created_at, updated_at  
)

3. **`celdas`** (  
   **id** [PK],  
   codigo [UK],  
   tipo_permitido, estado, zona_piso, observaciones, created_at, updated_at  
)

4. **`mensualidades`** (  
   **id** [PK],  
   codigo_contrato [UK],  
   **cliente_id** [FK -> usuarios.id],  
   **vehiculo_id** [FK -> vehiculos.id],  
   **celda_preferida_id** [FK -> celdas.id, NULLable],  
   fecha_inicio, fecha_fin, valor_mensual, estado, observaciones, created_at, updated_at  
)

5. **`pagos_mensualidad`** (  
   **id** [PK],  
   **mensualidad_id** [FK -> mensualidades.id],  
   monto, fecha_pago, metodo_pago, referencia_comprobante,  
   **operario_id** [FK -> usuarios.id],  
   created_at  
)

6. **`movimientos`** (  
   **id** [PK],  
   **vehiculo_id** [FK -> vehiculos.id],  
   **celda_id** [FK -> celdas.id],  
   **operario_entrada_id** [FK -> usuarios.id],  
   **operario_salida_id** [FK -> usuarios.id, NULLable],  
   fecha_hora_entrada, fecha_hora_salida [NULLable],  
   estado, observaciones, created_at, updated_at  
)

7. **`novedades`** (  
   **id** [PK],  
   **movimiento_id** [FK -> movimientos.id],  
   **vehiculo_id** [FK -> vehiculos.id],  
   tipo_novedad, severidad, descripcion, evidencia_url [NULLable],  
   **registrado_por_id** [FK -> usuarios.id],  
   momento, fecha_registro  
)

---

## 3. Justificación de Normalización (Formas Normales)

- **Primera Forma Normal (1FN):**
  - Todos los atributos son atómicos (nombres y apellidos separados, tipos parametrizados en enumeraciones, valores indivisibles). Cada tabla tiene su respectiva clave primaria `id`.
- **Segunda Forma Normal (2FN):**
  - Todas las tablas poseen claves primarias simples (`id` autoincremental). No existen dependencias funcionales parciales con respecto a llaves compuestas.
- **Tercera Forma Normal (3FN):**
  - Se eliminan las dependencias transitivas. Por ejemplo, los datos del cliente no se almacenan repetidos en `movimientos` ni en `mensualidades`, sino que se referencian a través de `cliente_id` hacia la tabla `usuarios`. Las celdas poseen su propia entidad independiente para controlar su disponibilidad global.

---

## 4. Índices y Estrategia de Rendimiento en MySQL

Para garantizar tiempos de respuesta menores a 500 ms (RNF-01), se definen los siguientes índices:
1. `idx_vehiculos_placa` en `vehiculos(placa)`: Búsqueda inmediata en caseta.
2. `idx_movimientos_estado` en `movimientos(estado, vehiculo_id)`: Consulta instantánea para verificar si un vehículo está actualmente dentro (regla anti-passback).
3. `idx_celdas_estado` en `celdas(estado, tipo_permitido)`: Búsqueda rápida de celdas disponibles por tipo.
4. `idx_mensualidades_fechas` en `mensualidades(vehiculo_id, fecha_fin, estado)`: Verificación rápida de mensualidades activas.
