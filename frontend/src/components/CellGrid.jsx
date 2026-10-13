import React, { useState } from 'react';

export function CellGrid({ cells, onSelectCellForEntry }) {
  const [filterType, setFilterType] = useState('ALL');

  const filteredCells = cells.filter(cell => {
    if (filterType === 'ALL') return true;
    if (filterType === 'CARRO') return cell.tipo_permitido === 'CARRO' || cell.tipo_permitido === 'CAMIONETA';
    if (filterType === 'MOTO') return cell.tipo_permitido === 'MOTO';
    return true;
  });

  return (
    <div className="glass-panel" style={{ height: '100%' }}>
      <div className="section-header">
        <div className="section-title">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="3" y="3" width="7" height="7"/>
            <rect x="14" y="3" width="7" height="7"/>
            <rect x="14" y="14" width="7" height="7"/>
            <rect x="3" y="14" width="7" height="7"/>
          </svg>
          Matriz de Celdas de Parqueo
        </div>

        <div className="filter-tabs">
          <button 
            className={`tab-btn ${filterType === 'ALL' ? 'active' : ''}`}
            onClick={() => setFilterType('ALL')}
          >
            Todas ({cells.length})
          </button>
          <button 
            className={`tab-btn ${filterType === 'CARRO' ? 'active' : ''}`}
            onClick={() => setFilterType('CARRO')}
          >
            Carros / Camionetas
          </button>
          <button 
            className={`tab-btn ${filterType === 'MOTO' ? 'active' : ''}`}
            onClick={() => setFilterType('MOTO')}
          >
            Motos
          </button>
        </div>
      </div>

      <div className="cells-container">
        {filteredCells.map(cell => {
          const statusClass = cell.estado.toLowerCase();
          const isOccupied = cell.estado === 'OCUPADA';
          const isFree = cell.estado === 'DISPONIBLE';

          return (
            <div 
              key={cell.id} 
              className={`cell-box ${statusClass}`}
              onClick={() => isFree && onSelectCellForEntry(cell)}
              title={isFree ? `Hacer clic para asignar celda ${cell.codigo}` : `Celda ${cell.codigo} (${cell.estado})`}
              style={{ cursor: isFree ? 'pointer' : 'default' }}
            >
              <div className="cell-header">
                <span className="cell-code">{cell.codigo}</span>
                <span className="cell-type-badge">{cell.tipo_permitido}</span>
              </div>

              <div>
                <span className="cell-status-text">{cell.estado}</span>
                {isOccupied && cell.vehiculo_actual && (
                  <div className="cell-plate-tag">
                    {cell.vehiculo_actual.placa}
                  </div>
                )}
                {isFree && (
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                    {cell.zona_piso}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
