# Diseño de Arquitectura y Diagramas UML
## Proyecto: Parqueadero Autos Colombia - Iteración 1

Este documento define la arquitectura general del sistema y proporciona las especificaciones para los diagramas UML requeridos (Casos de Uso, Diagrama de Clases y Diagrama de Paquetes), acompañados de sus representaciones gráficas en Mermaid y la guía paso a paso para su modelado en la herramienta **StarUML**.

---

## 1. Especificación de la Arquitectura del Sistema

El sistema implementa una **Arquitectura en Capas (Layered / Clean Architecture adaptada)**, desacoplando la interfaz de usuario del backend mediante servicios REST y aislando la persistencia de datos:

```
┌────────────────────────────────────────────────────────┐
│             CAPA DE PRESENTACIÓN (FRONTEND)            │
│   React + Vite SPA | Hooks de Estado | CSS Moderno     │
└───────────────────────────┬────────────────────────────┘
                            │ JSON / HTTP REST API
┌───────────────────────────▼────────────────────────────┐
│              CAPA DE CONTROLADORES (ROUTERS)           │
│   FastAPI APIRouters | Validación Pydantic Schemas     │
├────────────────────────────────────────────────────────┤
│              CAPA DE SERVICIOS (LÓGICA DE NEGOCIO)     │
│   Validación de Mensualidad | Anti-passback | Reglas    │
├────────────────────────────────────────────────────────┤
│              CAPA DE REPOSITORIOS / PERSISTENCIA       │
│   SQLAlchemy 2.0 ORM | Transacciones ACID | Sesiones    │
└───────────────────────────┬────────────────────────────┘
                            │ Conexión TCP / PyMySQL
┌───────────────────────────▼────────────────────────────┐
│             CAPA DE BASE DE DATOS (MOTOR RELACIONAL)   │
│   MySQL 8.x (InnoDB, Constraints, Triggers/Índices)    │
└────────────────────────────────────────────────────────┘
```

---

## 2. Diagrama de Casos de Uso (UML)

### 2.1. Representación en Mermaid
```mermaid
graph LR
    Operario((Operario de Caseta))
    Admin((Administrador))
    Sistema((Sistema / Cron))

    UC01[Consultar Placa y Mensualidad]
    UC02[Registrar Entrada de Vehículo]
    UC03[Asignar Celda de Parqueo]
    UC04[Registrar Novedad Física]
    UC05[Registrar Salida de Vehículo]
    UC06[Liberar Celda]
    UC07[Monitorear Aforo y Celdas]
    UC08[Alertar Vencimiento Mensualidad]

    Operario --> UC01
    Operario --> UC02
    Operario --> UC05
    Operario --> UC07

    Admin --> UC07
    Admin --> UC08

    UC02 -.->|<<include>>| UC01
    UC02 -.->|<<include>>| UC03
    UC02 -.->|<<extend>>| UC04
    UC05 -.->|<<include>>| UC06
    UC01 -.->|<<extend>>| UC08
```

### 2.2. Guía para Modelar en StarUML:
1. Abrir **StarUML** -> Menú `Model` -> `Add Diagram` -> `Use Case Diagram`.
2. Desde la barra de herramientas lateral (*Toolbox*), arrastrar 2 actores (`Actor`):
   - **Operario de Caseta**
   - **Administrador**
3. Arrastrar los casos de uso (`UseCase`) y nombrarlos:
   - `CU-01: Validar Placa y Mensualidad`
   - `CU-02: Registrar Entrada de Vehículo`
   - `CU-03: Asignar Celda`
   - `CU-04: Registrar Novedad Física`
   - `CU-05: Registrar Salida de Vehículo`
   - `CU-06: Liberar Celda de Parqueo`
   - `CU-07: Monitorear Tablero de Celdas`
4. Crear relaciones:
   - `Association` desde los actores hacia los Casos de Uso correspondientes.
   - `Include` desde `Registrar Entrada` hacia `Validar Placa` y hacia `Asignar Celda`.
   - `Extend` desde `Registrar Novedad` hacia `Registrar Entrada` (condición: daño visible).
   - `Include` desde `Registrar Salida` hacia `Liberar Celda`.

---

## 3. Diagrama de Clases del Dominio (UML)

