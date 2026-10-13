import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    OPERARIO = "OPERARIO"
    CLIENTE = "CLIENTE"

class UserStatus(str, enum.Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    documento_identidad = Column(String(20), unique=True, nullable=False, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    rol = Column(Enum(UserRole), default=UserRole.CLIENTE, nullable=False)
    password_hash = Column(String(255), nullable=False, default="")
    estado = Column(Enum(UserStatus), default=UserStatus.ACTIVO, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    vehiculos = relationship("Vehicle", back_populates="cliente")
    mensualidades = relationship("Subscription", back_populates="cliente")
