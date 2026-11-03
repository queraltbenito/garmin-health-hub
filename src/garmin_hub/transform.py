"""Transformación del JSON de Garmin en filas para las tablas."""

import json
from datetime import datetime, timezone


def flatten(data: dict, prefix: str = "") -> dict:
    """Aplana un diccionario anidado: {'a': {'b': 1}} -> {'a_b': 1}."""
    flat = {}
    for key, value in data.items():
        name = f"{prefix}_{key}" if prefix else key
        if isinstance(value, dict):
            flat.update(flatten(value, name))
        elif isinstance(value, list):
            flat[name] = json.dumps(value)
        else:
            flat[name] = value
    return flat


def ms_to_local(ms: int | None) -> datetime | None:
    """Convierte un timestamp 'Local' de Garmin (ms) en la hora de reloj."""
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).replace(tzinfo=None)


def seconds_to_hours(seconds: int | None) -> float | None:
    """Pasa segundos a horas con 2 decimales; None si falta el dato."""
    if seconds is None:
        return None
    return round(seconds / 3600, 2)


def parse_sleep_day(day: dict) -> dict:
    """Todos los campos de una noche, aplanados, más columnas calculadas útiles."""
    row = flatten(day)
    row["sleep_start_local"] = ms_to_local(day.get("sleepStartTimestampLocal"))
    row["sleep_end_local"] = ms_to_local(day.get("sleepEndTimestampLocal"))
    row["total_sleep_h"] = seconds_to_hours(day.get("sleepTimeSeconds"))
    return row