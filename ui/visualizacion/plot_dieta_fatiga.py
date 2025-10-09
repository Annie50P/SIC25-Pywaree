import seaborn as sns

def plot_dieta_vs_fatiga(ax, df):
    """Box Plot comparando fatiga según tipo de dieta."""
    sns.boxplot(x='dieta_tipo', y='fatiga_score', data=df, ax=ax, palette='Set2')
    ax.set_title("Dieta vs Fatiga")
    ax.set_xlabel("Tipo de Dieta")
    ax.set_ylabel("Nivel de Fatiga (0–5)")
