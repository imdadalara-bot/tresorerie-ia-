const API_BASE = '/api';

function getToken() {
  return localStorage.getItem('token');
}

async function request(path, options = {}) {
  const token = getToken();
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Erreur réseau' }));
    throw new Error(error.detail || `Erreur ${res.status}`);
  }

  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  // Auth
  register: (data) => request('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
  login: (data) => request('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  getMe: () => request('/auth/me'),

  // Transactions
  getTransactions: (days = 30) => request(`/transactions?days=${days}`),
  addTransaction: (data) => request('/transactions', { method: 'POST', body: JSON.stringify(data) }),
  deleteTransaction: (id) => request(`/transactions/${id}`, { method: 'DELETE' }),

  // Dashboard
  getDashboard: () => request('/dashboard'),
  updateProfile: (data) => request('/dashboard/profile', { method: 'PUT', body: JSON.stringify(data) }),

  // Orange Money
  getOmStatus: () => request('/orange-money/status'),
  getOmAuthUrl: () => request('/orange-money/auth-url'),
  syncOm: () => request('/orange-money/sync', { method: 'POST' }),

  // Export
  exportPdf: (days = 30) => {
    const token = getToken();
    return fetch(`${API_BASE}/export/pdf?days=${days}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
  },
};
