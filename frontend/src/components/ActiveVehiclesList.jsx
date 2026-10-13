import React from 'react';

export function ActiveVehiclesList({ activeVehicles, onTriggerExit }) {
  return (
    <div className="glass-panel" style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div className="section-header">
        <div className="section-title">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/>
            <circle cx="7" cy="17" r="2"/>
            <path d="M9 17h6"/>
            <circle cx="17" cy="17" r="2"/>
          </svg>
          Vehículos Adentro ({activeVehicles.length})
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', overflowY: 'auto', flex: 1, paddingRight: '4px' }}>
        {activeVehicles.length === 0 ? (
          <div style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '30px 10px', fontSize: '0.9rem' }}>
            No hay vehículos dentro del parqueadero en este momento.
          </div>
        ) : (
          activeVehicles.map(veh => (
            <div 
              key={veh.id}
              style={{
                background: 'rgba(255, 255, 255, 0.03)',
                border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-sm)',
                padding: '12px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}
            >
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span className="cell-plate-tag" style={{ margin: 0 }}>{veh.placa}</span>
                  <span style={{ fontSize: '0.8rem', color: '#60a5fa', fontWeight: 600 }}>
                    Celda {veh.celda_codigo}
                  </span>
                </div>
                <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                  {veh.cliente_nombre} &middot; {veh.vehiculo_marca}
                </div>
                <div style={{ fontSize: '0.75rem', color: '#34d399', marginTop: '2px' }}>
                  ⏱️ Estadía: {veh.tiempo_transcurrido}
                </div>
              </div>

              <button 
                className="action-btn btn-secondary"
                style={{ padding: '6px 10px', fontSize: '0.78rem' }}
                onClick={() => onTriggerExit(veh.placa)}
                title="Registrar salida de este vehículo"
              >
                Salida
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
