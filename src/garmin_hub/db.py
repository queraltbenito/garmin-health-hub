"""Escritura en la base de datos DuckDB."""

from pathlib import Path

import duckdb
import pandas as pd

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "garmin.duckdb"


def write_table(df: pd.DataFrame, table: str) -> None:
    """Crea (o reemplaza) una tabla en DuckDB con el contenido del DataFrame."""
    with duckdb.connect(str(DB_PATH)) as con:
        con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM df")