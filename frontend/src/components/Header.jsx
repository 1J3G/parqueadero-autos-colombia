import React from 'react';

export function Header({ onOpenEntry, onOpenExit }) {
  return (
    <header className="top-nav">
      <div className="logo-area">
        <div className="logo-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/>
            <circle cx="7" cy="17" r="2"/>
            <path d="M9 17h6"/>
            <circle cx="17" cy="17" r="2"/>
          </svg>
        </div>
        <div>
          <div className="brand-title">
            Parqueadero Autos Colombia
            <span className="brand-badge">Iteración 1</span>
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            Caseta de Control Operativo &middot; Servicio de Mensualidades
          </div>
        </div>
      </div>

      <div className="header-actions">
        <button 
          id="btn-open-entry"
          className="action-btn btn-primary" 
          onClick={onOpenEntry}
          title="Registrar Ingreso de Vehículo"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <path d="M12 5v14M5 12h14"/>
          </svg>
          Registrar Entrada
        </button>

        <button 
          id="btn-open-exit"
          className="action-btn btn-success" 
          onClick={onOpenExit}
          title="Registrar Salida de Vehículo"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          Registrar Salida
        </button>
      </div>
    </header>
  );
}
