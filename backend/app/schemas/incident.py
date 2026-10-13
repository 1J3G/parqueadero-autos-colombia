from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models.incident import IncidentType, IncidentSeverity, IncidentMoment

class IncidentBase(BaseModel):
    tipo_novedad: IncidentType
    severidad: IncidentSeverity = IncidentSeverity.LEVE
    descripcion: str
    evidencia_url: Optional[str] = None
    momento: IncidentMoment = IncidentMoment.ENTRADA

class IncidentCreate(IncidentBase):
    vehiculo_id: Optional[int] = None
    registrado_por_id: Optional[int] = 2

class IncidentResponse(IncidentBase):
    id: int
    movimiento_id: Optional[int] = None
    vehiculo_id: int
    registrado_por_id: int
    fecha_registro: datetime

    model_config = ConfigDict(from_attributes=True)
