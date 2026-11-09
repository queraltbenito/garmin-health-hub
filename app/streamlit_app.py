"""Dashboard de sueño con los datos de Garmin."""

import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st

from garmin_hub.db import DB_PATH

st.set_page_config(page_title="Garmin Health Hub", layout="wide")
st.title("Mi sueño")


@st.cache_data(ttl=600)
def load_sleep() -> pd.DataFrame:
    """Lee de DuckDB solo las columnas que necesita el dashboard."""
    query = """
        SELECT
            calendarDate              AS date,
            total_sleep_h,
            sleepScores_overall_value AS sleep_score,
            deepSleepSeconds  / 3600  AS deep_h,
            lightSleepSeconds / 3600  AS light_h,
            remSleepSeconds   / 3600  AS rem_h,
            awakeSleepSeconds / 3600  AS awake_h
        FROM sleep
        ORDER BY calendarDate
    """
    with duckdb.connect(str(DB_PATH), read_only=True) as con:
        return con.sql(query).df()


df = load_sleep()

# Filtro de fechas en la barra lateral
first, last = df["date"].min().date(), df["date"].max().date()
selected = st.sidebar.date_input("Fechas", (first, last), min_value=first, max_value=last)
if len(selected) != 2:
    st.stop()
start, end = selected
view = df[df["date"].between(pd.Timestamp(start), pd.Timestamp(end))].copy()

# Indicadores
col1, col2, col3 = st.columns(3)
col1.metric("Noches", len(view))
col2.metric("Horas de sueño (media)", f"{view['total_sleep_h'].mean():.1f} h")
col3.metric("Nota de sueño (media)", f"{view['sleep_score'].mean():.0f}")

# Gráfico de horas con media móvil de 7 días
view["media_7_dias"] = view["total_sleep_h"].rolling(7, min_periods=1).mean()
fig = px.line(
    view,
    x="date",
    y=["total_sleep_h", "media_7_dias"],
    labels={"date": "", "value": "Horas", "variable": ""},
    title="Horas de sueño por noche",
)
st.plotly_chart(fig, width="stretch")