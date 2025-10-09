import pandas as pd

def plot_sueno_vs_fatiga(ax, df):
    """Correlación individual entre el sueño del día anterior y la fatiga del día actual."""
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['sueno_prev'] = df['sueno_score'].shift(1)
    ax.scatter(df['sueno_prev'], df['fatiga_score'], color='teal', alpha=0.6)
    ax.set_title("Sueño (T-1) vs Fatiga (T)")
    ax.set_xlabel("Calidad del Sueño (día anterior)")
    ax.set_ylabel("Fatiga (día actual)")
    ax.grid(True, linestyle='--', alpha=0.5)
