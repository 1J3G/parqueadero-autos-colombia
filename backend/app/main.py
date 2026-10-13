from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
import app.models  # Asegura el registro de todos los modelos
from app.routers import movements, cells, vehicles

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas si no existen (útil en dev/test)
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"[Warning] Error inicializando tablas en base de datos: {e}")
    yield

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="API de Gestión Operativa para Parqueadero Autos Colombia - Iteración 1",
    lifespan=lifespan
)

# Configuración de CORS para permitir conexión con Frontend React / Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de routers modulares
app.include_router(movements.router, prefix="/api")
app.include_router(cells.router, prefix="/api")
app.include_router(vehicles.router, prefix="/api")

@app.get("/", tags=["Health Check"])
def root():
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "docs_url": "/docs",
        "version": "1.0.0"
    }
