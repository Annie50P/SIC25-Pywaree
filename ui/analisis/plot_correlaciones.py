import seaborn as sns


def plot_heatmap_correlaciones(ax, df):
    """Mapa de calor con correlaciones entre síntomas y factores."""
    columnas = [
        "dolor_score",
        "fatiga_score",
        "rigidez_score",
        "temperatura_C",
        "actividad_fisica",
        "sueno_score",
        "dieta_score",
        "clima_adverso",
        "estado_animo_score"
    ]
    df_corr = df[columnas].corr()
    sns.heatmap(df_corr, annot=True, cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Mapa de Correlaciones: Síntomas y Factores")
