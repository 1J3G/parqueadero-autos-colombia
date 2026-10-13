# Documento de Requerimientos del Sistema (SRS)
## Proyecto: Parqueadero Autos Colombia - Iteración 1

---

## 1. Introducción y Propósito
El propósito de este documento es especificar formalmente los requerimientos funcionales y no funcionales para la **Iteración 1** del sistema de gestión operativa de **"Parqueadero Autos Colombia"**. 

El modelo de negocio principal corresponde al servicio de parqueadero por modalidad de **mensualidad** (contrato mensual con pago recurrente), el cual requiere un control riguroso de:
1. Registro ágil y seguro de entradas y salidas de vehículos.
2. Verificación de vigencia y estado de pagos de la mensualidad.
3. Gestión del estado y asignación de celdas en tiempo real.
4. Registro de novedades y estado físico del vehículo (evidencia de daños preexistentes).
5. Seguridad e integridad operativa para operarios de caseta y administradores.

---

## 2. Reglas de Negocio (RN)

- **RN-01 (Validación de Mensualidad Activa):** Un vehículo solo puede ingresar si tiene un contrato de mensualidad con estado **Activo** y su fecha de vigencia es mayor o igual a la fecha actual. Si está vencida, el sistema debe alertar al operario y bloquear el ingreso salvo autorización administrativa con registro de novedad.
- **RN-02 (Regla Anti-Passback / Duplicidad de Tránsito):** No se permite registrar la entrada de un vehículo que figure con estado actual "Dentro del parqueadero". De igual forma, no se permite registrar la salida de un vehículo que figure "Fuera del parqueadero".
- **RN-03 (Asignación y Compatibilidad de Celda):** Al ingresar, el vehículo debe ser asignado a una celda disponible compatible con su tipo (Carro, Moto, Camioneta, Discapacitado). La celda pasa inmediatamente a estado "Ocupada".
- **RN-04 (Liberación de Celda en Salida):** Al registrar la salida de un vehículo, la celda ocupada se libera automáticamente y pasa a estado "Disponible".
- **RN-05 (Custodia y Responsabilidad por Novedades):** Si el vehículo ingresa con golpes, rayones o novedades físicas visibles, el operario debe registrarlas en el sistema con descripción y severidad (Leve, Moderada, Grave) para evitar reclamaciones injustificadas.
- **RN-06 (Unicidad de Placa):** Cada vehículo está unívocamente identificado por su placa alfanumérica en el formato regulatorio colombiano (ejemplo: `ABC123` para carros o `ABC12D` para motos).
- **RN-07 (Trazabilidad de Operaciones):** Todo registro de entrada, salida o novedad debe almacenar fecha, hora exacta (timestamp) y el ID del operario responsable en turno.

---

## 3. Requerimientos Funcionales (RF)

### 3.1. Módulo de Gestión de Entrada de Vehículos
- **RF-01 (Búsqueda Rápida por Placa):** El sistema debe permitir al operario ingresar o escanear la placa del vehículo y obtener en menos de 1 segundo los datos del vehículo, propietario, estado de su mensualidad y celda asignada habitual.
- **RF-02 (Validación de Acceso):** El sistema debe verificar automáticamente que el vehículo tenga mensualidad vigente, esté al día con los pagos y no se encuentre actualmente dentro de las instalaciones.
- **RF-03 (Asignación de Celda de Parqueo):** El sistema debe sugerir la celda fija asociada a la mensualidad o una celda libre compatible con el tipo de vehículo, permitiendo confirmar o cambiar la celda.
- **RF-04 (Registro de Entrada):** El sistema debe registrar la fecha y hora de ingreso, kilometraje (opcional), celda asignada y operario de turno, cambiando el estado del vehículo a "Dentro" y de la celda a "Ocupada".
- **RF-05 (Registro de Novedad en Entrada):** El sistema debe permitir registrar novedades visuales del vehículo al ingresar (tipo de novedad, descripción, nivel de severidad: Leve, Moderado, Grave).
- **RF-06 (Generación de Comprobante de Entrada):** El sistema debe generar un comprobante digital (ticket/resumen de entrada) con placa, celda, fecha/hora de ingreso y datos del cliente.

