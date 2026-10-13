from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models.vehicle import VehicleType, VehicleTransitStatus

class VehicleBase(BaseModel):
    placa: str
    tipo_vehiculo: VehicleType
    marca: str
    modelo: Optional[str] = None
    color: str

class VehicleResponse(VehicleBase):
    id: int
    cliente_id: int
    estado_actual: VehicleTransitStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class VehicleValidationResponse(BaseModel):
    vehiculo_id: int
    placa: str
    tipo_vehiculo: VehicleType
    marca: str
    modelo: Optional[str] = None
    color: str
    estado_actual: VehicleTransitStatus
    cliente_nombre: str
    cliente_documento: str
    cliente_telefono: str
    mensualidad_id: Optional[int] = None
    codigo_contrato: Optional[str] = None
    fecha_fin_mensualidad: Optional[date] = None
    estado_mensualidad: Optional[str] = None
    es_mensualidad_vigente: bool
    dias_restantes: Optional[int] = None
    celda_preferida_codigo: Optional[str] = None
    celda_sugerida_id: Optional[int] = None
    celda_sugerida_codigo: Optional[str] = None
    mensaje_alerta: Optional[str] = None
