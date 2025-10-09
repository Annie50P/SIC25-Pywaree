import pandas as pd
from scipy.stats import ttest_ind


def cargar_y_procesar(ruta_csv):
    """Carga, transforma y genera variables analíticas para el MAC."""
    df = pd.read_csv(ruta_csv)
    df["fecha"] = pd.to_datetime(df["fecha"])

    # Clima
    df["clima_adverso"] = (
        (df["clima"] == "Lluvioso") | (df["clima"] == "Húmedo")
    ).astype(int)

    # Sueño
    mapeo_sueno = {"Horrible": 1, "Malo": 2, "Ok": 3, "Bueno": 4, "Excelente": 5}
    df["sueno_score"] = pd.to_numeric(df["sueño"].replace(mapeo_sueno), errors="coerce")

    # Dieta
    mapeo_dieta = {"Inflamatoria": 0, "Balanceada": 1, "Antiinflamatoria": 2}
    df["dieta_score"] = pd.to_numeric(df["dieta_tipo"].replace(mapeo_dieta), errors="coerce")

    # Estado de ánimo
    mapeo_animo = {"Feliz": 1, "Tranquilo": 2, "Optimista": 3, "Neutral": 4, "Estresado": 5, "Ansioso": 6, "Irritable": 7, "Frustrado": 8, "Triste": 9}
    df["estado_animo_score"] = pd.to_numeric(df["estado_animo"].replace(mapeo_animo), errors="coerce")

    # ISA (Índice de Síntomas Agregados)
    columnas_sintomas = [
        "dolor_score",
        "inflamacion_score",
        "fatiga_score",
        "rigidez_score",
    ]
    df["ISA"] = df[columnas_sintomas].mean(axis=1)

    # Subconjunto numérico
    columnas_numericas = [
        "temperatura_C",
        "actividad_fisica",
        "sueno_score",
        "dieta_score",
        "clima_adverso",
        "rigidez_score",
        "dolor_score",
        "inflamacion_score",
        "fatiga_score",
        "estado_animo_score",
        "ISA",
    ]
    columnas_existentes = [c for c in columnas_numericas if c in df.columns]
    df_numerico = df[columnas_existentes].copy()

    # Matriz de correlación
    matriz_correlacion = df_numerico.corr(numeric_only=True)

    return df, df_numerico, matriz_correlacion
