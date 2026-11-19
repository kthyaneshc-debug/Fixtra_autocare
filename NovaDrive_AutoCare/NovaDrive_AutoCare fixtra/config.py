import os
from pathlib import Path

from dotenv import load_dotenv

# Load local environment variables from the project directory.
load_dotenv(Path(__file__).resolve().parent / ".env")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
}

DATABASE_NAME = os.getenv("DB_NAME", "novadrive_autocare_db")
SHOP_NAME = "Fixtra AutoCare"
SHOP_TAGLINE = "Smart Service. Safer Journeys."
