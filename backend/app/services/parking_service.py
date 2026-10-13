from datetime import datetime, date
from typing import Optional, Tuple
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle, VehicleTransitStatus, VehicleType
from app.models.cell import Cell, CellStatus
from app.models.subscription import Subscription, SubscriptionStatus
from app.models.movement import Movement, MovementStatus
from app.models.incident import Incident, IncidentType, IncidentSeverity, IncidentMoment
from app.schemas.movement import MovementEntryRequest, MovementExitRequest
from app.schemas.vehicle import VehicleValidationResponse

class ParkingService:
    @staticmethod
    def validate_vehicle_for_entry(db: Session, placa: str) -> VehicleValidationResponse:
        placa_clean = placa.strip().upper()
        vehicle = db.query(Vehicle).filter(Vehicle.placa == placa_clean).first()
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El vehículo con placa '{placa_clean}' no se encuentra registrado en el sistema."
            )

        # Regla Anti-Passback: Validar si ya está dentro
        if vehicle.estado_actual == VehicleTransitStatus.DENTRO:
            # Buscar la celda actual donde se encuentra
            active_mov = db.query(Movement).filter(
                Movement.vehiculo_id == vehicle.id, 
                Movement.estado == MovementStatus.ACTIVO
            ).first()
            celda_nombre = active_mov.celda.codigo if active_mov and active_mov.celda else "desconocida"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Infracción Anti-Passback: El vehículo ya figura DENTRO del parqueadero en la celda {celda_nombre}."
            )

        # Validar contrato de mensualidad
        today = date.today()
        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.vehiculo_id == vehicle.id,
                Subscription.estado.in_([SubscriptionStatus.ACTIVA, SubscriptionStatus.PENDIENTE_PAGO])
            )
            .order_by(Subscription.fecha_fin.desc())
            .first()
        )

        es_vigente = False
        dias_restantes = None
        alerta = None
        subscription_id = None
        contrato_cod = None
        fecha_fin = None
        estado_mens = "SIN_CONTRATO"
        celda_preferida_cod = None

        if subscription:
            subscription_id = subscription.id
            contrato_cod = subscription.codigo_contrato
            fecha_fin = subscription.fecha_fin
            estado_mens = subscription.estado.value
            if subscription.celda_preferida:
                celda_preferida_cod = subscription.celda_preferida.codigo

            dias_restantes = (subscription.fecha_fin - today).days

            if dias_restantes >= 0 and subscription.estado == SubscriptionStatus.ACTIVA:
                es_vigente = True
                if dias_restantes <= 5:
                    alerta = f"Atención: La mensualidad vence en {dias_restantes} días ({subscription.fecha_fin})."
            else:
                alerta = f"Mensualidad Vencida: Venció hace {abs(dias_restantes)} días ({subscription.fecha_fin})."
        else:
            alerta = "El vehículo no tiene un contrato de mensualidad registrado o está cancelado."

        # Buscar celda sugerida (primero la fija si está disponible, o primera libre compatible)
        celda_sugerida_id = None
        celda_sugerida_codigo = None

        if subscription and subscription.celda_preferida and subscription.celda_preferida.estado == CellStatus.DISPONIBLE:
            celda_sugerida_id = subscription.celda_preferida.id
            celda_sugerida_codigo = subscription.celda_preferida.codigo
        else:
            # Buscar celda compatible libre
            compatible_cell = (
                db.query(Cell)
                .filter(Cell.tipo_permitido == vehicle.tipo_vehiculo, Cell.estado == CellStatus.DISPONIBLE)
                .order_by(Cell.codigo)
                .first()
            )
            if compatible_cell:
                celda_sugerida_id = compatible_cell.id
                celda_sugerida_codigo = compatible_cell.codigo

        return VehicleValidationResponse(
            vehiculo_id=vehicle.id,
            placa=vehicle.placa,
            tipo_vehiculo=vehicle.tipo_vehiculo,
            marca=vehicle.marca,
            modelo=vehicle.modelo,
            color=vehicle.color,
            estado_actual=vehicle.estado_actual,
            cliente_nombre=f"{vehicle.cliente.nombres} {vehicle.cliente.apellidos}",
            cliente_documento=vehicle.cliente.documento_identidad,
            cliente_telefono=vehicle.cliente.telefono,
            mensualidad_id=subscription_id,
            codigo_contrato=contrato_cod,
            fecha_fin_mensualidad=fecha_fin,
            estado_mensualidad=estado_mens,
            es_mensualidad_vigente=es_vigente,
            dias_restantes=dias_restantes,
            celda_preferida_codigo=celda_preferida_cod,
            celda_sugerida_id=celda_sugerida_id,
            celda_sugerida_codigo=celda_sugerida_codigo,
            mensaje_alerta=alerta
        )

    @staticmethod
    def register_entry(db: Session, entry_req: MovementEntryRequest) -> dict:
        placa_clean = entry_req.placa.strip().upper()
        
        # 1. Obtener y validar vehículo
        vehicle = db.query(Vehicle).filter(Vehicle.placa == placa_clean).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehículo no registrado.")
        
        if vehicle.estado_actual == VehicleTransitStatus.DENTRO:
            raise HTTPException(status_code=400, detail="El vehículo ya figura dentro del parqueadero.")

        # 2. Validar celda
        cell = db.query(Cell).filter(Cell.id == entry_req.celda_id).first()
        if not cell:
            raise HTTPException(status_code=404, detail="Celda de parqueo no encontrada.")
        
        if cell.estado != CellStatus.DISPONIBLE:
            raise HTTPException(status_code=400, detail=f"La celda {cell.codigo} no está disponible (Estado: {cell.estado.value}).")

        try:
            # 3. Crear movimiento
            movement = Movement(
                vehiculo_id=vehicle.id,
                celda_id=cell.id,
                operario_entrada_id=entry_req.operario_id,
                fecha_hora_entrada=datetime.now(),
                estado=MovementStatus.ACTIVO,
                kilometraje_entrada=entry_req.kilometraje_entrada,
                observaciones=entry_req.observaciones
            )
            db.add(movement)
            db.flush() # Obtener movement.id

            # 4. Actualizar estados
            cell.estado = CellStatus.OCUPADA
            vehicle.estado_actual = VehicleTransitStatus.DENTRO

            # 5. Si viene novedad al ingreso, registrarla
            novedad_creada = None
            if entry_req.novedad:
                incident = Incident(
                    movimiento_id=movement.id,
                    vehiculo_id=vehicle.id,
                    tipo_novedad=entry_req.novedad.tipo_novedad,
                    severidad=entry_req.novedad.severidad,
                    descripcion=entry_req.novedad.descripcion,
                    evidencia_url=entry_req.novedad.evidencia_url,
                    registrado_por_id=entry_req.operario_id,
                    momento=IncidentMoment.ENTRADA,
                    fecha_registro=datetime.now()
                )
                db.add(incident)
                db.flush()
                novedad_creada = {
                    "tipo": incident.tipo_novedad.value,
                    "severidad": incident.severidad.value,
                    "descripcion": incident.descripcion
                }

            db.commit()
            db.refresh(movement)

            return {
                "success": True,
                "mensaje": f"Entrada registrada exitosamente para el vehículo {vehicle.placa} en celda {cell.codigo}",
                "movimiento_id": movement.id,
                "placa": vehicle.placa,
                "cliente": f"{vehicle.cliente.nombres} {vehicle.cliente.apellidos}",
                "celda_codigo": cell.codigo,
                "fecha_hora_entrada": movement.fecha_hora_entrada.isoformat(),
                "novedad": novedad_creada
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error al registrar entrada: {str(e)}")

    @staticmethod
    def register_exit(db: Session, exit_req: MovementExitRequest) -> dict:
        movement = None
        if exit_req.movimiento_id:
            movement = db.query(Movement).filter(
                Movement.id == exit_req.movimiento_id,
                Movement.estado == MovementStatus.ACTIVO
            ).first()
        elif exit_req.placa:
            placa_clean = exit_req.placa.strip().upper()
            vehicle = db.query(Vehicle).filter(Vehicle.placa == placa_clean).first()
            if not vehicle:
                raise HTTPException(status_code=404, detail="Vehículo no encontrado.")
            movement = db.query(Movement).filter(
                Movement.vehiculo_id == vehicle.id,
                Movement.estado == MovementStatus.ACTIVO
            ).first()

        if not movement:
            raise HTTPException(
                status_code=404, 
                detail="No se encontró un registro de entrada activo para este vehículo."
            )

        try:
            now = datetime.now()
            movement.fecha_hora_salida = now
            movement.estado = MovementStatus.FINALIZADO
            movement.operario_salida_id = exit_req.operario_id
            if exit_req.kilometraje_salida:
                movement.kilometraje_salida = exit_req.kilometraje_salida
            if exit_req.observaciones:
                movement.observaciones = (movement.observaciones or "") + f" | Salida: {exit_req.observaciones}"

            # Liberar celda y cambiar estado vehículo
            cell = db.query(Cell).filter(Cell.id == movement.celda_id).first()
            if cell:
                cell.estado = CellStatus.DISPONIBLE

            vehicle = db.query(Vehicle).filter(Vehicle.id == movement.vehiculo_id).first()
            if vehicle:
                vehicle.estado_actual = VehicleTransitStatus.FUERA

            # Novedad a la salida
            if exit_req.novedad_salida:
                incident_out = Incident(
                    movimiento_id=movement.id,
                    vehiculo_id=vehicle.id,
                    tipo_novedad=exit_req.novedad_salida.tipo_novedad,
                    severidad=exit_req.novedad_salida.severidad,
                    descripcion=exit_req.novedad_salida.descripcion,
                    evidencia_url=exit_req.novedad_salida.evidencia_url,
                    registrado_por_id=exit_req.operario_id,
                    momento=IncidentMoment.SALIDA,
                    fecha_registro=now
                )
                db.add(incident_out)

            db.commit()

            # Calcular duración
            delta = now - movement.fecha_hora_entrada
            total_seconds = int(delta.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            tiempo_formato = f"{hours}h {minutes}m"

            return {
                "success": True,
                "mensaje": f"Salida registrada exitosamente. Celda {cell.codigo if cell else ''} liberada.",
                "movimiento_id": movement.id,
                "placa": vehicle.placa if vehicle else "",
                "cliente": f"{vehicle.cliente.nombres} {vehicle.cliente.apellidos}" if vehicle else "",
                "celda_liberada": cell.codigo if cell else "",
                "fecha_hora_entrada": movement.fecha_hora_entrada.isoformat(),
                "fecha_hora_salida": now.isoformat(),
                "tiempo_estadia": tiempo_formato
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error al registrar salida: {str(e)}")

    @staticmethod
    def get_active_movements(db: Session):
        movements = (
            db.query(Movement)
            .filter(Movement.estado == MovementStatus.ACTIVO)
            .order_by(Movement.fecha_hora_entrada.desc())
            .all()
        )
        data = []
        now = datetime.now()
        for m in movements:
            delta = now - m.fecha_hora_entrada
            total_seconds = int(delta.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            data.append({
                "id": m.id,
                "placa": m.vehiculo.placa,
                "vehiculo_marca": m.vehiculo.marca,
                "vehiculo_color": m.vehiculo.color,
                "tipo_vehiculo": m.vehiculo.tipo_vehiculo.value,
                "cliente_nombre": f"{m.vehiculo.cliente.nombres} {m.vehiculo.cliente.apellidos}",
                "celda_codigo": m.celda.codigo,
                "fecha_hora_entrada": m.fecha_hora_entrada.isoformat(),
                "tiempo_transcurrido": f"{hours}h {minutes}m",
                "observaciones": m.observaciones,
                "novedades_count": len(m.novedades)
            })
        return data
