import pytest
from datetime import date, datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models.user import User, UserRole, UserStatus
from app.models.vehicle import Vehicle, VehicleType, VehicleTransitStatus
from app.models.cell import Cell, CellStatus
from app.models.subscription import Subscription, SubscriptionStatus

# Base de datos de prueba en memoria SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()

    # Usuario cliente y operario
    user_op = User(
        id=2, documento_identidad="102030", nombres="Andres", apellidos="Operario",
        telefono="3000000", email="op@test.com", rol=UserRole.OPERARIO, password_hash=""
    )
    user_client = User(
        id=4, documento_identidad="712345", nombres="Mauricio", apellidos="Restrepo",
        telefono="3200000", email="cliente@test.com", rol=UserRole.CLIENTE, password_hash=""
    )
    db.add_all([user_op, user_client])
    db.commit()

    # Celdas
    cell1 = Cell(id=1, codigo="A-01", tipo_permitido=VehicleType.CARRO, estado=CellStatus.DISPONIBLE, zona_piso="Piso 1")
    cell2 = Cell(id=2, codigo="A-02", tipo_permitido=VehicleType.CARRO, estado=CellStatus.DISPONIBLE, zona_piso="Piso 1")
    db.add_all([cell1, cell2])
    db.commit()

    # Vehículo 1 (Activo)
    v1 = Vehicle(
        id=1, placa="ABC123", tipo_vehiculo=VehicleType.CARRO, marca="Mazda",
        modelo="3", color="Rojo", cliente_id=4, estado_actual=VehicleTransitStatus.FUERA
    )
    # Vehículo 2 (Sin mensualidad)
    v2 = Vehicle(
        id=2, placa="XYZ999", tipo_vehiculo=VehicleType.CARRO, marca="Renault",
        modelo="Logan", color="Gris", cliente_id=4, estado_actual=VehicleTransitStatus.FUERA
    )
    db.add_all([v1, v2])
    db.commit()

    # Mensualidad activa para Vehículo 1
    sub1 = Subscription(
        id=1, codigo_contrato="CTR-001", cliente_id=4, vehiculo_id=1,
        celda_preferida_id=1, fecha_inicio=date.today() - timedelta(days=5),
        fecha_fin=date.today() + timedelta(days=25), valor_mensual=150000,
        estado=SubscriptionStatus.ACTIVA
    )
    db.add(sub1)
    db.commit()
    db.close()

    yield

    Base.metadata.drop_all(bind=engine_test)

def test_validate_vehicle_active_subscription():
    response = client.get("/api/vehicles/validate/ABC123")
    assert response.status_code == 200
    data = response.json()
    assert data["placa"] == "ABC123"
    assert data["es_mensualidad_vigente"] is True
    assert data["celda_sugerida_codigo"] == "A-01"

def test_entry_and_exit_flow():
    # 1. Registrar entrada
    entry_payload = {
        "placa": "ABC123",
        "celda_id": 1,
        "operario_id": 2,
        "kilometraje_entrada": 45000,
        "novedad": {
            "tipo_novedad": "RAYON",
            "severidad": "LEVE",
            "descripcion": "Rayón leve en guardabarro derecho"
        }
    }
    entry_resp = client.post("/api/movements/entry", json=entry_payload)
    assert entry_resp.status_code == 201
    entry_data = entry_resp.json()
    assert entry_data["success"] is True
    assert entry_data["celda_codigo"] == "A-01"
    assert entry_data["novedad"]["tipo"] == "RAYON"

    # 2. Verificar Anti-Passback (no debe permitir doble entrada)
    dup_resp = client.post("/api/movements/entry", json=entry_payload)
    assert dup_resp.status_code == 400
    assert "ya figura dentro" in dup_resp.json()["detail"]

    # 3. Verificar estado de celdas y métricas
    metrics_resp = client.get("/api/cells/metrics")
    assert metrics_resp.status_code == 200
    metrics = metrics_resp.json()
    assert metrics["ocupadas"] == 1
    assert metrics["disponibles"] == 1

    # 4. Registrar salida
    exit_payload = {
        "placa": "ABC123",
        "operario_id": 2
    }
    exit_resp = client.post("/api/movements/exit", json=exit_payload)
    assert exit_resp.status_code == 200
    exit_data = exit_resp.json()
    assert exit_data["success"] is True
    assert exit_data["celda_liberada"] == "A-01"

    # 5. Celda debe volver a estar disponible
    metrics_after = client.get("/api/cells/metrics").json()
    assert metrics_after["ocupadas"] == 0
    assert metrics_after["disponibles"] == 2
