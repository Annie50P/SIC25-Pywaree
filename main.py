import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import os
import csv
import json
from ui.plotframe import PlotFrame
from ui.analisis import PLOTS_ANALISIS
from ui.visualizacion import PLOTS_VISUALIZACION
from analisis_datos.correlaciones import cargar_y_procesar

# Nombre del archivo para guardar los perfiles de usuario
USR_DIR = "usuarios"
ARCHIVO_USUARIOS = os.path.join(USR_DIR, "usuarios.json")
DATOS_DIR = os.path.join(USR_DIR, "datos")
DATOS_SIMULADOS = "notebooks/dataset_clinico_180dias.csv"
usuario_actual = ""

# --- DATOS predefinidos
USUARIOS_PREDETERMINADOS = {
    "andres": {
        "contrasena": "1234",
        "nombre": "Andres",
        "apellido": "Gómez",
        "email": "andres@mail.com",
        "edad": 35,
        "genero": "Masculino",
    },
    "ana": {
        "contrasena": "5678",
        "nombre": "Ana",
        "apellido": "Martínez",
        "email": "ana.martinez@corp.com",
        "edad": 42,
        "genero": "Femenino",
    },
}
# ------------------------------

# -- Cargar datos del usuario --
# def cargar_datos_usuario(usuario_actual):
#     ruta = os.path.join(DATOS_DIR, f"{usuario_actual}_registros.csv")
#     if not os.path.exists(ruta):
#         return None, None, None
#     return cargar_y_procesar(ruta)

# --- FUNCIONES DE PERSISTENCIA DE USUARIOS ---


def guardar_usuarios():
    """Guarda el diccionario global de usuarios en un archivo JSON."""
    global USUARIOS_REGISTRADOS
    try:
        with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as f:
            json.dump(USUARIOS_REGISTRADOS, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Error de Persistencia", f"Error al guardar usuarios: {e}")


def cargar_usuarios():
    """Carga el diccionario de usuarios desde un archivo JSON."""
    if os.path.exists(ARCHIVO_USUARIOS):
        try:
            with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error al cargar usuarios: {e}. Usando datos predeterminados.")
            return USUARIOS_PREDETERMINADOS.copy()
    return USUARIOS_PREDETERMINADOS.copy()


# Cargar los usuarios al inicio
USUARIOS_REGISTRADOS = cargar_usuarios()


# --- FUNCIÓN DE TRADUCCIÓN PARA LA FECHA ---
def obtener_fecha_actual_espanol():
    """Retorna la fecha actual formateada en español."""
    now = datetime.datetime.now()
    dias_es = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    meses_es = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ]
    dia_semana = dias_es[now.weekday()]
    mes = meses_es[now.month - 1]
    return f"{dia_semana} {now.day} de {mes}, {now.year}"


# --- GESTIÓN DE SESIÓN ---
def cerrar_sesion(ventana_actual):
    """Cierra la sesión actual y vuelve a la ventana de login."""
    global usuario_actual
    usuario_actual = ""
    ventana_actual.destroy()
    abrir_ventana_login()


