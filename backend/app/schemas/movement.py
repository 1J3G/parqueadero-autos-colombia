from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.models.movement import MovementStatus
from app.schemas.incident import IncidentCreate, IncidentResponse

class MovementEntryRequest(BaseModel):
    placa: str
    celda_id: int
    operario_id: int = 2
    kilometraje_entrada: Optional[int] = None
    observaciones: Optional[str] = None
    novedad: Optional[IncidentCreate] = None

class MovementExitRequest(BaseModel):
    placa: Optional[str] = None
    movimiento_id: Optional[int] = None
    operario_id: int = 2
    kilometraje_salida: Optional[int] = None
    observaciones: Optional[str] = None
    novedad_salida: Optional[IncidentCreate] = None

class MovementResponse(BaseModel):
    id: int
    vehiculo_id: int
    placa: str
    tipo_vehiculo: str
    celda_id: int
    celda_codigo: str
    operario_entrada_id: int
    operario_salida_id: Optional[int] = None
    fecha_hora_entrada: datetime
    fecha_hora_salida: Optional[datetime] = None
    tiempo_estadia_formato: Optional[str] = None
    estado: MovementStatus
    kilometraje_entrada: Optional[int] = None
    kilometraje_salida: Optional[int] = None
    observaciones: Optional[str] = None
    novedades: List[IncidentResponse] = []

    model_config = ConfigDict(from_attributes=True)
