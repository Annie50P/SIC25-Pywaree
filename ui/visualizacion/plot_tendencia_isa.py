import pandas as pd

def plot_tendencia_isa(ax, df):
    """Promedio mensual del ISA (malestar general)."""
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['mes'] = df['fecha'].dt.to_period('M')
    promedio_mensual = df.groupby('mes')['ISA'].mean()
    promedio_mensual.plot(kind='bar', color='#673AB7', ax=ax)
    ax.set_title("Tendencia Mensual del Malestar (ISA)")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Promedio ISA")
    ax.grid(axis='y', linestyle='--', alpha=0.5)
