from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.movement import MovementEntryRequest, MovementExitRequest
from app.services.parking_service import ParkingService

router = APIRouter(prefix="/movements", tags=["Movimientos de Entrada y Salida"])

@router.get("/active", summary="Listar vehículos que están actualmente dentro del parqueadero")
def get_active_movements(db: Session = Depends(get_db)):
    return ParkingService.get_active_movements(db=db)

@router.post("/entry", status_code=status.HTTP_201_CREATED, summary="Registrar entrada de vehículo")
def register_entry(request: MovementEntryRequest, db: Session = Depends(get_db)):
    """
    Registra el ingreso de un vehículo, valida la disponibilidad de la celda,
    cambia los estados a OCUPADA/DENTRO y registra novedades si existen.
    """
    return ParkingService.register_entry(db=db, entry_req=request)

@router.post("/exit", summary="Registrar salida de vehículo")
def register_exit(request: MovementExitRequest, db: Session = Depends(get_db)):
    """
    Registra la salida del vehículo por placa o ID de movimiento, calcula
    tiempo de estadía, libera la celda y cambia el estado a FUERA.
    """
    return ParkingService.register_exit(db=db, exit_req=request)
