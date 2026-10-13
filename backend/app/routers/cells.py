from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.vehicle import VehicleType
from app.services.cell_service import CellService

router = APIRouter(prefix="/cells", tags=["Celdas y Aforo"])

@router.get("", summary="Listar todas las celdas con estado actual")
def get_cells(tipo: Optional[VehicleType] = None, db: Session = Depends(get_db)):
    return CellService.get_all_cells(db=db, tipo=tipo)

@router.get("/metrics", summary="Obtener métricas de ocupación y aforo")
def get_metrics(db: Session = Depends(get_db)):
    return CellService.get_cell_metrics(db=db)