### 3.1. Representación en Mermaid
```mermaid
classDiagram
    class Usuario {
        +int id
        +string documentoIdentidad
        +string nombres
        +string apellidos
        +string telefono
        +string email
        +Rol rol
        +string passwordHash
        +EstadoUsuario estado
        +autenticar(credenciales) bool
        +cambiarEstado(nuevoEstado) void
    }

    class Vehiculo {
        +int id
        +string placa
        +TipoVehiculo tipo
        +string marca
        +string modelo
        +string color
        +int clienteId
        +EstadoVehiculo estadoActual
        +validarPlacaFormato() bool
        +cambiarEstadoTransito(nuevoEstado) void
    }

    class Celda {
        +int id
        +string codigo
        +TipoVehiculo tipoPermitido
        +EstadoCelda estado
        +string zonaPiso
        +ocupar() void
        +liberar() void
        +estaDisponible() bool
    }

    class Mensualidad {
        +int id
        +string codigoContrato
        +int clienteId
        +int vehiculoId
        +date fechaInicio
        +date fechaFin
        +float valorMensual
        +EstadoMensualidad estado
        +esVigente() bool
        +diasParaVencer() int
    }

    class Movimiento {
        +int id
        +int vehiculoId
        +int celdaId
        +int operarioEntradaId
        +int operarioSalidaId
        +datetime fechaHoraEntrada
        +datetime fechaHoraSalida
        +EstadoMovimiento estado
        +registrarSalida(operarioId) void
        +calcularTiempoEstadia() string
    }

    class Novedad {
        +int id
        +int movimientoId
        +int vehiculoId
        +TipoNovedad tipo
        +Severidad severidad
        +string descripcion
        +string evidenciaUrl
        +MomentoNovedad momento
        +datetime fechaRegistro
    }

    Usuario "1" --> "0..*" Vehiculo : posee
    Usuario "1" --> "0..*" Mensualidad : suscribe
    Vehiculo "1" --> "0..*" Mensualidad : amparado_por
    Vehiculo "1" --> "0..*" Movimiento : genera
    Celda "1" --> "0..*" Movimiento : aloja
    Movimiento "1" --> "0..*" Novedad : contiene
    Usuario "1" --> "0..*" Movimiento : atiende_entrada
```

### 3.2. Guía para Modelar en StarUML:
1. Menú `Model` -> `Add Diagram` -> `Class Diagram`.
2. Arrastrar elementos `Class` desde el Toolbox para cada entidad:
   - `Usuario`, `Vehiculo`, `Celda`, `Mensualidad`, `Movimiento`, `Novedad`.
3. Para cada clase, hacer clic derecho -> `Add Attribute` para agregar los campos con visibilidad (`+` Public, `-` Private) y tipo de dato.
4. Clic derecho -> `Add Operation` para agregar los métodos de dominio (ej. `esVigente()`, `ocupar()`, `liberar()`).
5. Dibujar asociaciones `Directed Association` o `Association` configurando las multiplicidades (`1` a `0..*`).

---

## 4. Diagrama de Paquetes (UML)

Organiza los módulos lógicos del sistema y define sus dependencias e interfaces:

### 4.1. Representación en Mermaid
```mermaid
graph TD
    subgraph Frontend_App [Paquete: Frontend React Application]
        UI_Components[Componentes UI: Entrada, Salida, Celdas]
        UI_Services[API Client / HTTP Axios/Fetch]
        UI_State[Gestión de Estado]
    end

    subgraph Backend_App [Paquete: Backend Python FastAPI Service]
        subgraph Routers [app.routers]
            R_Auth[auth_router]
            R_Vehicles[vehicles_router]
            R_Movements[movements_router]
            R_Cells[cells_router]
        end

        subgraph Services [app.services]
            S_Parking[parking_service]
            S_Subscription[subscription_service]
            S_Incident[incident_service]
        end

        subgraph Repositories [app.repositories]
            Repo_Movements[movement_repository]
            Repo_Cells[cell_repository]
            Repo_Vehicles[vehicle_repository]
        end

        subgraph Models_Schemas [app.models & app.schemas]
            ORM_Models[SQLAlchemy Models]
            Pydantic_DTO[Pydantic Schemas / DTOs]
        end
    end

    subgraph Database_Layer [Paquete: Base de Datos Relacional]
        MySQL_DB[(MySQL 8.0 Engine)]
    end

    UI_Components --> UI_Services
    UI_Services --> Routers
    Routers --> Services
    Routers --> Pydantic_DTO
    Services --> Repositories
    Services --> ORM_Models
    Repositories --> MySQL_DB
```

### 4.2. Guía para Modelar en StarUML:
1. Menú `Model` -> `Add Diagram` -> `Package Diagram`.
2. Arrastrar elementos `Package` (`app.routers`, `app.services`, `app.repositories`, `app.models`, `Frontend_App`, `MySQL_DB`).
3. Crear relaciones de dependencia (`Dependency` - flecha punteada) indicando el flujo unidireccional de capas, respetando el principio de inversión de dependencias.
