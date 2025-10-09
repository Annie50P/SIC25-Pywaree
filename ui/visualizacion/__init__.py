"""
Módulo central de visualizaciones del MAC (Motor de Análisis de Correlación).

Contiene funciones para:
- Distribución y tendencia de síntomas.
- Correlaciones individuales (sueño, estrés, clima, dieta, ejercicio).
Cada función recibe:
    plot_func(ax, df)
Donde:
    ax -> matplotlib.axes.Axes
    df -> pandas.DataFrame con las columnas procesadas (ver analisis_datos/correlaciones.py)
"""

# ================================================================
# Importación de todas las funciones de visualización
# ================================================================
from .plot_tendencia_isa import plot_tendencia_isa
from .plot_sueno_fatiga import plot_sueno_vs_fatiga
from .plot_estres_dolor import plot_estres_vs_dolor
from .plot_dieta_fatiga import plot_dieta_vs_fatiga
from .plot_clima_rigidez import plot_clima_vs_rigidez
from .plot_ejercicio_isa import plot_ejercicio_vs_isa

# ================================================================
# Diccionario de acceso rápido (útil para menús dinámicos)
# ================================================================
PLOTS_VISUALIZACION = {
    "Tendencia Mensual (ISA)": plot_tendencia_isa,
    "Sueno vs Fatiga": plot_sueno_vs_fatiga,
    "Estres vs Dolor": plot_estres_vs_dolor,
    "Dieta vs Fatiga": plot_dieta_vs_fatiga,
    "Clima vs Rigidez": plot_clima_vs_rigidez,
    "Ejercicio vs ISA": plot_ejercicio_vs_isa,
}

# ================================================================
# Alias útiles para importación directa
# ================================================================
__all__ = [
    "plot_tendencia_isa",
    "plot_sueno_vs_fatiga",
    "plot_estres_vs_dolor",
    "plot_dieta_vs_fatiga",
    "plot_clima_vs_rigidez",
    "plot_ejercicio_vs_isa",
    "PLOTS_VISUALIZACION",
]
