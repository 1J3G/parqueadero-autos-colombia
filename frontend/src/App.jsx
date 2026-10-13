import React, { useState, useEffect, useCallback } from 'react';
import { api } from './api/client';
import { Header } from './components/Header';
import { SummaryMetrics } from './components/SummaryMetrics';
import { CellGrid } from './components/CellGrid';
import { ActiveVehiclesList } from './components/ActiveVehiclesList';
import { EntryModal } from './components/EntryModal';
import { ExitModal } from './components/ExitModal';

export function App() {
  const [cells, setCells] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [activeVehicles, setActiveVehicles] = useState([]);
  const [loading, setLoading] = useState(true);

  // Modales
  const [isEntryOpen, setIsEntryOpen] = useState(false);
  const [isExitOpen, setIsExitOpen] = useState(false);
  const [selectedCellForEntry, setSelectedCellForEntry] = useState(null);

  // Notificación tipo toast
  const [toastMessage, setToastMessage] = useState('');

  const showToast = (msg) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(''), 4500);
  };

  const loadDashboardData = useCallback(async () => {
    try {
      const [cellsData, metricsData, movementsData] = await Promise.all([
        api.getCells(),
        api.getMetrics(),
        api.getActiveMovements()
      ]);
      setCells(cellsData);
      setMetrics(metricsData);
      setActiveVehicles(movementsData);
    } catch (err) {
      console.error("Error al cargar datos del dashboard:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadDashboardData();
    // Polling ligero cada 10 segundos para actualizar estado en vivo
    const interval = setInterval(loadDashboardData, 10000);
    return () => clearInterval(interval);
  }, [loadDashboardData]);

  const handleCellSelectForEntry = (cell) => {
    setSelectedCellForEntry(cell);
    setIsEntryOpen(true);
  };

  const handleTriggerExit = (placa) => {
    setIsExitOpen(true);
  };

  return (
    <div className="app-layout">
      <Header 
        onOpenEntry={() => { setSelectedCellForEntry(null); setIsEntryOpen(true); }}
        onOpenExit={() => setIsExitOpen(true)}
      />

      <main className="main-content">
        {toastMessage && (
          <div className="info-banner success" style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>✅</span>
            <span>{toastMessage}</span>
          </div>
        )}

        <SummaryMetrics metrics={metrics} />

        <div className="dashboard-grid">
          <CellGrid 
            cells={cells} 
            onSelectCellForEntry={handleCellSelectForEntry}
          />

          <ActiveVehiclesList 
            activeVehicles={activeVehicles}
            onTriggerExit={handleTriggerExit}
          />
        </div>
      </main>

      {/* Modal de Entrada */}
      <EntryModal 
        isOpen={isEntryOpen}
        onClose={() => setIsEntryOpen(false)}
        onSuccess={(msg) => {
          showToast(msg);
          loadDashboardData();
        }}
        initialCell={selectedCellForEntry}
        availableCells={cells}
      />

      {/* Modal de Salida */}
      <ExitModal 
        isOpen={isExitOpen}
        onClose={() => setIsExitOpen(false)}
        onSuccess={(msg) => {
          showToast(msg);
          loadDashboardData();
        }}
        activeVehicles={activeVehicles}
      />
    </div>
  );
}

export default App;
