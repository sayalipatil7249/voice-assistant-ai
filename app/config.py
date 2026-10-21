"""Runtime configuration loaded from environment variables and an optional .env."""

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def _csv_setting(name: str, default: str) -> list[str]:
    return [item.strip() for item in os.getenv(name, default).split(",") if item.strip()]


CORS_ORIGINS = _csv_setting(
    "CORS_ORIGINS",
    "http://127.0.0.1:5500,http://localhost:5500,http://127.0.0.1:3000,http://localhost:3000",
)

voice_reference = Path(os.getenv("VOICE_REFERENCE_PATH", "en_v1_011.wav"))
VOICE_REFERENCE_PATH = (
    voice_reference if voice_reference.is_absolute() else PROJECT_ROOT / voice_reference
)
