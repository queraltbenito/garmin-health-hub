"""Utilidades de fechas."""

from collections.abc import Iterator
from datetime import date, timedelta


def date_chunks(start: date, end: date, days: int) -> Iterator[tuple[date, date]]:
    """Divide [start, end] en tramos consecutivos de como máximo `days` días."""
    chunk_start = start
    while chunk_start <= end:
        chunk_end = min(chunk_start + timedelta(days=days - 1), end)
        yield chunk_start, chunk_end
        chunk_start = chunk_end + timedelta(days=1)