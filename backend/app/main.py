from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import auth, transactions, dashboard, orange_money, export, ca

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Trésorier IA",
    description="Gestion intelligente de trésorerie pour PME Afrique de l'Ouest",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(orange_money.router, prefix="/api")
app.include_router(export.router, prefix="/api")
app.include_router(ca.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "tresorier-ia"}
