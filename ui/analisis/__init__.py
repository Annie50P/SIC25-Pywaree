"""
Módulo central de visualizaciones del MAC (Motor de Análisis de Correlación).

Contiene funciones para:
- Dolor a través del tiempo
- Mapas de calor de correlaciones globales.
Cada función recibe:
    plot_func(ax, df)
Donde:
    ax -> matplotlib.axes.Axes
    df -> pandas.DataFrame con las columnas procesadas (ver analisis_datos/correlaciones.py)
"""

# ================================================================
# Importación de todas las funciones de visualización
# ================================================================
from .plot_dolor_tiempo import plot_dolor_tiempo
from .plot_correlaciones import plot_heatmap_correlaciones

# ================================================================
# Diccionario de acceso rápido (útil para menús dinámicos)
# ================================================================
PLOTS_ANALISIS = {
    "Distribucion del Dolor": plot_dolor_tiempo,
    "Mapa de Correlaciones": plot_heatmap_correlaciones,
}

# ================================================================
# Alias útiles para importación directa
# ================================================================
__all__ = [
    "plot_dolor_tiempo",
    "plot_heatmap_correlaciones",
    "PLOTS_ANALISIS",
]
