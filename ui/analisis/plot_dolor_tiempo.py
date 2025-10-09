import matplotlib.dates as mdates
import pandas as pd


def plot_dolor_tiempo(ax, df):
    """Histograma de los niveles de dolor a lo largo del tiempo."""
    df["fecha"] = pd.to_datetime(df["fecha"])
    ax.bar(df["fecha"], df["dolor_score"], color="#4B0082", alpha=0.7)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b"))
    ax.set_title("Distribución Diaria del Dolor")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Nivel de Dolor (0–5)")
    ax.grid(True, linestyle="--", alpha=0.5)