# --- LÓGICA DE LA APLICACIÓN ---
def generar_mensaje_retroalimentacion(datos):
    """Analiza los datos del registro y crea un mensaje de feedback."""
    mensajes = ["¡Tu registro ha sido guardado con éxito!"]
    try:
        dolor = int(datos["dolor"])
        fatiga = int(datos["fatiga"])
    except ValueError:
        dolor, fatiga = 0, 0

    if dolor >= 4 or fatiga >= 4:
        mensajes.append(
            "Vemos que hoy ha sido un día con síntomas elevados. Recuerda ser amable contigo mismo y descansar."
        )
    if datos["clima"] in ["Lluvioso", "Húmedo"]:
        mensajes.append(
            "Los días húmedos pueden intensificar la rigidez. Considera mantenerte abrigado y hacer estiramientos suaves."
        )
    if datos["dieta"] == "Inflamatoria":
        mensajes.append(
            "Notamos una dieta pro-inflamatoria. Incorporar más vegetales o pescado puede hacer una gran diferencia."
        )
    elif datos["dieta"] == "Antiinflamatoria":
        mensajes.append(
            "¡Excelente elección con una dieta antiinflamatoria! Es un gran apoyo para tu cuerpo."
        )
    if datos["sueno"] in ["Malo", "Horrible"]:
        mensajes.append(
            f"Un sueño de calidad '{datos['sueno'].lower()}' afecta la fatiga. Priorizar el descanso es clave."
        )
    elif datos["sueno"] in ["Excelente", "Bueno"]:
        mensajes.append(
            "¡Qué bien que hayas tenido una buena noche de sueño! Es fundamental."
        )
    if datos["actividad"] == "Sí":
        mensajes.append("¡Felicidades por mantenerte activo! Cada movimiento cuenta.")
    else:
        if dolor < 3 and fatiga < 3:
            mensajes.append(
                "En días con menos síntomas, una caminata suave puede ayudar a la movilidad."
            )
        else:
            mensajes.append(
                "Escuchar a tu cuerpo y descansar en días difíciles es muy importante."
            )
    return "\n\n- ".join(mensajes)


# -------------------------------------------------------------------
# --- INTERFAZ GRÁFICA ---
# -------------------------------------------------------------------


