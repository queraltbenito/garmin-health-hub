"""Reconstruye la base de datos a partir de los datos en bruto (no llama a la API)."""

import pandas as pd

from garmin_hub.db import write_table
from garmin_hub.storage import load_raw
from garmin_hub.transform import parse_sleep_day

if __name__ == "__main__":
    rows = [parse_sleep_day(day) for day in load_raw("sleep")]

    df = pd.DataFrame(rows)
    df = df.drop_duplicates(subset="calendarDate", keep="last")
    df["calendarDate"] = pd.to_datetime(df["calendarDate"]).dt.date

    write_table(df, "sleep")
    print(f"✔ Tabla sleep: {len(df)} noches, {len(df.columns)} columnas")