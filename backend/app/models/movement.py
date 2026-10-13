import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class MovementStatus(str, enum.Enum):
    ACTIVO = "ACTIVO"
    FINALIZADO = "FINALIZADO"

class Movement(Base):
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=False)
    celda_id = Column(Integer, ForeignKey("celdas.id"), nullable=False)
    operario_entrada_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    operario_salida_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha_hora_entrada = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_hora_salida = Column(DateTime, nullable=True)
    estado = Column(Enum(MovementStatus), default=MovementStatus.ACTIVO, nullable=False, index=True)
    kilometraje_entrada = Column(Integer, nullable=True)
    kilometraje_salida = Column(Integer, nullable=True)
    observaciones = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    vehiculo = relationship("Vehicle", back_populates="movimientos")
    celda = relationship("Cell", back_populates="movimientos")
    operario_entrada = relationship("User", foreign_keys=[operario_entrada_id])
    operario_salida = relationship("User", foreign_keys=[operario_salida_id])
    novedades = relationship("Incident", back_populates="movimiento")
