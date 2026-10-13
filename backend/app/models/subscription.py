import enum
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Enum, DateTime, Date, Numeric, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class SubscriptionStatus(str, enum.Enum):
    ACTIVA = "ACTIVA"
    VENCIDA = "VENCIDA"
    CANCELADA = "CANCELADA"
    PENDIENTE_PAGO = "PENDIENTE_PAGO"

class Subscription(Base):
    __tablename__ = "mensualidades"

    id = Column(Integer, primary_key=True, index=True)
    codigo_contrato = Column(String(30), unique=True, nullable=False, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=False)
    celda_preferida_id = Column(Integer, ForeignKey("celdas.id"), nullable=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    valor_mensual = Column(Numeric(10, 2), nullable=False)
    estado = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVA, nullable=False)
    observaciones = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    cliente = relationship("User", back_populates="mensualidades")
    vehiculo = relationship("Vehicle", back_populates="mensualidades")
    celda_preferida = relationship("Cell", back_populates="mensualidades_preferidas")
