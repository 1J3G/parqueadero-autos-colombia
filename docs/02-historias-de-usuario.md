# Historias de Usuario (User Stories) - Iteración 1
## Proyecto: Parqueadero Autos Colombia

Este documento contiene las Historias de Usuario (HU) desarrolladas para la **Iteración 1: Gestión de entrada y salida de vehículos**, redactadas bajo el estándar ágil y acompañadas de sus respectivos criterios de aceptación en formato BDD Gherkin (**Dado que / Cuando / Entonces** - *Given / When / Then*).

---

## 1. Matriz de Trazabilidad (RF vs. Historias de Usuario)

| Historia de Usuario | Título | Requerimientos Asociados | Prioridad |
|---|---|---|---|
| **HU-01** | Búsqueda y Validación de Vehículo por Placa | RF-01, RF-02, RF-14, RF-15 | Alta (Must) |
| **HU-02** | Registro de Entrada y Asignación de Celda | RF-03, RF-04, RF-06 | Alta (Must) |
| **HU-03** | Registro de Novedades al Ingreso | RF-05, RF-07 | Media (Should) |
| **HU-04** | Registro de Salida de Vehículo y Liberación de Celda | RF-07, RF-08, RF-09, RF-10 | Alta (Must) |
| **HU-05** | Monitor de Estado de Celdas en Tiempo Real | RF-11, RF-12, RF-13 | Alta (Must) |
| **HU-06** | Control de Alertas de Vencimiento de Mensualidad | RF-02, RF-14, RF-15 | Media (Should) |

---

## 2. Historias de Usuario Detalladas

---

### HU-01: Búsqueda y Validación de Vehículo por Placa
**Como** operario de caseta de entrada,  
**Quiero** ingresar la placa del vehículo que llega al parqueadero,  
**Para** verificar en tiempo real si el cliente cuenta con una mensualidad activa y saber si tiene autorización de ingreso.

#### Criterios de Aceptación (Gherkin):
- **Escenario 1: Vehículo con mensualidad activa y al día**
  - **Dado que** el vehículo con placa `ABC123` está registrado en el sistema,
  - **Y** su mensualidad tiene fecha de vencimiento posterior a la fecha actual,
  - **Y** el vehículo actualmente figura como "Fuera",
  - **Cuando** el operario digita la placa `ABC123` y presiona "Buscar",
  - **Entonces** el sistema debe mostrar los datos del cliente, vehículo, tipo (Carro/Moto), estado "Mensualidad Vigente" (en verde) y habilitar el botón de "Registrar Entrada".

- **Escenario 2: Vehículo con mensualidad vencida**
  - **Dado que** el vehículo con placa `XYZ789` tiene su fecha de mensualidad vencida,
  - **Cuando** el operario consulta la placa `XYZ789`,
  - **Entonces** el sistema debe mostrar una alerta visual en rojo "Mensualidad Vencida el [Fecha]", indicando los días de mora,
  - **Y** deshabilitar el registro normal de entrada, solicitando confirmación de regularización o cobro de tarifa especial.

- **Escenario 3: Vehículo que ya se encuentra dentro (Anti-passback)**
  - **Dado que** el vehículo con placa `DEF456` ya tiene una entrada registrada sin salida previa,
  - **Cuando** el operario intenta consultar o registrar su ingreso,
  - **Entonces** el sistema debe emitir un error crítico: "El vehículo ya se encuentra registrado dentro de las instalaciones en la celda [A-04]".

---

### HU-02: Registro de Entrada y Asignación de Celda
**Como** operario de caseta,  
**Quiero** confirmar la entrada del vehículo y asignarle una celda disponible acorde a su tipo,  
**Para** garantizar el orden en el estacionamiento y controlar el aforo en tiempo real.

#### Criterios de Aceptación (Gherkin):
- **Escenario 1: Asignación automática o sugerida de celda disponible**
  - **Dado que** el vehículo `ABC123` (tipo Automóvil) fue validado exitosamente,
  - **Cuando** el operario abre la sección de asignación de celda,
  - **Entonces** el sistema debe preseleccionar la celda asignada en su contrato o la primera celda libre de tipo "Automóvil" (ejemplo: `A-12`),
  - **Y** permitir al operario cambiarla si es necesario por otra celda disponible.

- **Escenario 2: Confirmación de ingreso exitoso**
  - **Dado que** el operario confirma la celda `A-12` para el vehículo `ABC123`,
  - **Cuando** hace clic en "Registrar Entrada",
  - **Entonces** el sistema debe guardar el movimiento con fecha, hora exacta y usuario operario en base de datos MySQL,
  - **Y** actualizar la celda `A-12` a estado "Ocupada",
  - **Y** generar el ticket/comprobante de entrada digital con opción de impresión o envío.

