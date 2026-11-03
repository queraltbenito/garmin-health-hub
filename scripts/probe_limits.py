"""Experimento: ¿cuántos días por petición acepta la API y hasta dónde llega el histórico?"""

import os
import time
from datetime import date, timedelta

import requests
from dotenv import load_dotenv

from garmin_hub.api import get_sleep, get_token

if __name__ == "__main__":
    load_dotenv()
    token = get_token(os.environ["GARMIN_PERSONAL_API_KEY"])
    yesterday = date.today() - timedelta(days=1)

    print("1) Tamaño máximo del rango por petición")
    for days in [7, 30, 60, 90, 180, 365]:
        start = yesterday - timedelta(days=days - 1)
        try:
            nights = get_sleep(token, start, yesterday)
            print(f"   {days:>3} días → OK, {len(nights)} noches")
        except requests.HTTPError as err:
            print(f"   {days:>3} días → ERROR {err.response.status_code}")
        time.sleep(1)  # una pausa entre peticiones, por respeto a la API

    print("3) Mes a mes hacia atrás (tramos de 30 días)")
    end = yesterday
    for _ in range(14):
        start = end - timedelta(days=29)
        try:
            nights = get_sleep(token, start, end)
            print(f"   {start} → {end}: {len(nights)} noches")
        except requests.HTTPError as err:
            print(f"   {start} → {end}: ERROR {err.response.status_code}")
        end = start - timedelta(days=1)  # el siguiente tramo termina el día antes
        time.sleep(1)