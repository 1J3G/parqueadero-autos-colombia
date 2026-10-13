const API_BASE_URL = 'http://localhost:8000/api';

export const api = {
  // Celdas
  async getCells(tipo = '') {
    const url = tipo ? `${API_BASE_URL}/cells?tipo=${tipo}` : `${API_BASE_URL}/cells`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Error al cargar celdas');
    return res.json();
  },

  async getMetrics() {
    const res = await fetch(`${API_BASE_URL}/cells/metrics`);
    if (!res.ok) throw new Error('Error al cargar métricas');
    return res.json();
  },

  // Vehículos
  async validatePlate(placa) {
    const res = await fetch(`${API_BASE_URL}/vehicles/validate/${encodeURIComponent(placa)}`);
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'Error al validar vehículo');
    }
    return data;
  },

  // Movimientos
  async getActiveMovements() {
    const res = await fetch(`${API_BASE_URL}/movements/active`);
    if (!res.ok) throw new Error('Error al consultar vehículos dentro');
    return res.json();
  },

  async registerEntry(payload) {
    const res = await fetch(`${API_BASE_URL}/movements/entry`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'Error al registrar entrada');
    }
    return data;
  },

  async registerExit(payload) {
    const res = await fetch(`${API_BASE_URL}/movements/exit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'Error al registrar salida');
    }
    return data;
  }
};