def mostrar_registro_diario(panel_contenedor):
    for widget in panel_contenedor.winfo_children():
        widget.destroy()

    fecha_hoy = obtener_fecha_actual_espanol()

    canvas = tk.Canvas(panel_contenedor, bg="white")
    scrollbar = ttk.Scrollbar(panel_contenedor, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)

    tk.Label(
        scrollable_frame,
        text=f"Registro de Hoy - {fecha_hoy}",
        font=("Arial", 16, "bold"),
        fg="#4B0082",
        bg="white",
    ).pack(pady=20, padx=20, anchor="w")

    opciones_0_5 = [str(i) for i in range(6)]
    rigidez_var, dolor_var, inflamacion_var, fatiga_var = (
        tk.StringVar(value="0") for _ in range(4)
    )
    (
        estado_animo_var,
        actividad_fisica_var,
        calidad_sueno_var,
        tipo_dieta_var,
        clima_actual_var,
    ) = (tk.StringVar(value="-- Seleccionar --") for _ in range(5))
    temperatura_var = tk.StringVar(value="")

    formulario = tk.Frame(scrollable_frame, bg="white", padx=20, pady=10)
    formulario.pack(fill="x", padx=20)

    fila_actual = 0

    tk.Label(
        formulario,
        text=" Clima y Entorno",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#4B0082",
    ).grid(row=fila_actual, column=0, columnspan=3, sticky="w", pady=(20, 5))
    fila_actual += 1
    tk.Label(formulario, text="Tipo de Clima", bg="white").grid(
        row=fila_actual, column=0, sticky="w"
    )
    ttk.Combobox(
        formulario,
        textvariable=clima_actual_var,
        values=["Soleado", "Seco", "Ventoso", "Nublado", "Lluvioso", "Húmedo"],
        state="readonly",
        width=20,
    ).grid(row=fila_actual + 1, column=0, sticky="w", padx=10)
    tk.Label(formulario, text="Temperatura (°C)", bg="white").grid(
        row=fila_actual, column=1, sticky="w", padx=40
    )
    tk.Entry(formulario, textvariable=temperatura_var, width=15).grid(
        row=fila_actual + 1, column=1, sticky="w", padx=40
    )
    tk.Label(
        formulario, text="Ej: 28.5", font=("Arial", 8), fg="gray", bg="white"
    ).grid(row=fila_actual + 2, column=1, sticky="w", padx=40)
    fila_actual += 3

    tk.Label(
        formulario,
        text="Síntomas",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#1976D2",
    ).grid(row=fila_actual, column=0, columnspan=3, sticky="w", pady=(10, 5))
    fila_actual += 1
    tk.Label(formulario, text="Rigidez Matutina (0-5)", bg="white").grid(
        row=fila_actual, column=0, sticky="w"
    )
    ttk.Combobox(
        formulario,
        textvariable=rigidez_var,
        values=opciones_0_5,
        state="readonly",
        width=12,
    ).grid(row=fila_actual + 1, column=0, padx=10, sticky="w")
    tk.Label(formulario, text="Dolor Articular (0-5)", bg="white").grid(
        row=fila_actual, column=1, sticky="w", padx=40
    )
    ttk.Combobox(
        formulario,
        textvariable=dolor_var,
        values=opciones_0_5,
        state="readonly",
        width=12,
    ).grid(row=fila_actual + 1, column=1, padx=40, sticky="w")
    tk.Label(formulario, text="Inflamación Articular (0-5)", bg="white").grid(
        row=fila_actual, column=2, sticky="w", padx=40
    )
    ttk.Combobox(
        formulario,
        textvariable=inflamacion_var,
        values=opciones_0_5,
        state="readonly",
        width=12,
    ).grid(row=fila_actual + 1, column=2, padx=40, sticky="w")
    fila_actual += 3
    tk.Label(formulario, text="Fatiga Crónica (0-5)", bg="white").grid(
        row=fila_actual, column=0, sticky="w", pady=(10, 0)
    )
    ttk.Combobox(
        formulario,
        textvariable=fatiga_var,
        values=opciones_0_5,
        state="readonly",
        width=12,
    ).grid(row=fila_actual + 1, column=0, padx=10, sticky="w")
    fila_actual += 3

    tk.Label(
        formulario,
        text=" Estado Emocional",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#1976D2",
    ).grid(row=fila_actual, column=0, columnspan=3, sticky="w", pady=(20, 5))
    fila_actual += 1
    tk.Label(formulario, text="Estado de Ánimo", bg="white").grid(
        row=fila_actual, column=0, sticky="w"
    )
    ttk.Combobox(
        formulario,
        textvariable=estado_animo_var,
        values=[
            "Feliz",
            "Tranquilo",
            "Optimista",
            "Neutral",
            "Estresado",
            "Ansioso",
            "Irritable",
            "Frustrado",
            "Triste",
        ],
        state="readonly",
        width=20,
    ).grid(row=fila_actual + 1, column=0, sticky="w", padx=10)
    fila_actual += 3

    tk.Label(
        formulario,
        text=" Actividad Física y Sueño",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#1976D2",
    ).grid(row=fila_actual, column=0, columnspan=3, sticky="w", pady=(20, 5))
    fila_actual += 1
    tk.Label(formulario, text="¿Realizaste Actividad Física?", bg="white").grid(
        row=fila_actual, column=0, sticky="w"
    )
    ttk.Combobox(
        formulario,
        textvariable=actividad_fisica_var,
        values=["Sí", "No"],
        state="readonly",
        width=20,
    ).grid(row=fila_actual + 1, column=0, sticky="w", padx=10)
    tk.Label(formulario, text="Calidad del Sueño", bg="white").grid(
        row=fila_actual, column=1, sticky="w", padx=40
    )
    ttk.Combobox(
        formulario,
        textvariable=calidad_sueno_var,
        values=["Excelente", "Bueno", "Ok", "Malo", "Horrible"],
        state="readonly",
        width=20,
    ).grid(row=fila_actual + 1, column=1, sticky="w", padx=40)
    fila_actual += 3

    tk.Label(
        formulario,
        text=" Nutrición y Dieta",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#4B0082",
    ).grid(row=fila_actual, column=0, columnspan=3, sticky="w", pady=(20, 5))
    fila_actual += 1
    tk.Label(formulario, text="Tipo de Dieta", bg="white").grid(
        row=fila_actual, column=0, sticky="w"
    )
    ttk.Combobox(
        formulario,
        textvariable=tipo_dieta_var,
        values=["Antiinflamatoria", "Balanceada", "Inflamatoria"],
        state="readonly",
        width=20,
    ).grid(row=fila_actual + 1, column=0, sticky="w", padx=10)
    fila_actual += 3

    def validar_y_guardar_registro():
        campos_obligatorios = [
            v.get()
            for v in [
                rigidez_var,
                dolor_var,
                inflamacion_var,
                fatiga_var,
                estado_animo_var,
                actividad_fisica_var,
                calidad_sueno_var,
                tipo_dieta_var,
                clima_actual_var,
            ]
        ]
        if "-- Seleccionar --" in campos_obligatorios or not temperatura_var.get():
            messagebox.showerror(
                "Error",
                "Por favor, complete todos los campos.",
                parent=panel_contenedor,
            )
            return
        try:
            temperatura = float(temperatura_var.get().replace(",", "."))
        except ValueError:
            messagebox.showerror(
                "Error",
                "La temperatura debe ser un número válido.",
                parent=panel_contenedor,
            )
            return

        datos_para_feedback = {
            k: v.get()
            for k, v in zip(
                ["dolor", "fatiga", "clima", "dieta", "sueno", "actividad"],
                [
                    dolor_var,
                    fatiga_var,
                    clima_actual_var,
                    tipo_dieta_var,
                    calidad_sueno_var,
                    actividad_fisica_var,
                ],
            )
        }
        nueva_fila = [
            datetime.datetime.now().strftime("%Y-%m-%d"),
            clima_actual_var.get(),
            temperatura,
            1 if actividad_fisica_var.get() == "Sí" else 0,
            calidad_sueno_var.get(),
            tipo_dieta_var.get(),
            rigidez_var.get(),
            dolor_var.get(),
            inflamacion_var.get(),
            fatiga_var.get(),
            estado_animo_var.get(),
        ]
        nombre_archivo = os.path.join(DATOS_DIR, f"{usuario_actual}_registros.csv")
        try:
            file_exists = os.path.exists(nombre_archivo)
            with open(nombre_archivo, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(
                        [
                            "fecha",
                            "clima",
                            "temperatura_C",
                            "actividad_fisica",
                            "sueño",
                            "dieta_tipo",
                            "rigidez_score",
                            "dolor_score",
                            "inflamacion_score",
                            "fatiga_score",
                            "estado_animo",
                        ]
                    )
                writer.writerow(nueva_fila)
            messagebox.showinfo(
                "Análisis Diario",
                generar_mensaje_retroalimentacion(datos_para_feedback),
                parent=panel_contenedor,
            )
        except Exception as e:
            messagebox.showerror(
                "Error de Guardado",
                f"Ocurrió un error al guardar: {e}",
                parent=panel_contenedor,
            )

    tk.Button(
        scrollable_frame,
        text=" Guardar y Analizar Registro",
        bg="#4B0082",
        fg="white",
        font=("Arial", 12, "bold"),
        width=30,
        command=validar_y_guardar_registro,
    ).pack(pady=40)


# -------------------------------------------------------------------
# Interfaz para mostrar graficas
# -------------------------------------------------------------------
def crear_menu_graficas(panel_contenedor, plots_dict, titulo_general, ruta_datos):
    """
    Crea un panel con un menú desplegable para seleccionar y visualizar gráficas.
    """
    # Limpiar el panel antes de insertar contenido nuevo
    for widget in panel_contenedor.winfo_children():
        widget.destroy()

    # --- Encabezado general ---
    tk.Label(
        panel_contenedor,
        text=f"RF03: {titulo_general}",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="#2C3E50",
    ).pack(pady=10, anchor="w", padx=20)

    # --- Frame superior con menú desplegable ---
    menu_frame = tk.Frame(panel_contenedor, bg="white")
    menu_frame.pack(fill="x", padx=30, pady=(10, 5))

    tk.Label(
        menu_frame,
        text="Seleccionar gráfica:",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#1976D2",
    ).pack(side="left", padx=(0, 10))

    combo_graficas = ttk.Combobox(
        menu_frame,
        values=list(plots_dict.keys()),
        state="readonly",
        width=45,
        font=("Arial", 10),
    )
    combo_graficas.pack(side="left", padx=5)
    combo_graficas.set(list(plots_dict.keys())[0])  # seleccionar la primera por defecto

    # --- Frame título y contenedor del gráfico ---
    titulo_grafica = tk.Label(
        panel_contenedor,
        text=list(plots_dict.keys())[0],
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#4B0082",
    )
    titulo_grafica.pack(anchor="w", padx=30, pady=(10, 5))

    frame_grafico = tk.Frame(panel_contenedor, bg="white")
    frame_grafico.pack(fill="both", expand=True, padx=30, pady=10)

    # --- Cargar y procesar datos ---
    if not os.path.exists(ruta_datos):
        tk.Label(
            frame_grafico,
            text="No hay datos disponibles para generar las gráficas.",
            font=("Arial", 12),
            bg="white",
            fg="gray",
        ).pack(expand=True)
        return

    df, df_numerico, matriz_correlacion = cargar_y_procesar(ruta_datos)
    if matriz_correlacion.isna().all().all():
        tk.Label(
            frame_grafico,
            text="No hay suficientes datos numéricos para generar correlaciones.",
            font=("Arial", 12),
            bg="white",
            fg="gray",
        ).pack(expand=True)
        return

    # --- Crear el PlotFrame inicial ---
    plot_func_inicial = plots_dict[list(plots_dict.keys())[0]]
    plot_frame = PlotFrame(
        frame_grafico,
        plot_func=plot_func_inicial,
        plot_args=(df_numerico,),
        bg="white",
    )
    plot_frame.pack(fill="both", expand=True)

    # --- Función para actualizar gráfica seleccionada ---
    def actualizar_grafica(_event=None):
        seleccion = combo_graficas.get()
        plot_func = plots_dict.get(seleccion)
        if not plot_func:
            return
        titulo_grafica.config(text=seleccion)
        plot_frame.set_plot(plot_func, df_numerico)

    combo_graficas.bind("<<ComboboxSelected>>", actualizar_grafica)
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# Analisis estadistico
# -------------------------------------------------------------------
def mostrar_analisis_estadistico(panel_contenedor):
    """Interfaz de selección y visualización de gráficos de análisis estadístico."""
    crear_menu_graficas(panel_contenedor, PLOTS_ANALISIS, "Análisis Estadístico", DATOS_SIMULADOS)
# -------------------------------------------------------------------


# -------------------------------------------------------------------
# Visualizacion clinica
# -------------------------------------------------------------------
def mostrar_visualizacion(panel_contenedor):
    """Interfaz de selección y visualización de gráficos de análisis estadístico."""
    crear_menu_graficas(panel_contenedor, PLOTS_VISUALIZACION, "Visualización", DATOS_SIMULADOS)
# -------------------------------------------------------------------


def abrir_ventana_principal():
    ventana_principal = tk.Tk()
    ventana_principal.title("MAC - Panel Principal")
    # -- ventana login dimension fija --
    # ventana_principal.geometry("1000x600")
    # -- ventana principal zoomed --
    ventana_principal.attributes("-zoomed", True)

    encabezado = tk.Frame(ventana_principal, height=50, bg="dark violet")
    encabezado.pack(side="top", fill="x")
    tk.Label(
        encabezado,
        text="Motor de Análisis de Correlación (MAC)",
        font=("Arial", 14, "bold"),
        bg="dark violet",
        fg="white",
    ).pack(side="left", padx=20, pady=10)
    contenedor_usuario = tk.Frame(encabezado, bg="dark violet")
    contenedor_usuario.pack(side="right", padx=10)
    tk.Label(
        contenedor_usuario,
        text=usuario_actual,
        font=("Arial", 12),
        bg="dark violet",
        fg="white",
    ).pack(side="left", padx=10)
    tk.Button(
        contenedor_usuario,
        text="Cerrar Sesión 🚪",
        bg="#DC3545",
        fg="white",
        font=("Arial", 10),
        command=lambda: cerrar_sesion(ventana_principal),
    ).pack(side="left", padx=10)

    menu_lateral = tk.Frame(ventana_principal, width=200, bg="white")
    menu_lateral.pack(side="left", fill="y")
    tk.Frame(ventana_principal, width=1, bg="#CCCCCC").pack(side="left", fill="y")
    panel_derecho = tk.Frame(ventana_principal, bg="white")
    panel_derecho.pack(side="right", expand=True, fill="both")

    def mostrar_panel_vacio(panel_contenedor, titulo):
        for widget in panel_contenedor.winfo_children():
            widget.destroy()
        tk.Label(
            panel_contenedor,
            text=f"Contenido de {titulo} (Próxima Implementación)",
            font=("Arial", 18),
            fg="gray",
            bg="white",
        ).pack(expand=True)

    def mostrar_perfil(panel_contenedor):
        for widget in panel_contenedor.winfo_children():
            widget.destroy()

        contenedor_perfil = tk.Frame(panel_contenedor, bg="white")
        contenedor_perfil.place(relx=0.5, rely=0.1, anchor="n")

        tk.Label(
            contenedor_perfil,
            text="Información de Mi Perfil",
            font=("Arial", 16, "bold"),
            bg="white",
        ).pack(pady=10)

        info_usuario = USUARIOS_REGISTRADOS.get(usuario_actual, {})
        formulario = tk.Frame(contenedor_perfil, bg="white", padx=20, pady=10)
        formulario.pack()

        nombre_var = tk.StringVar(value=info_usuario.get("nombre", ""))
        apellido_var = tk.StringVar(value=info_usuario.get("apellido", ""))
        email_var = tk.StringVar(value=info_usuario.get("email", ""))
        edad_var = tk.StringVar(value=info_usuario.get("edad", ""))
        genero_var = tk.StringVar(value=info_usuario.get("genero", ""))

        tk.Label(formulario, text="Nombre:", bg="white", anchor="e", width=20).grid(
            row=0, column=0, padx=5, pady=5
        )
        tk.Entry(formulario, textvariable=nombre_var, width=40).grid(
            row=0, column=1, padx=5, pady=5
        )
        tk.Label(formulario, text="Apellido:", bg="white", anchor="e", width=20).grid(
            row=1, column=0, padx=5, pady=5
        )
        tk.Entry(formulario, textvariable=apellido_var, width=40).grid(
            row=1, column=1, padx=5, pady=5
        )
        tk.Label(formulario, text="Email:", bg="white", anchor="e", width=20).grid(
            row=2, column=0, padx=5, pady=5
        )
        tk.Entry(formulario, textvariable=email_var, width=40).grid(
            row=2, column=1, padx=5, pady=5
        )
        tk.Label(formulario, text="Edad:", bg="white", anchor="e", width=20).grid(
            row=3, column=0, padx=5, pady=5
        )
        tk.Entry(formulario, textvariable=edad_var, width=40).grid(
            row=3, column=1, padx=5, pady=5
        )
        tk.Label(formulario, text="Género:", bg="white", anchor="e", width=20).grid(
            row=4, column=0, padx=5, pady=5
        )
        tk.Entry(formulario, textvariable=genero_var, width=40).grid(
            row=4, column=1, padx=5, pady=5
        )

        def actualizar_info():
            """Recolecta, valida y guarda la información actualizada del perfil."""
            global USUARIOS_REGISTRADOS
            try:
                nombre = nombre_var.get().strip()
                apellido = apellido_var.get().strip()
                email = email_var.get().strip()
                edad = int(edad_var.get().strip())
                genero = genero_var.get().strip()

                if not all([nombre, apellido, email, genero]):
                    messagebox.showerror(
                        "Error de Validación",
                        "Ningún campo puede estar vacío.",
                        parent=panel_contenedor,
                    )
                    return
                if "@" not in email or "." not in email:
                    messagebox.showerror(
                        "Error de Validación",
                        "El formato del email no es válido.",
                        parent=panel_contenedor,
                    )
                    return
            except ValueError:
                messagebox.showerror(
                    "Error de Validación",
                    "La edad debe ser un número entero válido.",
                    parent=panel_contenedor,
                )
                return

            USUARIOS_REGISTRADOS[usuario_actual].update(
                {
                    "nombre": nombre,
                    "apellido": apellido,
                    "email": email,
                    "edad": edad,
                    "genero": genero,
                }
            )
            guardar_usuarios()
            messagebox.showinfo(
                "Actualización Exitosa",
                "La información de tu perfil ha sido guardada.",
                parent=panel_contenedor,
            )

        tk.Button(
            contenedor_perfil,
            text="Actualizar Información",
            bg="#1976D2",
            fg="white",
            font=("Arial", 12, "bold"),
            width=25,
            command=actualizar_info,
        ).pack(pady=20)

    # ===================================================================
    # --- MENÚ LATERAL RESTAURADO (INICIO) ---
    # ===================================================================
    opciones_menu_map = {
        "Registro Diario": lambda: mostrar_registro_diario(panel_derecho),
        "Análisis Estadístico": lambda: mostrar_analisis_estadistico(panel_derecho),
        "Visualizaciones": lambda: mostrar_visualizacion(panel_derecho),
        "Simulación Dataset": lambda: mostrar_panel_vacio(
            panel_derecho, "Simulación Dataset"
        ),
        "Mi Perfil": lambda: mostrar_perfil(panel_derecho),
    }

    def resaltar(event):
        event.widget.config(bg="#E0E0E0")

    def restaurar(event):
        event.widget.config(bg="white")

    def seleccionar_opcion(event, opcion):
        opciones_menu_map[opcion]()

    for opcion in opciones_menu_map.keys():
        btn = tk.Label(
            menu_lateral,
            text=opcion,
            bg="white",
            fg="black",
            font=("Arial", 10),
            anchor="w",
            padx=10,
        )
        btn.pack(fill="x", pady=2)
        btn.bind("<Enter>", resaltar)
        btn.bind("<Leave>", restaurar)
        btn.bind("<Button-1>", lambda event, o=opcion: seleccionar_opcion(event, o))
    # ===================================================================
    # --- MENÚ LATERAL RESTAURADO (FIN) ---
    # ===================================================================

    mostrar_registro_diario(panel_derecho)
    ventana_principal.mainloop()


def abrir_ventana_registro(ventana_padre, entry_usuario, entry_contrasena):
    ventana_registro = tk.Toplevel(ventana_padre)
    ventana_registro.title("Registrar Usuario")
    ventana_registro.geometry("450x450")
    ventana_registro.transient(ventana_padre)
    ventana_registro.grab_set()

    tk.Label(
        ventana_registro,
        text="Complete sus Datos de Registro",
        font=("Arial", 14, "bold"),
        pady=10,
    ).pack()

    canvas = tk.Canvas(ventana_registro)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(ventana_registro, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    form_registro = tk.Frame(canvas, padx=10, pady=10)
    canvas.create_window((0, 0), window=form_registro, anchor="nw")
    canvas.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    entradas = {}
    campos_registro = [
        "Nombre de Usuario:",
        "Contraseña:",
        "Nombre:",
        "Apellido:",
        "Email:",
        "Edad:",
        "Género:",
    ]
    claves = ["usuario", "contrasena", "nombre", "apellido", "email", "edad", "genero"]
    genero_var = tk.StringVar(value="-- Seleccionar --")

    for i, (etiqueta, clave) in enumerate(zip(campos_registro, claves)):
        tk.Label(form_registro, text=etiqueta, anchor="w", width=20).grid(
            row=i, column=0, padx=5, pady=5
        )
        if clave == "genero":
            entrada = ttk.Combobox(
                form_registro,
                textvariable=genero_var,
                values=["Femenino", "Masculino", "Otro"],
                state="readonly",
                width=28,
            )
        else:
            entrada = tk.Entry(form_registro, width=30)
            if clave == "contrasena":
                entrada.config(show="*")
        entrada.grid(row=i, column=1, padx=5, pady=5)
        entradas[clave] = entrada

    def guardar_registro():
        datos = {
            clave: entradas[clave].get().strip()
            for clave in claves
            if clave != "genero"
        }
        datos["genero"] = genero_var.get()

        if (
            any(not v for k, v in datos.items() if k != "genero")
            or datos["genero"] == "-- Seleccionar --"
        ):
            messagebox.showerror(
                "Error",
                "Por favor, complete todos los campos.",
                parent=ventana_registro,
            )
            return
        if datos["usuario"] in USUARIOS_REGISTRADOS:
            messagebox.showerror(
                "Error", "El nombre de usuario ya existe.", parent=ventana_registro
            )
            return
        if "@" not in datos["email"] or "." not in datos["email"]:
            messagebox.showerror("Error", "Email inválido.", parent=ventana_registro)
            return
        try:
            datos["edad"] = int(datos["edad"])
        except ValueError:
            messagebox.showerror(
                "Error", "La edad debe ser un número.", parent=ventana_registro
            )
            return

        usuario_reg = datos.pop("usuario")
        USUARIOS_REGISTRADOS[usuario_reg] = datos
        guardar_usuarios()

        messagebox.showinfo(
            "Registro Exitoso",
            f"Usuario '{usuario_reg}' registrado. Ya puedes iniciar sesión.",
            parent=ventana_registro,
        )
        ventana_registro.destroy()

        entry_usuario.delete(0, tk.END)
        entry_usuario.insert(0, usuario_reg)
        entry_contrasena.delete(0, tk.END)
        entry_contrasena.insert(0, datos["contrasena"])

    tk.Button(
        form_registro,
        text="Registrar y Volver",
        bg="#4CAF50",
        fg="white",
        font=("Arial", 10, "bold"),
        command=guardar_registro,
    ).grid(row=len(campos_registro), column=0, columnspan=2, pady=20)


def abrir_ventana_login():
    global ventana_login
    try:
        ventana_login.destroy()
    except (NameError, tk.TclError):
        pass

    ventana_login = tk.Tk()
    ventana_login.title("MAC - Iniciar Sesión")
    # -- ventana login zoomed --
    # ventana_login.attributes("-zoomed", True)
    ventana_login.geometry("800x400")
    ventana_login.resizable(False, False)

    frame_izquierdo = tk.Frame(ventana_login, width=400, height=400, bg="dark violet")
    frame_izquierdo.pack(side="left", fill="both")
    frame_izquierdo.pack_propagate(False)

    label_info = tk.Label(
        frame_izquierdo,
        text="Motor de Análisis de Correlación\npara Artritis Reumatoide",
        font=("Arial", 16),
        bg="dark violet",
        fg="white",
        justify="center",
    )
    label_info.place(relx=0.5, rely=0.5, anchor="center")

    frame_derecho = tk.Frame(ventana_login, width=400, height=400, bg="white")
    frame_derecho.pack(side="right", fill="both")
    frame_derecho.pack_propagate(False)

    contenedor_formulario = tk.Frame(frame_derecho, bg="white")
    contenedor_formulario.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(contenedor_formulario, text="Usuario o Email", bg="white").pack(
        pady=(10, 5)
    )
    entry_usuario = tk.Entry(contenedor_formulario, width=30)
    entry_usuario.pack()

    tk.Label(contenedor_formulario, text="Contraseña", bg="white").pack(pady=(10, 5))
    entry_contrasena = tk.Entry(contenedor_formulario, show="*", width=30)
    entry_contrasena.pack()

    def verificar_credenciales():
        global usuario_actual
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()
        if (
            usuario in USUARIOS_REGISTRADOS
            and USUARIOS_REGISTRADOS[usuario]["contrasena"] == contrasena
        ):
            usuario_actual = usuario
            ventana_login.destroy()
            abrir_ventana_principal()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    tk.Button(
        contenedor_formulario,
        text="Ingresar",
        bg="#1976D2",
        fg="white",
        width=20,
        command=verificar_credenciales,
    ).pack(pady=20)
    tk.Button(
        contenedor_formulario,
        text="¿No tienes cuenta? Regístrate aquí",
        fg="blue",
        bg="white",
        cursor="hand2",
        borderwidth=0,
        command=lambda: abrir_ventana_registro(
            ventana_login, entry_usuario, entry_contrasena
        ),
    ).pack()

    ventana_login.mainloop()


# Inicia la aplicación
abrir_ventana_login()
