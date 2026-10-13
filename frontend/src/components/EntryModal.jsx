import React, { useState, useEffect } from 'react';
import { api } from '../api/client';

export function EntryModal({ isOpen, onClose, onSuccess, initialCell, availableCells }) {
  const [placa, setPlaca] = useState('');
  const [loading, setLoading] = useState(false);
  const [validating, setValidating] = useState(false);
  const [validationData, setValidationData] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');

  const [selectedCellId, setSelectedCellId] = useState('');
  const [kilometraje, setKilometraje] = useState('');
  const [observaciones, setObservaciones] = useState('');

  // Novedades
  const [hasNovedad, setHasNovedad] = useState(false);
  const [tipoNovedad, setTipoNovedad] = useState('RAYON');
  const [severidad, setSeveridad] = useState('LEVE');
  const [descripcionNovedad, setDescripcionNovedad] = useState('');

  useEffect(() => {
    if (initialCell) {
      setSelectedCellId(initialCell.id);
    }
  }, [initialCell]);

  if (!isOpen) return null;

  const handleValidatePlate = async (e) => {
    e?.preventDefault();
    if (!placa.trim()) return;

    setValidating(true);
    setErrorMsg('');
    setValidationData(null);

    try {
      const data = await api.validatePlate(placa.trim().toUpperCase());
      setValidationData(data);
      if (data.celda_sugerida_id) {
        setSelectedCellId(data.celda_sugerida_id);
      }
    } catch (err) {
      setErrorMsg(err.message);
    } finally {
      setValidating(false);
    }
  };

  const handleRegisterEntry = async (e) => {
    e.preventDefault();
    if (!validationData) return;
    if (!selectedCellId) {
      setErrorMsg('Debe seleccionar una celda de parqueo.');
      return;
    }

    setLoading(true);
    setErrorMsg('');

    try {
      const payload = {
        placa: validationData.placa,
        celda_id: parseInt(selectedCellId),
        operario_id: 2,
        kilometraje_entrada: kilometraje ? parseInt(kilometraje) : null,
        observaciones: observaciones || null,
        novedad: hasNovedad ? {
          tipo_novedad: tipoNovedad,
          severidad: severidad,
          descripcion: descripcionNovedad,
          momento: 'ENTRADA'
        } : null
      };

      const result = await api.registerEntry(payload);
      onSuccess(result.mensaje);
      handleClose();
    } catch (err) {
      setErrorMsg(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setPlaca('');
    setValidationData(null);
    setErrorMsg('');
    setHasNovedad(false);
    setDescripcionNovedad('');
    setKilometraje('');
    setObservaciones('');
    onClose();
  };

  return (
    <div className="modal-overlay">
      <div className="modal-card">
        <div className="modal-header">
          <div className="modal-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <path d="M12 5v14M5 12h14"/>
            </svg>
            Registrar Entrada de Vehículo
          </div>
          <button className="modal-close" onClick={handleClose}>&times;</button>
        </div>

        <form onSubmit={handleRegisterEntry}>
          <div className="modal-body">
            {errorMsg && (
              <div className="info-banner danger">
                ⚠️ {errorMsg}
              </div>
            )}

            {/* Paso 1: Búsqueda por Placa */}
            <div className="form-group">
              <label className="form-label">Placa del Vehículo (Colombia):</label>
              <div style={{ display: 'flex', gap: '8px' }}>
                <input 
                  type="text" 
                  value={placa} 
                  onChange={(e) => setPlaca(e.target.value.toUpperCase())}
                  placeholder="Ej: HJR542 o ABC12D" 
                  style={{ flex: 1, textTransform: 'uppercase', fontSize: '1.1rem', fontWeight: 700, letterSpacing: '0.05em' }}
                  autoFocus
                />
                <button 
                  type="button" 
                  className="action-btn btn-secondary"
                  onClick={handleValidatePlate}
                  disabled={validating || !placa.trim()}
                >
                  {validating ? 'Buscando...' : 'Buscar Placa'}
                </button>
              </div>
            </div>

            {/* Resultado de Validación */}
            {validationData && (
              <>
                <div className={`info-banner ${validationData.es_mensualidad_vigente ? 'success' : 'danger'}`}>
                  <div style={{ fontWeight: 700, fontSize: '1rem', marginBottom: '4px' }}>
                    {validationData.cliente_nombre} &middot; {validationData.marca} ({validationData.color})
                  </div>
                  <div>Contrato: <strong>{validationData.codigo_contrato || 'N/A'}</strong></div>
                  <div>
                    Estado Mensualidad:{' '}
                    <strong>
                      {validationData.es_mensualidad_vigente 
                        ? `VIGENTE (Vence en ${validationData.dias_restantes} días - ${validationData.fecha_fin_mensualidad})`
                        : `VENCIDA / INACTIVA (${validationData.mensaje_alerta})`
                      }
                    </strong>
                  </div>
                </div>

                {/* Paso 2: Selección de Celda */}
                <div className="form-group">
                  <label className="form-label">Asignar Celda de Parqueo:</label>
                  <select 
                    value={selectedCellId} 
                    onChange={(e) => setSelectedCellId(e.target.value)}
                    required
                  >
                    <option value="">-- Seleccionar celda disponible --</option>
                    {availableCells
                      .filter(c => c.estado === 'DISPONIBLE')
                      .map(cell => (
                        <option key={cell.id} value={cell.id}>
                          {cell.codigo} ({cell.tipo_permitido} - {cell.zona_piso})
                        </option>
                      ))}
                  </select>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                  <div className="form-group">
                    <label className="form-label">Kilometraje Entrada (Opcional):</label>
                    <input 
                      type="number" 
                      value={kilometraje} 
                      onChange={(e) => setKilometraje(e.target.value)}
                      placeholder="Ej: 45000"
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Observaciones Generales:</label>
                    <input 
                      type="text" 
                      value={observaciones} 
                      onChange={(e) => setObservaciones(e.target.value)}
                      placeholder="Ej: Conductor autorizado"
                    />
                  </div>
                </div>

                {/* Paso 3: Registro de Novedad al Ingreso */}
                <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '14px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
                  <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontWeight: 600, fontSize: '0.9rem' }}>
                    <input 
                      type="checkbox" 
                      checked={hasNovedad} 
                      onChange={(e) => setHasNovedad(e.target.checked)}
                    />
                    Registrar Novedad Física en Vehículo (Rayón, Golpe o Daño preexistente)
                  </label>

                  {hasNovedad && (
                    <div style={{ marginTop: '12px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
                      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                        <div>
                          <label className="form-label">Tipo de Daño:</label>
                          <select value={tipoNovedad} onChange={(e) => setTipoNovedad(e.target.value)}>
                            <option value="RAYON">Rayón de Carrocería</option>
                            <option value="GOLPE">Golpe / Abolladura</option>
                            <option value="ESPEJO_ROTO">Espejo Roto</option>
                            <option value="OBJETOS_VALOR">Objetos de Valor a la vista</option>
                            <option value="MECANICA">Fuga o Falla Mecánica</option>
                            <option value="OTRO">Otro</option>
                          </select>
                        </div>
                        <div>
                          <label className="form-label">Severidad:</label>
                          <select value={severidad} onChange={(e) => setSeveridad(e.target.value)}>
                            <option value="LEVE">Leve</option>
                            <option value="MODERADA">Moderada</option>
                            <option value="GRAVE">Grave</option>
                          </select>
                        </div>
                      </div>
                      <div>
                        <label className="form-label">Detalle del estado del vehículo:</label>
                        <textarea 
                          rows="2" 
                          value={descripcionNovedad}
                          onChange={(e) => setDescripcionNovedad(e.target.value)}
                          placeholder="Describa el rayón, golpe o novedad encontrada al ingresar..."
                          required={hasNovedad}
                        />
                      </div>
                    </div>
                  )}
                </div>
              </>
            )}
          </div>

          <div className="modal-footer">
            <button type="button" className="action-btn btn-secondary" onClick={handleClose}>
              Cancelar
            </button>
            {validationData && (
              <button 
                type="submit" 
                className="action-btn btn-primary"
                disabled={loading || !selectedCellId || !validationData.es_mensualidad_vigente}
              >
                {loading ? 'Guardando...' : 'Confirmar Ingreso e Imprimir'}
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}
