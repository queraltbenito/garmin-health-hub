"""Descarga todo el histórico de sueño por tramos de 30 días. Se puede relanzar sin repetir trabajo."""

import os
import time
from datetime import date, timedelta

from dotenv import load_dotenv

from garmin_hub.api import get_sleep, get_token
from garmin_hub.dates import date_chunks
from garmin_hub.storage import raw_path, save_raw

START_DATE = date(2025, 10, 1)  # primeros datos: octubre de 2025
CHUNK_DAYS = 30  # la API acepta 30 días por petición, pero no 60
PAUSE_SECONDS = 1  # pausa entre peticiones

if __name__ == "__main__":
    load_dotenv()
    token = get_token(os.environ["GARMIN_PERSONAL_API_KEY"])
    yesterday = date.today() - timedelta(days=1)

    for start, end in date_chunks(START_DATE, yesterday, CHUNK_DAYS):
        is_last = end == yesterday
        if raw_path("sleep", start, end).exists() and not is_last:
            print(f"  ↷ {start} → {end}: ya descargado")
            continue

        nights = get_sleep(token, start, end)
        save_raw(nights, "sleep", start, end)
        print(f"  ✔ {start} → {end}: {len(nights)} noches")
        time.sleep(PAUSE_SECONDS)