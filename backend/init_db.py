"""
Script de inicialización y carga de datos semilla (Seed Data)
Funciona tanto con MySQL como con SQLite de forma agnóstica.
"""
from datetime import date, datetime, timedelta
from app.database import engine, Base, SessionLocal
from app.models.user import User, UserRole, UserStatus
from app.models.vehicle import Vehicle, VehicleType, VehicleTransitStatus
from app.models.cell import Cell, CellStatus
from app.models.subscription import Subscription, SubscriptionStatus
from app.models.movement import Movement, MovementStatus
from app.models.incident import Incident, IncidentType, IncidentSeverity, IncidentMoment

def init_database():
    # 1. Crear todas las tablas
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 2. Verificar si ya existen usuarios
        if db.query(User).count() > 0:
            print("La base de datos ya contiene datos. Omitiendo carga de semillas.")
            return

        print("Cargando datos semilla...")

        # Usuarios
        admin = User(
            id=1, documento_identidad="1020304050", nombres="Carlos", apellidos="Gómez",
            telefono="3001234567", email="admin@autoscolombia.com", rol=UserRole.ADMIN,
            password_hash="$2b$12$e80MvK2iL4h8D7Oa8XvQde7zR8m5V3p1N5e7G6k0pL9qW4z8y1B2a", estado=UserStatus.ACTIVO
        )
        op1 = User(
            id=2, documento_identidad="1030405060", nombres="Andrés", apellidos="López",
            telefono="3109876543", email="operario1@autoscolombia.com", rol=UserRole.OPERARIO,
            password_hash="$2b$12$e80MvK2iL4h8D7Oa8XvQde7zR8m5V3p1N5e7G6k0pL9qW4z8y1B2a", estado=UserStatus.ACTIVO
        )
        op2 = User(
            id=3, documento_identidad="1040506070", nombres="Laura", apellidos="Martínez",
            telefono="3157654321", email="operario2@autoscolombia.com", rol=UserRole.OPERARIO,
            password_hash="$2b$12$e80MvK2iL4h8D7Oa8XvQde7zR8m5V3p1N5e7G6k0pL9qW4z8y1B2a", estado=UserStatus.ACTIVO
        )
        c1 = User(
            id=4, documento_identidad="71234567", nombres="Mauricio", apellidos="Restrepo",
            telefono="3201122334", email="mauricio.restrepo@gmail.com", rol=UserRole.CLIENTE,
            password_hash="", estado=UserStatus.ACTIVO
        )
        c2 = User(
            id=5, documento_identidad="43567890", nombres="Camila", apellidos="Fernández",
            telefono="3004455667", email="camila.fernandez@outlook.com", rol=UserRole.CLIENTE,
            password_hash="", estado=UserStatus.ACTIVO
        )
        c3 = User(
            id=6, documento_identidad="98765432", nombres="Javier", apellidos="Vargas",
            telefono="3118899001", email="javier.vargas@yahoo.com", rol=UserRole.CLIENTE,
            password_hash="", estado=UserStatus.ACTIVO
        )
        db.add_all([admin, op1, op2, c1, c2, c3])
        db.flush()

        # Celdas
        cells = [
            Cell(id=1, codigo="A-01", tipo_permitido=VehicleType.CARRO, estado=CellStatus.DISPONIBLE, zona_piso="Piso 1 - Zona Norte", observaciones="Cerca a la entrada principal"),
            Cell(id=2, codigo="A-02", tipo_permitido=VehicleType.CARRO, estado=CellStatus.DISPONIBLE, zona_piso="Piso 1 - Zona Norte", observaciones="Celda estándar"),
            Cell(id=3, codigo="A-03", tipo_permitido=VehicleType.CARRO, estado=CellStatus.DISPONIBLE, zona_piso="Piso 1 - Zona Norte", observaciones="Celda estándar"),
            Cell(id=4, codigo="A-04", tipo_permitido=VehicleType.CARRO, estado=CellStatus.DISPONIBLE, zona_piso="Piso 1 - Zona Norte", observaciones="Celda estándar"),
            Cell(id=5, codigo="A-05", tipo_permitido=VehicleType.CARRO, estado=CellStatus.MANTENIMIENTO, zona_piso="Piso 1 - Zona Norte", observaciones="Pintura y demarcación en proceso"),
            Cell(id=6, codigo="B-01", tipo_permitido=VehicleType.CAMIONETA, estado=CellStatus.DISPONIBLE, zona_piso="Piso 1 - Zona Sur", observaciones="Espacio amplio para SUV"),
            Cell(id=7, codigo="B-02", tipo_permitido=VehicleType.CAMIONETA, estado=CellStatus.DISPONIBLE, zona_piso="Piso 1 - Zona Sur", observaciones="Espacio amplio"),
            Cell(id=8, codigo="M-01", tipo_permitido=VehicleType.MOTO, estado=CellStatus.DISPONIBLE, zona_piso="Piso 1 - Zona Motos", observaciones="Bahía techada"),
            Cell(id=9, codigo="M-02", tipo_permitido=VehicleType.MOTO, estado=CellStatus.DISPONIBLE, zona_piso="Piso 1 - Zona Motos", observaciones="Bahía techada"),
            Cell(id=10, codigo="E-01", tipo_permitido=VehicleType.ESPECIAL, estado=CellStatus.DISPONIBLE, zona_piso="Piso 1 - Zona Accesible", observaciones="Movilidad reducida"),
        ]
        db.add_all(cells)
        db.flush()

        # Vehículos
        vehicles = [
            Vehicle(id=1, placa="HJR542", tipo_vehiculo=VehicleType.CARRO, marca="Mazda", modelo="Mazda 3 2021", color="Rojo Diamante", cliente_id=4, estado_actual=VehicleTransitStatus.FUERA),
            Vehicle(id=2, placa="TKL890", tipo_vehiculo=VehicleType.CAMIONETA, marca="Renault", modelo="Duster 2020", color="Gris Estrella", cliente_id=5, estado_actual=VehicleTransitStatus.FUERA),
            Vehicle(id=3, placa="WXY12C", tipo_vehiculo=VehicleType.MOTO, marca="Yamaha", modelo="MT-03 2022", color="Negro Mate", cliente_id=6, estado_actual=VehicleTransitStatus.FUERA),
            Vehicle(id=4, placa="QWE345", tipo_vehiculo=VehicleType.CARRO, marca="Chevrolet", modelo="Onix 2019", color="Blanco", cliente_id=4, estado_actual=VehicleTransitStatus.FUERA),
        ]
        db.add_all(vehicles)
        db.flush()

        # Mensualidades
        today = date.today()
        subs = [
            # 1. Vigente (Mauricio - HJR542)
            Subscription(
                id=1, codigo_contrato="CTR-2026-001", cliente_id=4, vehiculo_id=1,
                celda_preferida_id=1, fecha_inicio=today - timedelta(days=10),
                fecha_fin=today + timedelta(days=20), valor_mensual=180000.0,
                estado=SubscriptionStatus.ACTIVA, observaciones="Contrato mensual activo diurno y nocturno"
            ),
            # 2. Próxima a vencer en 3 días (Camila - TKL890)
            Subscription(
                id=2, codigo_contrato="CTR-2026-002", cliente_id=5, vehiculo_id=2,
                celda_preferida_id=6, fecha_inicio=today - timedelta(days=27),
                fecha_fin=today + timedelta(days=3), valor_mensual=220000.0,
                estado=SubscriptionStatus.ACTIVA, observaciones="Por vencer en 3 días"
            ),
            # 3. Vencida (Javier - WXY12C)
            Subscription(
                id=3, codigo_contrato="CTR-2026-003", cliente_id=6, vehiculo_id=3,
                celda_preferida_id=8, fecha_inicio=today - timedelta(days=40),
                fecha_fin=today - timedelta(days=10), valor_mensual=80000.0,
                estado=SubscriptionStatus.VENCIDA, observaciones="Venció hace 10 días"
            ),
        ]
        db.add_all(subs)
        db.commit()
        print("¡Base de datos inicializada y datos semilla cargados con éxito!")
    except Exception as e:
        db.rollback()
        print(f"Error cargando semillas: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
