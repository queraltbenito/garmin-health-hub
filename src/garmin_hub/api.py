"""Cliente mínimo de la Garmin Personal API."""

from datetime import date

import requests

BASE_URL = "https://personal.connectapi.garmin.com"
TOKEN_PATH = "/personalapitoken-service/personal-api/personal-api-key/token"
TIMEOUT = 30  # segundos


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