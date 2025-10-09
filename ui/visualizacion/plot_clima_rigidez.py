def plot_clima_vs_rigidez(ax, df):
    """Correlación entre temperatura (proxy del clima) y rigidez matutina."""
    ax.scatter(df['temperatura_C'], df['rigidez_score'], color='orange', alpha=0.6)
    ax.set_title("Temperatura vs Rigidez Matutina")
    ax.set_xlabel("Temperatura (°C)")
    ax.set_ylabel("Rigidez (0–5)")
    ax.grid(True, linestyle='--', alpha=0.5)
