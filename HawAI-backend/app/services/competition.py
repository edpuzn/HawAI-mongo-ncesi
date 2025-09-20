# services/competition.py
from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
from typing import Any

router = APIRouter(prefix="/competition", tags=["competition"])

# Proje kökü (HawAI-backend) altındaki data dizinini hedefle
DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "competition.json"


def _load_data() -> Any:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Competition data not found: {DATA_PATH}")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/", summary="Get competition analysis (static)")
def get_competition():
    try:
        data = _load_data()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Competition data not found on server")
    return data


# Optional: small helper route for markdown rendering later
@router.get("/summary", summary="Get a short markdown summary")
def get_competition_summary():
    data = _load_data()
    hawai = data.get("hawai", {})
    summary = {
        "title": "HawAI Competitive Summary",
        "focus": hawai.get("focus"),
        "differentiators": hawai.get("differentiators", []),
    }
    return summary


