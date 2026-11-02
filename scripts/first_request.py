import os
from datetime import date, timedelta

import requests
from dotenv import load_dotenv

BASE_URL = "https://personal.connectapi.garmin.com"
TOKEN_PATH = "/personalapitoken-service/personal-api/personal-api-key/token"
TIMEOUT = 30  # segundos

def get_token(api_key: str) -> str:
    "Cambia la clave larga por un token bearer (24h)"
    response = requests.post(
        BASE_URL + TOKEN_PATH,
        headers = {"Authorization": f"ApiKey {api_key}", "Accept" : "*/*"},
        timeout = TIMEOUT,
    )
    response.raise_for_status()
    return response.text.strip() #el token llega como texto plano


def get_sleep(token: str, start: str, end: str) -> list:
    "Resúmenes de sueño diario entre dos fechas (ambas incluidas)."
    response = requests.get(
        BASE_URL + "/sleep-service/sleep/dailySleepSummariesByDate",
        headers = {"Authorization": f"Bearer {token}"},
        params = {"startDate": start.isoformat(), "endDate": end.isoformat()},
        timeout = TIMEOUT,
    )
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    load_dotenv()  # lee el .env y lo carga en las variables de entorno
    api_key = os.environ["GARMIN_PERSONAL_API_KEY"]

    token = get_token(api_key)
    print("✔ Token obtenido")

    end = date.today() - timedelta(days=1)  # ayer
    start = end - timedelta(days=6)         # 7 días en total
    sleep = get_sleep(token, start, end)

    print(f"Tipo de respuesta: {type(sleep).__name__}")
    if isinstance(sleep, list) and sleep:
        print(f"Días recibidos: {len(sleep)}")
        print(f"Claves del primer día: {list(sleep[0].keys())}")
    else:
        print(sleep)