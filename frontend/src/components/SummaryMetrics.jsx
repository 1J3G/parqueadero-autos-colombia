import React from 'react';

export function SummaryMetrics({ metrics }) {
  if (!metrics) return null;

  return (
    <div className="metrics-grid">
      <div className="glass-panel metric-card">
        <div className="metric-icon-box blue">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="3" y="3" width="18" height="18" rx="2"/>
            <path d="M3 9h18M9 21V9"/>
          </svg>
        </div>
        <div>
          <div className="metric-label">Total Celdas</div>
          <div className="metric-value">{metrics.total_celdas}</div>
        </div>
      </div>

      <div className="glass-panel metric-card">
        <div className="metric-icon-box green">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"/>
            <path d="m9 12 2 2 4-4"/>
          </svg>
        </div>
        <div>
          <div className="metric-label">Celdas Libres</div>
          <div className="metric-value" style={{ color: 'var(--color-success)' }}>
            {metrics.disponibles}
          </div>
        </div>
      </div>

      <div className="glass-panel metric-card">
        <div className="metric-icon-box red">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="15" y1="9" x2="9" y2="15"/>
            <line x1="9" y1="9" x2="15" y2="15"/>
          </svg>
        </div>
        <div>
          <div className="metric-label">Ocupadas</div>
          <div className="metric-value" style={{ color: 'var(--color-danger)' }}>
            {metrics.ocupadas}
          </div>
        </div>
      </div>

      <div className="glass-panel metric-card">
        <div className="metric-icon-box amber">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
          </svg>
        </div>
        <div>
          <div className="metric-label">% Ocupación</div>
          <div className="metric-value" style={{ color: 'var(--color-warning)' }}>
            {metrics.porcentaje_ocupacion}%
          </div>
        </div>
      </div>
    </div>
  );
}
