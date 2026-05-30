# Trésorier IA

> Gestion intelligente de trésorerie pour PME en Afrique de l'Ouest

**"Voir chaque matin ta trésorerie réelle et savoir si tu vas avoir assez cette semaine."**

## Features

- **Dashboard temps réel** — Solde du jour, flux hebdomadaire, prédiction 15 jours
- **Saisie rapide** — Ajoutez vos entrées/sorties en 2 champs
- **Agent IA de prévision** — Prédit votre solde à 15 jours (régression linéaire + saisonnalité jour-de-semaine)
- **Alertes intelligentes** — Notification si risque de solde négatif
- **Orange Money** — Intégration OAuth2 pour sync automatique
- **Mode hors-ligne** — IndexedDB + Service Worker (PWA)
- **Export PDF** — Rapport financier pour banques/microfinance
- **Mobile-first** — Interface ultra-légère (<50KB), optimisée 2G/3G

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Svelte 4 + TailwindCSS + Vite |
| Backend | Python 3.12 + FastAPI |
| Database | PostgreSQL |
| Auth | JWT (jose) + bcrypt |
| AI Agent | NumPy (linear regression + day-of-week seasonality) |
| Offline | IndexedDB + Service Worker (PWA) |
| Deploy | Docker Compose |

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set up database
createdb tresorier_ia
# Or use Docker: docker run -d -p 5432:5432 -e POSTGRES_USER=tresorier -e POSTGRES_PASSWORD=tresorier -e POSTGRES_DB=tresorier_ia postgres:16-alpine

# Configure
cp .env.example .env
# Edit .env with your settings

# Run
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Docker Compose (recommended)

```bash
docker-compose up -d
```

App available at `http://localhost:5173`, API at `http://localhost:8000/docs`.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/register` | Créer un compte |
| POST | `/api/auth/login` | Se connecter |
| GET | `/api/auth/me` | Profil utilisateur |
| GET | `/api/transactions` | Liste des transactions |
| POST | `/api/transactions` | Ajouter une transaction |
| DELETE | `/api/transactions/{id}` | Supprimer une transaction |
| GET | `/api/dashboard` | Dashboard + forecast IA |
| PUT | `/api/dashboard/profile` | Mettre à jour le profil |
| GET | `/api/orange-money/auth-url` | URL OAuth Orange Money |
| POST | `/api/orange-money/callback` | Callback OAuth |
| GET | `/api/orange-money/status` | Statut connexion |
| POST | `/api/orange-money/sync` | Synchroniser transactions |
| GET | `/api/export/pdf` | Exporter rapport PDF |

## AI Forecast Agent

The forecast agent predicts cash balance 15 days ahead using:

1. **Daily net flow aggregation** — Computes income - expenses per day
2. **Day-of-week averages** — Identifies patterns (e.g., Wednesdays = supplier payments)
3. **Linear trend** — Detects growth/decline with dampened extrapolation
4. **Risk assessment** — LOW / MEDIUM / HIGH based on predicted shortfalls

Works with as few as 7 days of data. No ML model needed — simple, explainable, fast (<100ms).

## Pricing (Production)

| Tier | Price | Features |
|------|-------|----------|
| Free | 0 FCFA | 1 compte, 30j historique |
| Pro | 2,000 FCFA/mois (~3€) | 3+ comptes, 1 an historique, notifications, export PDF |
| Enterprise | 33,000 FCFA/mois (~50€) | Illimité, API, white-label |

## Target Market

- Small retailers (épiceries, quincailleries) — Dakar, Abidjan
- Small-scale farmers (1-5 hectares) — Senegal, Ivory Coast
- Small restaurants/hotels — West Africa

## License

MIT
