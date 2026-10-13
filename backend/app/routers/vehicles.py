from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.vehicle import VehicleValidationResponse
from app.services.parking_service import ParkingService

router = APIRouter(prefix="/vehicles", tags=["Vehículos y Mensualidades"])

@router.get("/validate/{placa}", response_model=VehicleValidationResponse, summary="Validar placa y estado de mensualidad")
def validate_vehicle(placa: str, db: Session = Depends(get_db)):
    """
    Verifica si el vehículo está registrado, el estado de su mensualidad (vigente o vencida),
    regla anti-passback y la celda sugerida para parquear.
    """
    return ParkingService.validate_vehicle_for_entry(db=db, placa=placa)
