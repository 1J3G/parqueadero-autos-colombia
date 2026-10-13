from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.cell import Cell, CellStatus
from app.models.vehicle import VehicleType, VehicleTransitStatus
from app.models.movement import Movement, MovementStatus
from app.models.vehicle import Vehicle

class CellService:
    @staticmethod
    def get_all_cells(db: Session, tipo: Optional[VehicleType] = None) -> List[dict]:
        query = db.query(Cell)
        if tipo:
            query = query.filter(Cell.tipo_permitido == tipo)
        cells = query.order_by(Cell.codigo).all()

        results = []
        for cell in cells:
            cell_data = {
                "id": cell.id,
                "codigo": cell.codigo,
                "tipo_permitido": cell.tipo_permitido.value,
                "estado": cell.estado.value,
                "zona_piso": cell.zona_piso,
                "observaciones": cell.observaciones,
                "created_at": cell.created_at,
                "updated_at": cell.updated_at,
                "vehiculo_actual": None
            }

            # Si está ocupada, adjuntar información del vehículo
            if cell.estado == CellStatus.OCUPADA:
                active_movement = (
                    db.query(Movement)
                    .filter(Movement.celda_id == cell.id, Movement.estado == MovementStatus.ACTIVO)
                    .first()
                )
                if active_movement and active_movement.vehiculo:
                    cell_data["vehiculo_actual"] = {
                        "placa": active_movement.vehiculo.placa,
                        "marca": active_movement.vehiculo.marca,
                        "modelo": active_movement.vehiculo.modelo,
                        "color": active_movement.vehiculo.color,
                        "fecha_hora_entrada": active_movement.fecha_hora_entrada.isoformat()
                    }

            results.append(cell_data)

        return results

    @staticmethod
    def get_cell_metrics(db: Session) -> dict:
        total = db.query(Cell).count()
        disponibles = db.query(Cell).filter(Cell.estado == CellStatus.DISPONIBLE).count()
        ocupadas = db.query(Cell).filter(Cell.estado == CellStatus.OCUPADA).count()
        mantenimiento = db.query(Cell).filter(Cell.estado == CellStatus.MANTENIMIENTO).count()
        reservadas = db.query(Cell).filter(Cell.estado == CellStatus.RESERVADA).count()

        libres_carros = db.query(Cell).filter(
            Cell.estado == CellStatus.DISPONIBLE, 
            Cell.tipo_permitido.in_([VehicleType.CARRO, VehicleType.CAMIONETA])
        ).count()

        libres_motos = db.query(Cell).filter(
            Cell.estado == CellStatus.DISPONIBLE, 
            Cell.tipo_permitido == VehicleType.MOTO
        ).count()

        porcentaje_ocupacion = round((ocupadas / total * 100), 1) if total > 0 else 0

        return {
            "total_celdas": total,
            "disponibles": disponibles,
            "ocupadas": ocupadas,
            "mantenimiento": mantenimiento,
            "reservadas": reservadas,
            "libres_carros": libres_carros,
            "libres_motos": libres_motos,
            "porcentaje_ocupacion": porcentaje_ocupacion
        }
