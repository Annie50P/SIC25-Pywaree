import seaborn as sns

def plot_ejercicio_vs_isa(ax, df):
    """Box Plot de ISA en días con ejercicio vs sin ejercicio."""
    sns.boxplot(x='actividad_fisica', y='ISA', data=df, ax=ax, palette='coolwarm')
    ax.set_title("Ejercicio vs Malestar General (ISA)")
    ax.set_xlabel("Ejercicio (1=Sí, 0=No)")
    ax.set_ylabel("ISA")
