"""Descarga el sueño de los últimos 7 días, lo guarda en bruto y lo transforma."""

import os
from datetime import date, timedelta

from dotenv import load_dotenv

from garmin_hub.api import get_sleep, get_token
from garmin_hub.storage import save_raw
from garmin_hub.transform import parse_sleep_day

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

    rows = [parse_sleep_day(day) for day in sleep]
    print(f"Columnas por fila: {len(rows[0])}")
    for row in rows:
        print(
            row["calendarDate"],
            row["sleep_start_local"],
            row["total_sleep_h"],
            row["sleepScores_overall_value"],
        )