### 3.2. Módulo de Gestión de Salida de Vehículos
- **RF-07 (Consulta de Vehículo para Salida):** El sistema debe permitir buscar el vehículo por placa o número de celda y verificar que se encuentre registrado como "Dentro".
- **RF-08 (Validación de Novedades y Permanencia):** El sistema debe mostrar el tiempo total de permanencia, las novedades registradas al ingreso y permitir registrar novedades ocurridas durante la estadía si fuese necesario.
- **RF-09 (Registro de Salida):** El sistema debe registrar la fecha y hora de salida, calcular el tiempo de permanencia, cambiar el estado del vehículo a "Fuera" y actualizar la celda a estado "Disponible".
- **RF-10 (Generación de Comprobante de Salida):** El sistema debe emitir un comprobante digital de salida con el resumen de la estancia y paz y salvo del servicio mensual.

### 3.3. Módulo de Gestión de Celdas y Aforo
- **RF-11 (Visualización en Tiempo Real de Celdas):** El sistema debe ofrecer una vista en cuadrícula del estado de todas las celdas (Disponible, Ocupada, Mantenimiento, Reservada) identificadas por código (ej. A-01, B-05).
- **RF-12 (Filtrado de Celdas por Tipo):** El sistema debe permitir filtrar celdas por tipo de vehículo (Carro, Moto, Camioneta, Especial).
- **RF-13 (Métricas Rápidas de Ocupación):** El sistema debe mostrar el total de celdas libres, ocupadas, en mantenimiento y porcentaje global de ocupación.

### 3.4. Módulo de Gestión de Mensualidades y Clientes
- **RF-14 (Consulta de Estado de Mensualidad):** El sistema debe permitir consultar el historial de mensualidad del cliente, fecha de inicio, fecha de fin y estado del pago (Al día, Por vencer en X días, Vencido).
- **RF-15 (Alerta de Vencimiento Próximo):** El sistema debe advertir al operario si la mensualidad del vehículo que ingresa vencerá en los próximos 5 días calendario.

---

## 4. Requerimientos No Funcionales (RNF)

- **RNF-01 (Rendimiento y Tiempo de Respuesta):** El registro y consulta de placa en la caseta de entrada/salida debe procesarse en un tiempo inferior a 500 milisegundos bajo condiciones normales.
- **RNF-02 (Disponibilidad y Tolerancia a Fallos):** El sistema debe operar con alta disponibilidad (99.5% de uptime en horas laborales) y manejar excepciones de red o base de datos sin pérdida de datos en tránsito.
- **RNF-03 (Seguridad y Control de Acceso):** Autenticación mediante tokens JWT seguros y autorización basada en roles (Operario de Caseta, Supervisor, Administrador). Las contraseñas deben cifrarse con algoritmos seguros (bcrypt/argon2).
- **RNF-04 (Integridad y Consistencia de Datos en MySQL):** Uso estricto de transacciones ACID (`BEGIN`, `COMMIT`, `ROLLBACK`) en MySQL con motor InnoDB para garantizar que la asignación de celdas y el registro de entradas no generen condiciones de carrera (doble asignación).
- **RNF-05 (Usabilidad y Ergonomía en Caseta):** La interfaz de usuario debe estar optimizada para operarios de caseta, permitiendo operar mediante atajos de teclado rápidos (`Enter` para buscar/confirmar, `Esc` para cancelar), con alto contraste y diseño adaptable.
- **RNF-06 (Portabilidad y Modularidad):** Arquitectura desacoplada en capas (Backend REST API en Python FastAPI y Frontend SPA en React + Vite), facilitando despliegue local o en contenedores Docker.
- **RNF-07 (Trazabilidad y Auditoría):** Registro detallado de logs para cada transacción de entrada, salida y cambio de estado de celdas, incluyendo dirección IP y usuario responsable.
- **RNF-08 (Mantenibilidad del Código):** Código fuente con tipado estricto (Pydantic v2 / TypeScript / Python typing), documentación autogenerada OpenAPI/Swagger en `/docs`, y cobertura de pruebas unitarias.
- **RNF-09 (Escalabilidad de Almacenamiento):** Estructura relacional indexada por placa, fecha y estado para soportar decenas de miles de registros históricos de movimientos sin degradación.
- **RNF-10 (Compatibilidad de Navegadores):** El frontend debe ser compatible con las últimas versiones de Google Chrome, Mozilla Firefox y Microsoft Edge.
