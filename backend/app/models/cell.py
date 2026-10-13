import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.vehicle import VehicleType

class CellStatus(str, enum.Enum):
    DISPONIBLE = "DISPONIBLE"
    OCUPADA = "OCUPADA"
    MANTENIMIENTO = "MANTENIMIENTO"
    RESERVADA = "RESERVADA"

class Cell(Base):
    __tablename__ = "celdas"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(10), unique=True, nullable=False, index=True)
    tipo_permitido = Column(Enum(VehicleType), nullable=False)
    estado = Column(Enum(CellStatus), default=CellStatus.DISPONIBLE, nullable=False, index=True)
    zona_piso = Column(String(50), default="Piso 1", nullable=False)
    observaciones = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    movimientos = relationship("Movement", back_populates="celda")
    mensualidades_preferidas = relationship("Subscription", back_populates="celda_preferida")