- **Escenario 3: Sin celdas disponibles para el tipo de vehículo**
  - **Dado que** todas las celdas del tipo solicitado están ocupadas,
  - **Cuando** el operario intenta registrar la entrada,
  - **Entonces** el sistema debe emitir una advertencia: "Aforo completo para vehículos tipo Automóvil" e impedir la operación hasta que se libere un espacio.

---

### HU-03: Registro de Novedades al Ingreso
**Como** operario de parqueadero,  
**Quiero** registrar cualquier daño o novedad física detectada en el vehículo al momento de ingresar,  
**Para** salvaguardar la responsabilidad legal del parqueadero ante reclamos por daños preexistentes.

#### Criterios de Aceptación (Gherkin):
- **Escenario 1: Registro de novedad física con severidad**
  - **Dado que** el operario observa un rayón en la puerta lateral izquierda del vehículo `ABC123`,
  - **Cuando** activa el selector "Registrar Novedad" en el formulario de entrada,
  - **Y** selecciona la categoría "Carrocería / Rayón", nivel de severidad "Moderado", y escribe la observación "Rayón profundo de 15cm en puerta delantera izquierda",
  - **Y** confirma la entrada,
  - **Entonces** el sistema debe asociar la novedad al registro de entrada actual y guardarla en la tabla de novedades con timestamp,
  - **Y** plasmar la observación en el comprobante digital de ingreso.

---

### HU-04: Registro de Salida de Vehículo y Liberación de Celda
**Como** operario de caseta de salida,  
**Quiero** registrar la salida del vehículo ingresando su placa o número de celda,  
**Para** liberar la celda ocupada, calcular el tiempo de estadía y certificar el retiro del vehículo.

#### Criterios de Aceptación (Gherkin):
- **Escenario 1: Salida normal de vehículo que está dentro**
  - **Dado que** el vehículo `ABC123` ingresó a las 08:00 AM en la celda `A-12` y son las 05:30 PM,
  - **Cuando** el operario busca la placa `ABC123` en el módulo de salidas y presiona "Registrar Salida",
  - **Entonces** el sistema debe registrar la fecha y hora de salida,
  - **Y** calcular la duración total de permanencia (ej. "9 horas, 30 minutos"),
  - **Y** cambiar el estado de la celda `A-12` a "Disponible",
  - **Y** cambiar el estado del vehículo a "Fuera",
  - **Y** mostrar el resumen final de la salida.

- **Escenario 2: Intento de salida de vehículo que no figura adentro**
  - **Dado que** el vehículo `XYZ999` tiene estado "Fuera",
  - **Cuando** el operario intenta registrar su salida,
  - **Entonces** el sistema debe alertar: "El vehículo no tiene un registro de entrada activo dentro del parqueadero".

---

### HU-05: Monitor de Estado de Celdas en Tiempo Real
**Como** administrador u operario,  
**Quiero** visualizar en un tablero gráfico la matriz de todas las celdas del parqueadero organizadas por zona y tipo,  
**Para** conocer de un vistazo la ocupación total, disponibilidad de espacios y celdas bloqueadas.

#### Criterios de Aceptación (Gherkin):
- **Escenario 1: Visualización del mapa de celdas por estado y color**
  - **Dado que** el usuario ingresa al panel de "Celdas / Aforo",
  - **Cuando** carga la pantalla,
  - **Entonces** el sistema debe renderizar las celdas con códigos visuales:
    - Verde: Disponible
    - Rojo: Ocupada (con placa del vehículo y tiempo transcurrido)
    - Amarillo: En Mantenimiento
    - Azul: Reservada
  - **Y** mostrar las métricas superiores: Total celdas, % Ocupación, Libres para Carros y Libres para Motos.

---

### HU-06: Control de Alertas de Vencimiento de Mensualidad
**Como** administrador o cajero,  
**Quiero** recibir advertencias preventivas cuando la mensualidad de un cliente esté por expirar,  
**Para** notificarle con anticipación y gestionar la renovación del pago sin interrumpir su servicio.

#### Criterios de Aceptación (Gherkin):
- **Escenario 1: Alerta preventiva de vencimiento próximo (menor a 5 días)**
  - **Dado que** la mensualidad del vehículo `ABC123` vence en 3 días,
  - **Cuando** el operario registra el ingreso del vehículo,
  - **Entonces** el sistema debe mostrar un aviso visual color ámbar: "Atención: La mensualidad de este vehículo vence en 3 días ([Fecha de vencimiento]). Recordar renovación al usuario.",
  - **Y** permitir continuar con el registro de entrada sin bloquearlo.
