import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./tresorier_ia.db",
)
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30
ORANGE_MONEY_CLIENT_ID = os.getenv("ORANGE_MONEY_CLIENT_ID", "")
ORANGE_MONEY_CLIENT_SECRET = os.getenv("ORANGE_MONEY_CLIENT_SECRET", "")
ORANGE_MONEY_REDIRECT_URI = os.getenv(
    "ORANGE_MONEY_REDIRECT_URI", "http://localhost:8000/api/orange-money/callback"
)
