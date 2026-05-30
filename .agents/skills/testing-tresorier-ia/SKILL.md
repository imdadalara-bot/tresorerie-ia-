---
name: testing-tresorier-ia
description: End-to-end testing of the Trésorier IA SaaS app. Use when verifying registration, transactions, dashboard, forecast, or settings UI.
---

# Testing Trésorier IA

## Prerequisites

- Python 3.12 with pip
- Node.js with npm
- No external secrets needed for local testing (SQLite used by default)

## Setup

1. **Start backend**:
   ```bash
   rm -f tresorier_ia.db  # Fresh DB for clean testing
   cd backend && pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   ```

2. **Start frontend** (in separate shell):
   ```bash
   cd frontend && npm install && npm run dev
   ```
   Frontend runs on http://localhost:5173 and proxies `/api` to backend via vite.config.js.

## Key Test Flows

### Registration
- Navigate to http://localhost:5173
- Default view is Login. Click "Créer un compte" to switch to Register.
- Fill: Nom, Email, Téléphone (optional), Mot de passe, Secteur (dropdown), Devise (dropdown)
- On success: auto-redirects to Dashboard
- **Note**: The `@` character in email fields may not type correctly via computer-use tools. Use browser console to set email value:
  ```js
  document.querySelector('#reg-email').value = 'user@test.com';
  document.querySelector('#reg-email').dispatchEvent(new Event('input', {bubbles: true}));
  ```

### Dashboard Verification
- Empty state: 0 XOF balance, 0 weekly, green risk, alert "Pas assez de données"
- With data: Balance = income - expense, weekly summary computed, 15-day forecast with confidence %, risk level (green/yellow/red)
- Forecast algorithm: linear regression + day-of-week seasonality, confidence decays 3%/day

### Add Transaction
- Click "Ajouter" tab
- Toggle between "+ Entrée" (green, income) and "- Sortie" (red, expense)
- Enter amount, date (defaults to today), optional note
- On success: shows green "Transaction ajoutée !" then auto-navigates to Dashboard after 1s

### History
- Click "Historique" tab
- Shows transactions with amounts (green for income, red for expense), dates, notes
- Period selector: 7j / 30j / 90j (30j active by default)
- PDF export button available

### Settings
- Click "Réglages" tab
- Profile section: name, sector, currency editable
- Orange Money section: stub integration (not connected in dev)
- App info: version display

### Logout/Login
- Click "Déconnexion" in header
- **Known behavior**: After logout, the app shows the Register form (not Login). User must click "Se connecter" to switch.
- Login with email + password → Dashboard loads with persisted data

## API Endpoints (for shell-based testing)

- `POST /api/auth/register` — Register user
- `POST /api/auth/login` — Login, returns JWT
- `GET /api/auth/me` — Current user (requires Bearer token)
- `GET /api/dashboard` — Dashboard data with forecast
- `POST /api/transactions` — Add transaction
- `GET /api/transactions?days=30` — List transactions
- `GET /api/export/pdf?days=30` — Download PDF report

## Devin Secrets Needed

None for local testing. SQLite is used by default.
