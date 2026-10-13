from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models.cell import CellStatus
from app.models.vehicle import VehicleType

class CellBase(BaseModel):
    codigo: str
    tipo_permitido: VehicleType
    estado: CellStatus = CellStatus.DISPONIBLE
    zona_piso: str = "Piso 1"
    observaciones: Optional[str] = None

class CellResponse(CellBase):
    id: int
    created_at: datetime
    updated_at: datetime
    vehiculo_actual: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)

class CellStatusUpdate(BaseModel):
    estado: CellStatus
    observaciones: Optional[str] = None
