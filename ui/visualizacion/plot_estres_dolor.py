def plot_estres_vs_dolor(ax, df):
    """Correlación entre estrés (estado de ánimo bajo) y dolor articular."""
    ax.scatter(df['estado_animo_score'], df['dolor_score'], color='crimson', alpha=0.6)
    ax.set_title("Estrés / Estado de Ánimo vs Dolor Articular")
    ax.set_xlabel("Nivel de Estrés / Ánimo")
    ax.set_ylabel("Nivel de Dolor (0–5)")
    ax.grid(True, linestyle='--', alpha=0.5)
