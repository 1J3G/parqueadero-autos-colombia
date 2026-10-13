import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class IncidentType(str, enum.Enum):
    RAYON = "RAYON"
    GOLPE = "GOLPE"
    ESPEJO_ROTO = "ESPEJO_ROTO"
    OBJETOS_VALOR = "OBJETOS_VALOR"
    MECANICA = "MECANICA"
    OTRO = "OTRO"

class IncidentSeverity(str, enum.Enum):
    LEVE = "LEVE"
    MODERADA = "MODERADA"
    GRAVE = "GRAVE"

class IncidentMoment(str, enum.Enum):
    ENTRADA = "ENTRADA"
    SALIDA = "SALIDA"
    PERMANENCIA = "PERMANENCIA"

class Incident(Base):
    __tablename__ = "novedades"

    id = Column(Integer, primary_key=True, index=True)
    movimiento_id = Column(Integer, ForeignKey("movimientos.id"), nullable=True)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=False)
    tipo_novedad = Column(Enum(IncidentType), nullable=False)
    severidad = Column(Enum(IncidentSeverity), default=IncidentSeverity.LEVE, nullable=False)
    descripcion = Column(Text, nullable=False)
    evidencia_url = Column(String(255), nullable=True)
    registrado_por_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    momento = Column(Enum(IncidentMoment), default=IncidentMoment.ENTRADA, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    movimiento = relationship("Movement", back_populates="novedades")
    vehiculo = relationship("Vehicle", back_populates="novedades")
    registrado_por = relationship("User", foreign_keys=[registrado_por_id])
