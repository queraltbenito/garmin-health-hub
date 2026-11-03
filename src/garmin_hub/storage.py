"""Guardado de datos en disco."""

import json
from datetime import date
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"


def save_raw(data: list, dataset: str, start: date, end: date) -> Path:
    """Guarda la respuesta de la API tal cual en data/raw/<dataset>/<start>_<end>.json."""
    folder = RAW_DIR / dataset
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{start}_{end}.json"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    return path

def load_raw(dataset: str) -> list:
    """Lee todos los JSON de data/raw/<dataset>/ y junta sus registros en una lista."""
    records = []
    for path in sorted((RAW_DIR / dataset).glob("*.json")):
        records.extend(json.loads(path.read_text()))
    return records