import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class VehicleType(str, enum.Enum):
    CARRO = "CARRO"
    MOTO = "MOTO"
    CAMIONETA = "CAMIONETA"
    ESPECIAL = "ESPECIAL"

class VehicleTransitStatus(str, enum.Enum):
    DENTRO = "DENTRO"
    FUERA = "FUERA"

class Vehicle(Base):
    __tablename__ = "vehiculos"

    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String(10), unique=True, nullable=False, index=True)
    tipo_vehiculo = Column(Enum(VehicleType), nullable=False)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=True)
    color = Column(String(30), nullable=False)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    estado_actual = Column(Enum(VehicleTransitStatus), default=VehicleTransitStatus.FUERA, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    cliente = relationship("User", back_populates="vehiculos")
    mensualidades = relationship("Subscription", back_populates="vehiculo")
    movimientos = relationship("Movement", back_populates="vehiculo")
    novedades = relationship("Incident", back_populates="vehiculo")
