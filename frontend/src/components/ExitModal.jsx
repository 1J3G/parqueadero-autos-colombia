import React, { useState } from 'react';
import { api } from '../api/client';

export function ExitModal({ isOpen, onClose, onSuccess, activeVehicles }) {
  const [selectedPlaca, setSelectedPlaca] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [kilometrajeSalida, setKilometrajeSalida] = useState('');
  const [observaciones, setObservaciones] = useState('');

  if (!isOpen) return null;

  const currentVehicle = activeVehicles.find(v => v.placa === selectedPlaca);

  const handleRegisterExit = async (e) => {
    e.preventDefault();
    if (!selectedPlaca) {
      setErrorMsg('Seleccione un vehículo para registrar la salida.');
      return;
    }

    setLoading(true);
    setErrorMsg('');

    try {
      const payload = {
        placa: selectedPlaca,
        operario_id: 2,
        kilometraje_salida: kilometrajeSalida ? parseInt(kilometrajeSalida) : null,
        observaciones: observaciones || null
      };

      const result = await api.registerExit(payload);
      onSuccess(result.mensaje);
      handleClose();
    } catch (err) {
      setErrorMsg(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setSelectedPlaca('');
    setErrorMsg('');
    setKilometrajeSalida('');
    setObservaciones('');
    onClose();
  };

  return (
    <div className="modal-overlay">
      <div className="modal-card">
        <div className="modal-header">
          <div className="modal-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16 17 21 12 16 7"/>
              <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
            Registrar Salida de Vehículo
          </div>
          <button className="modal-close" onClick={handleClose}>&times;</button>
        </div>

        <form onSubmit={handleRegisterExit}>
          <div className="modal-body">
            {errorMsg && (
              <div className="info-banner danger">
                ⚠️ {errorMsg}
              </div>
            )}

            <div className="form-group">
              <label className="form-label">Seleccionar Vehículo dentro del Parqueadero:</label>
              <select 
                value={selectedPlaca} 
                onChange={(e) => setSelectedPlaca(e.target.value)}
                required
              >
                <option value="">-- Seleccionar vehículo por placa o celda --</option>
                {activeVehicles.map(v => (
                  <option key={v.id} value={v.placa}>
                    [{v.celda_codigo}] {v.placa} - {v.cliente_nombre} ({v.vehiculo_marca}) &middot; Tiempo: {v.tiempo_transcurrido}
                  </option>
                ))}
              </select>
            </div>

            {currentVehicle && (
              <div className="info-banner success" style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                <div><strong>Placa:</strong> {currentVehicle.placa} ({currentVehicle.vehiculo_marca} - {currentVehicle.vehiculo_color})</div>
                <div><strong>Propietario:</strong> {currentVehicle.cliente_nombre}</div>
                <div><strong>Celda a Liberar:</strong> {currentVehicle.celda_codigo}</div>
                <div><strong>Hora de Ingreso:</strong> {new Date(currentVehicle.fecha_hora_entrada).toLocaleTimeString()}</div>
                <div><strong>Tiempo de Estadía:</strong> {currentVehicle.tiempo_transcurrido}</div>
                {currentVehicle.novedades_count > 0 && (
                  <div style={{ color: '#fcd34d', fontWeight: 600 }}>
                    ⚠️ Este vehículo tiene {currentVehicle.novedades_count} novedad(es) registrada(s) al ingreso.
                  </div>
                )}
              </div>
            )}

            {currentVehicle && (
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                <div className="form-group">
                  <label className="form-label">Kilometraje Salida (Opcional):</label>
                  <input 
                    type="number" 
                    value={kilometrajeSalida} 
                    onChange={(e) => setKilometrajeSalida(e.target.value)}
                    placeholder="Ej: 45050"
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Observaciones de Salida:</label>
                  <input 
                    type="text" 
                    value={observaciones} 
                    onChange={(e) => setObservaciones(e.target.value)}
                    placeholder="Ej: Sin novedades al salir"
                  />
                </div>
              </div>
            )}
          </div>

          <div className="modal-footer">
            <button type="button" className="action-btn btn-secondary" onClick={handleClose}>
              Cancelar
            </button>
            <button 
              type="submit" 
              className="action-btn btn-success"
              disabled={loading || !selectedPlaca}
            >
              {loading ? 'Liberando...' : 'Confirmar Salida y Liberar Celda'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
