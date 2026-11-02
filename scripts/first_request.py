"""Primera petición a la Garmin Personal API: clave → token → datos de sueño."""

import json
import os
from datetime import date, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

BASE_URL = "https://personal.connectapi.garmin.com"
TOKEN_PATH = "/personalapitoken-service/personal-api/personal-api-key/token"
TIMEOUT = 30  # segundos
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"


def get_token(api_key: str) -> str:
    """Cambia la clave (larga duración) por un token bearer (24 h)."""
    response = requests.post(
        BASE_URL + TOKEN_PATH,
        headers={"Authorization": f"ApiKey {api_key}", "Accept": "*/*"},
        timeout=TIMEOUT,
    )
    if not response.ok:
        print(f"Error {response.status_code}: {response.text}")
    response.raise_for_status()
    return response.text.strip()


def get_sleep(token: str, start: date, end: date) -> list:
    """Resúmenes de sueño diarios entre dos fechas (ambas incluidas)."""
    response = requests.get(
        BASE_URL + "/sleep-service/sleep/dailySleepSummariesByDate",
        headers={"Authorization": f"Bearer {token}"},
        params={"startDate": start.isoformat(), "endDate": end.isoformat()},
        timeout=TIMEOUT,
    )
    if not response.ok:
        print(f"Error {response.status_code}: {response.text}")
    response.raise_for_status()
    return response.json()


def save_raw(data: list, dataset: str, start: date, end: date) -> Path:
    """Guarda la respuesta de la API tal cual en data/raw/<dataset>/<start>_<end>.json."""
    folder = RAW_DIR / dataset
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{start}_{end}.json"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    return path


if __name__ == "__main__":
    load_dotenv()
    api_key = os.environ["GARMIN_PERSONAL_API_KEY"]

    token = get_token(api_key)
    print("✔ Token obtenido")

    end = date.today() - timedelta(days=1)  # ayer
    start = end - timedelta(days=6)  # 7 días en total
    sleep = get_sleep(token, start, end)

    path = save_raw(sleep, "sleep", start, end)
    print(f"✔ Guardado en {path}")

    print(f"Días recibidos: {len(sleep)}")
    print(f"Claves del primer día: {list(sleep[0].keys())}")