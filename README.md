# Parqueadero Autos Colombia - Sistema de Control Operativo
> **Iteración 1: Gestión de Entrada, Salida de Vehículos, Celdas y Mensualidades**

Sistema integral de gestión operativa para parqueaderos por suscripción mensual en Colombia. Permite registrar ingresos y salidas en tiempo real, validar automáticamente la vigencia de contratos, controlar la disponibilidad de celdas por tipo de vehículo, registrar novedades físicas (daños preexistentes para protección legal) y prevenir fraudes o errores mediante reglas anti-passback.

---

## 🛠️ Stack Tecnológico

- **Backend:** Python 3.13 + [FastAPI](https://fastapi.tiangolo.com/) + Pydantic v2 + SQLAlchemy 2.0 + PyMySQL.
- **Base de Datos:** [MySQL 8.x](https://www.mysql.com/) (Motor InnoDB, codificación UTF-8 mb4, constraints e índices optimizados).
- **Frontend:** [React 18](https://react.dev/) + [Vite](https://vitejs.dev/) + CSS moderno (Glassmorphism, Dark Mode y diseño optimizado para caseta).
- **Documentación y Modelado:** Markdown, Mermaid y especificaciones para [StarUML](https://staruml.io/).
- **Control de Versiones:** Git / GitHub.

---

## 📁 Estructura del Proyecto

```text
parqueadero/
├── .gitignore                      # Exclusiones de Git
├── README.md                       # Documentación principal y guía de arranque
├── Prompt Parqueadero.txt          # Requerimientos base iniciales
│
├── docs/                           # Documentación técnica modular (.md)
│   ├── 01-requerimientos.md        # RF, RNF y Reglas de Negocio
│   ├── 02-historias-de-usuario.md  # Historias de Usuario con BDD Gherkin
│   ├── 03-modelo-datos.md          # MER, Modelo Relacional y Diccionario
│   ├── 04-arquitectura-uml.md      # Arquitectura en Capas y Diagramas UML
│   └── 05-mockups-ui.md            # Especificación UI y Wireframes
│
├── database/                       # Scripts SQL físicos
│   ├── schema.sql                  # Script DDL (Tablas, Claves, Índices) para MySQL
│   └── seed.sql                    # Datos semilla para pruebas inmediatas
│
├── backend/                        # API REST en Python FastAPI
│   ├── requirements.txt            # Dependencias Python
│   ├── .env.example                # Plantilla de variables de entorno
│   ├── app/
│   │   ├── main.py                 # Punto de entrada de FastAPI y CORS
│   │   ├── config.py               # Configuración Pydantic Settings
│   │   ├── database.py             # Conexión SQLAlchemy y pool
│   │   ├── models/                 # Modelos ORM (User, Vehicle, Cell, Movement, Incident)
│   │   ├── schemas/                # Schemas Pydantic / DTOs
│   │   ├── routers/                # Endpoints REST (movements, cells, vehicles)
│   │   └── services/               # Lógica de negocio (parking_service, cell_service)
│   └── tests/
│       └── test_movements.py       # Pruebas automatizadas (pytest)
│
└── frontend/                       # Dashboard Operativo en React + Vite
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── App.jsx                 # Componente principal y orquestador
        ├── main.jsx                # Punto de montaje React
        ├── index.css               # Estilos y tokens de diseño
        ├── api/client.js           # Cliente HTTP hacia la API
        └── components/
            ├── Header.jsx          # Barra superior y accesos rápidos
            ├── SummaryMetrics.jsx  # Indicadores clave en vivo
            ├── CellGrid.jsx        # Matriz visual de celdas
            ├── ActiveVehiclesList.jsx # Lista de vehículos adentro
            ├── EntryModal.jsx      # Modal de registro de entrada y novedades
            └── ExitModal.jsx       # Modal de salida y liberación
```

---

## 🚀 Guía de Instalación y Ejecución

### 1. Base de Datos (MySQL)

1. Abre tu cliente MySQL preferido (MySQL Workbench, phpMyAdmin, DBeaver o terminal).
2. Ejecuta el script DDL para crear la base de datos y sus tablas:
   ```bash
   mysql -u root -p < database/schema.sql
   ```
3. Opcionalmente, carga los datos semilla de prueba:
   ```bash
   mysql -u root -p < database/seed.sql
   ```

---

### 2. Backend (Python + FastAPI)

1. Abre una terminal y navega a la carpeta `backend`:
   ```bash
   cd backend
   ```
2. Crea y activa un entorno virtual de Python:
   ```bash
   # En Windows PowerShell:
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Configura tus variables de entorno copiando `.env.example`:
   ```bash
   cp .env.example .env
   ```
   *(Asegúrate de ajustar tu usuario y contraseña de MySQL en `DATABASE_URL`)*.
5. Ejecuta las pruebas unitarias para validar las reglas de negocio:
   ```bash
   pytest tests/
   ```
6. Inicia el servidor de desarrollo:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
7. Accede a la documentación interactiva Swagger:
   - **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
   - **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### 3. Frontend (React + Vite)

1. Abre otra terminal y navega a la carpeta `frontend`:
   ```bash
   cd frontend
   ```
2. Instala las dependencias de Node:
   ```bash
   npm install
   ```
3. Inicia el servidor local de desarrollo:
   ```bash
   npm run dev
   ```
4. Abre tu navegador en [http://localhost:5173](http://localhost:5173).

---

## 🧪 Casos de Prueba Listos para Demostración

Con los datos semilla cargados en `database/seed.sql`:

1. **Vehículo con Mensualidad Vigente (Éxito):**
   - Placa: `HJR542` (Mazda 3 Rojo, Propietario: Mauricio Restrepo).
   - Resultado: Mensualidad activa, sugiere celda `A-01`, permite registrar entrada con o sin novedades físicas.
2. **Vehículo con Mensualidad Próxima a Vencer (Alerta Preventiva):**
   - Placa: `TKL890` (Renault Duster Gris, Propietaria: Camila Fernández).
   - Resultado: Alerta ámbar notificando que la mensualidad vence en pocos días.
3. **Vehículo con Mensualidad Vencida (Bloqueo):**
   - Placa: `WXY12C` (Yamaha MT-03, Propietario: Javier Vargas).
   - Resultado: Alerta roja informando contrato vencido e impidiendo la entrada habitual.
4. **Regla Anti-Passback:**
   - Una vez que `HJR542` ingresa, intentar registrar nuevamente su entrada produce error inmediato informando que el vehículo ya está adentro en la celda `A-01`.
5. **Salida y Liberación de Celda:**
   - Al registrar la salida de `HJR542`, el sistema calcula el tiempo de estancia, libera automáticamente la celda `A-01` y actualiza la matriz en vivo.

---

## 🔗 Conexión a Repositorio GitHub

Para conectar este proyecto con un nuevo repositorio en GitHub:

```bash
# 1. En la raíz del proyecto (c:\cursos-desarrollo\parqueadero)
git init

# 2. Agregar todos los archivos al área de preparación
git add .

# 3. Realizar el primer commit
git commit -m "feat: inicializacion de proyecto Parqueadero Autos Colombia - Iteracion 1"

# 4. Crear rama principal
git branch -M main

# 5. Vincular con tu repositorio remoto en GitHub
git remote add origin https://github.com/TU_USUARIO/parqueadero-autos-colombia.git

# 6. Subir los cambios a GitHub
git push -u origin main
```
