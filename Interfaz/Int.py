import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 
import datetime # <--- NUEVA IMPORTACIÓN

# Variable global para almacenar el nombre de usuario
usuario_actual = ""

# --- ALMACENAMIENTO DE DATOS (Se mantiene igual) ---
USUARIOS_REGISTRADOS = {
    "andres": {
        "contrasena": "1234",
        "nombre": "Andres",
        "apellido": "Gómez",
        "email": "andres@mail.com",
        "edad": 35,
        "genero": "Masculino"
    },
    "ana": {
        "contrasena": "5678",
        "nombre": "Ana",
        "apellido": "Martínez",
        "email": "ana.martinez@corp.com",
        "edad": 42,
        "genero": "Femenino"
    },
    "jorge": {
        "contrasena": "secreto",
        "nombre": "Jorge",
        "apellido": "Pérez",
        "email": "jorge.perez@data.org",
        "edad": 55,
        "genero": "Masculino"
    }
}
# ------------------------------

# --- FUNCIÓN DE TRADUCCIÓN PARA LA FECHA ---
def obtener_fecha_actual_espanol():
    """Retorna la fecha actual formateada en español."""
    now = datetime.datetime.now()
    
    # Mapeo de días y meses de inglés a español
    dias_es = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    meses_es = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    
    # Obtener el día de la semana (0=Lunes, 6=Domingo) y el mes (1=Enero, 12=Diciembre)
    dia_semana = dias_es[now.weekday()]
    mes = meses_es[now.month - 1]
    
    # Formato deseado: "Día 04 de Mes, 2025"
    fecha_formateada = f"{dia_semana} {now.day} de {mes}, {now.year}"
    return fecha_formateada
# -------------------------------------------


# -------------------------------------------------------------------
# FUNCIÓN CLAVE: Cerrar sesión y volver al login (Se mantiene igual)
# -------------------------------------------------------------------

def cerrar_sesion(ventana_actual):
    """Destruye la ventana actual y llama a la función para abrir la ventana de login."""
    global usuario_actual
    usuario_actual = ""  # Limpia el usuario global
    ventana_actual.destroy()
    abrir_ventana_login()

# -------------------------------------------------------------------
# FUNCIÓN CLAVE: CONTENIDO DEL REGISTRO DIARIO CON SCROLLBAR (FECHA CORREGIDA)
# -------------------------------------------------------------------

def mostrar_registro_diario(panel_contenedor):
    """Crea y muestra el formulario de Registro Diario en el panel derecho CON SCROLLBAR."""
    
    for widget in panel_contenedor.winfo_children():
        widget.destroy()

    # --- OBTENER LA FECHA ACTUAL ---
    fecha_hoy = obtener_fecha_actual_espanol() # <--- ¡CORRECCIÓN AQUÍ!
    # -------------------------------
    
    # --- 1. CONFIGURACIÓN DEL SCROLL ---
    canvas = tk.Canvas(panel_contenedor, bg="white")
    scrollbar = ttk.Scrollbar(panel_contenedor, orient="vertical", command=canvas.yview)
    
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Frame que contendrá todo el contenido y que se desplazará
    scrollable_frame = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
    # Función para ajustar el scroll y el ancho del frame
    def on_frame_configure(event):
        # 1. Ajustar la scrollregion al tamaño total del frame (para el desplazamiento vertical)
        canvas.configure(scrollregion=canvas.bbox("all"))
        # 2. Forzar el ancho del frame interno a coincidir con el ancho del canvas
        canvas_width = event.width
        canvas.itemconfig(canvas.itemcget(tk.ALL, 'window'), width=canvas_width)

    scrollable_frame.bind("<Configure>", on_frame_configure)
    
    def on_canvas_resize(event):
        canvas.itemconfigure(canvas.itemcget(tk.ALL, 'window'), width=event.width)
    
    canvas.bind('<Configure>', on_canvas_resize)
    
    # --- SIMULACIÓN DE WIDGETS Y VARIABLES ---
    
    # Etiqueta de la fecha usando la variable dinámica
    tk.Label(scrollable_frame, text=f"Registro de Hoy - {fecha_hoy}", 
             font=("Arial", 16, "bold"), fg="#4B0082", bg="white").pack(pady=20, padx=20, anchor="w")

    opciones_0_5 = [str(i) for i in range(6)]
    rigidez_var = tk.StringVar(value="0")
    dolor_var = tk.StringVar(value="0")
    inflamacion_var = tk.StringVar(value="0")
    fatiga_var = tk.StringVar(value="0")
    
    estado_animo_var = tk.StringVar(value="-- Seleccionar --")
    actividad_fisica_var = tk.StringVar(value="-- Seleccionar --") 
    calidad_sueno_var = tk.StringVar(value="-- Seleccionar --") 
    tipo_dieta_var = tk.StringVar(value="-- Seleccionar --")
    consume_alcohol_var = tk.StringVar(value="-- Seleccionar --") 
    tomo_medicacion_var = tk.StringVar(value="-- Seleccionar --") 
    
    gluten_var = tk.BooleanVar()
    lacteos_var = tk.BooleanVar()
    azucares_var = tk.BooleanVar()
    procesados_var = tk.BooleanVar()
    carnes_rojas_var = tk.BooleanVar()
    frituras_var = tk.BooleanVar()
    
    
    # --- Estructura del Formulario (Usando Frame y Grid, ANCLADO AL SCROLLABLE_FRAME) ---
    
    formulario = tk.Frame(scrollable_frame, bg="white", padx=20, pady=10)
    formulario.pack(fill="x", padx=20)
    
    fila_actual = 0
    
    # ------------------ SECCIÓN SÍNTOMAS ------------------
    
    tk.Label(formulario, text="📌 Síntomas", font=("Arial", 12, "bold"), bg="white", fg="#1976D2").grid(row=fila_actual, column=0, columnspan=3, sticky="w", pady=(10, 5))
    fila_actual += 1

    # Columna 1: Rigidez Matutina
    tk.Label(formulario, text="Rigidez Matutina (0-5)", bg="white").grid(row=fila_actual, column=0, sticky="w")
    ttk.Combobox(formulario, textvariable=rigidez_var, values=opciones_0_5, state="readonly", width=12).grid(row=fila_actual + 1, column=0, padx=10, sticky="w")
    tk.Label(formulario, text="0 = Sin rigidez; 5 = Rigidez severa", font=("Arial", 8), fg="gray", bg="white").grid(row=fila_actual + 2, column=0, sticky="w")
    
    # Columna 2: Dolor Articular
    tk.Label(formulario, text="Dolor Articular (0-5)", bg="white").grid(row=fila_actual, column=1, sticky="w", padx=40)
    ttk.Combobox(formulario, textvariable=dolor_var, values=opciones_0_5, state="readonly", width=12).grid(row=fila_actual + 1, column=1, padx=40, sticky="w")
    tk.Label(formulario, text="0 = Sin dolor; 5 = Dolor severo", font=("Arial", 8), fg="gray", bg="white").grid(row=fila_actual + 2, column=1, sticky="w", padx=40)
    
    # Columna 3: Inflamación Articular
    tk.Label(formulario, text="Inflamación Articular (0-5)", bg="white").grid(row=fila_actual, column=2, sticky="w", padx=40)
    ttk.Combobox(formulario, textvariable=inflamacion_var, values=opciones_0_5, state="readonly", width=12).grid(row=fila_actual + 1, column=2, padx=40, sticky="w")
    tk.Label(formulario, text="0 = Sin inflamación; 5 = Inflamación severa", font=("Arial", 8), fg="gray", bg="white").grid(row=fila_actual + 2, column=2, sticky="w", padx=40)
    
    fila_actual += 3
    
    # Fatiga Crónica 
    tk.Label(formulario, text="Fatiga Crónica (0-5)", bg="white").grid(row=fila_actual, column=0, sticky="w", pady=(10, 0))
    ttk.Combobox(formulario, textvariable=fatiga_var, values=opciones_0_5, state="readonly", width=12).grid(row=fila_actual + 1, column=0, padx=10, sticky="w")
    tk.Label(formulario, text="0 = Sin fatiga; 5 = Fatiga extrema", font=("Arial", 8), fg="gray", bg="white").grid(row=fila_actual + 2, column=0, sticky="w")
    
    fila_actual += 3
    
    # ------------------ SECCIÓN ESTADO EMOCIONAL ------------------
    
    tk.Label(formulario, text="🧠 Estado Emocional", font=("Arial", 12, "bold"), bg="white", fg="#1976D2").grid(row=fila_actual, column=0, columnspan=3, sticky="w", pady=(20, 5))
    fila_actual += 1
    
    tk.Label(formulario, text="Estado de Ánimo", bg="white").grid(row=fila_actual, column=0, sticky="w")
    estados_animo = ["Feliz", "Neutral", "Triste", "Ansioso", "Irritable"]
    ttk.Combobox(formulario, textvariable=estado_animo_var, values=estados_animo, state="readonly", width=20).grid(row=fila_actual + 1, column=0, sticky="w", padx=10)
    tk.Label(formulario, text="Escala 1-5 según intensidad emocional", font=("Arial", 8), fg="gray", bg="white").grid(row=fila_actual + 2, column=0, sticky="w")
    
    fila_actual += 3

    # ------------------ SECCIÓN ACTIVIDAD FÍSICA Y SUEÑO ------------------
    
    tk.Label(formulario, text="🏃 Actividad Física y Sueño", font=("Arial", 12, "bold"), bg="white", fg="#1976D2").grid(row=fila_actual, column=0, columnspan=3, sticky="w", pady=(20, 5))
    fila_actual += 1

    # Columna 1: Actividad Física
    tk.Label(formulario, text="¿Realizaste Actividad Física?", bg="white").grid(row=fila_actual, column=0, sticky="w")
    opciones_si_no = ["Sí", "No"]
    ttk.Combobox(formulario, textvariable=actividad_fisica_var, values=opciones_si_no, state="readonly", width=20).grid(row=fila_actual + 1, column=0, sticky="w", padx=10)
    
    # Columna 2: Calidad del Sueño
    tk.Label(formulario, text="Calidad del Sueño", bg="white").grid(row=fila_actual, column=1, sticky="w", padx=40)
    opciones_calidad = ["Excelente (5)", "Buena (4)", "Regular (3)", "Mala (2)", "Pésima (1)"]
    ttk.Combobox(formulario, textvariable=calidad_sueno_var, values=opciones_calidad, state="readonly", width=20).grid(row=fila_actual + 1, column=1, sticky="w", padx=40)
    tk.Label(formulario, text="Escala 1-5", font=("Arial", 8), fg="gray", bg="white").grid(row=fila_actual + 2, column=1, sticky="w", padx=40)

    fila_actual += 3

    # ------------------ SECCIÓN NUTRICIÓN Y DIETA ------------------
    
    tk.Label(formulario, text="🍽️ Nutrición y Dieta", font=("Arial", 12, "bold"), bg="white", fg="#4B0082").grid(row=fila_actual, column=0, columnspan=3, sticky="w", pady=(20, 5))
    fila_actual += 1

    # Columna 1: Tipo de Dieta
    tk.Label(formulario, text="Tipo de Dieta", bg="white").grid(row=fila_actual, column=0, sticky="w")
    opciones_dieta = ["Cetogénica", "Mediterránea", "Vegetariana", "Estándar"]
    ttk.Combobox(formulario, textvariable=tipo_dieta_var, values=opciones_dieta, state="readonly", width=20).grid(row=fila_actual + 1, column=0, sticky="w", padx=10)
    
    # Columna 2: Consumo de Alcohol
    tk.Label(formulario, text="¿Consumiste Alcohol?", bg="white").grid(row=fila_actual, column=1, sticky="w", padx=40)
    opciones_si_no_alcohol = ["Sí", "No"]
    ttk.Combobox(formulario, textvariable=consume_alcohol_var, values=opciones_si_no_alcohol, state="readonly", width=20).grid(row=fila_actual + 1, column=1, sticky="w", padx=40)
    
    fila_actual += 3

    # Alimentos Consumidos (Checkboxes)
    tk.Label(formulario, text="Alimentos Consumidos (Selecciona todos los que apliquen)", font=("Arial", 10, "bold"), bg="white").grid(row=fila_actual, column=0, columnspan=3, sticky="w", pady=(10, 5))
    fila_actual += 1
    
    # Frame para los Checkboxes en una sola fila
    checkbox_frame = tk.Frame(formulario, bg="white")
    checkbox_frame.grid(row=fila_actual, column=0, columnspan=3, sticky="w", pady=5)

    tk.Checkbutton(checkbox_frame, text="Gluten", variable=gluten_var, bg="white").pack(side="left", padx=5)
    tk.Checkbutton(checkbox_frame, text="Lácteos", variable=lacteos_var, bg="white").pack(side="left", padx=5)
    tk.Checkbutton(checkbox_frame, text="Azúcares", variable=azucares_var, bg="white").pack(side="left", padx=5)
    tk.Checkbutton(checkbox_frame, text="Procesados", variable=procesados_var, bg="white").pack(side="left", padx=5)
    tk.Checkbutton(checkbox_frame, text="Carnes Rojas", variable=carnes_rojas_var, bg="white").pack(side="left", padx=5)
    tk.Checkbutton(checkbox_frame, text="Frituras", variable=frituras_var, bg="white").pack(side="left", padx=5)
    
    tk.Label(formulario, text="Estos datos se convertirán en columnas binarias para análisis", font=("Arial", 8), fg="gray", bg="white").grid(row=fila_actual + 1, column=0, columnspan=3, sticky="w")
    
    fila_actual += 2
    
    # ------------------ SECCIÓN MEDICACIÓN ------------------

    tk.Label(formulario, text="💊 Medicación", font=("Arial", 12, "bold"), bg="white", fg="#4B0082").grid(row=fila_actual, column=0, columnspan=3, sticky="w", pady=(20, 5))
    fila_actual += 1
    
    tk.Label(formulario, text="¿Tomaste tu Medicación?", bg="white").grid(row=fila_actual, column=0, sticky="w")
    ttk.Combobox(formulario, textvariable=tomo_medicacion_var, values=opciones_si_no, state="readonly", width=20).grid(row=fila_actual + 1, column=0, sticky="w", padx=10)
    
    # ------------------ BOTÓN GUARDAR (anclado al scrollable_frame) ------------------
    
    def validar_y_guardar_registro():
        
        campos_obligatorios = [
            rigidez_var.get(), dolor_var.get(), inflamacion_var.get(), fatiga_var.get(), 
            estado_animo_var.get(), actividad_fisica_var.get(), calidad_sueno_var.get(), 
            tipo_dieta_var.get(), consume_alcohol_var.get(), tomo_medicacion_var.get()
        ]
        
        if "-- Seleccionar --" in campos_obligatorios:
            messagebox.showerror("Error de Registro", "Por favor, complete todos los campos de selección obligatorios.", parent=panel_contenedor)
            return
            
        messagebox.showinfo("Registro Guardado", "El Registro Diario ha sido guardado correctamente para análisis.", parent=panel_contenedor)

    tk.Button(scrollable_frame, text="💾 Guardar Registro Diario", bg="#4B0082", fg="white",
              font=("Arial", 12, "bold"), width=30, command=validar_y_guardar_registro).pack(pady=40)
    
# -------------------------------------------------------------------


# Función para abrir la interfaz principal
def abrir_ventana_principal():
    ventana_principal = tk.Tk()
    ventana_principal.title("MAC - Panel Principal")
    ventana_principal.geometry("1000x500")
    ventana_principal.resizable(True, True) 

    # Encabezado superior con fondo dark violet
    encabezado = tk.Frame(ventana_principal, height=50, bg="dark violet")
    encabezado.pack(side="top", fill="x")

    tk.Label(encabezado, text="Motor de Análisis de Correlación (MAC)", font=("Arial", 14, "bold"),
             bg="dark violet", fg="white").pack(side="left", padx=20, pady=10)

    # Contenedor para el nombre de usuario y el botón de cerrar sesión
    contenedor_usuario = tk.Frame(encabezado, bg="dark violet")
    contenedor_usuario.pack(side="right", padx=10)
    
    tk.Label(contenedor_usuario, text=usuario_actual, font=("Arial", 12),
             bg="dark violet", fg="white").pack(side="left", padx=10)

    btn_cerrar_sesion = tk.Button(contenedor_usuario, text="Cerrar Sesión 🚪", 
                                  bg="#DC3545", fg="white", 
                                  font=("Arial", 10), cursor="hand2",
                                  command=lambda: cerrar_sesion(ventana_principal))
    btn_cerrar_sesion.pack(side="left", padx=10)

    # Menú lateral izquierdo
    menu_lateral = tk.Frame(ventana_principal, width=200, bg="white")
    menu_lateral.pack(side="left", fill="y")
    linea_divisoria = tk.Frame(ventana_principal, width=1, bg="#CCCCCC")
    linea_divisoria.pack(side="left", fill="y")

    # Panel principal derecho (Contenedor de Contenido)
    panel_derecho = tk.Frame(ventana_principal, bg="white")
    panel_derecho.pack(side="right", expand=True, fill="both")
    
    # Definir las opciones y la función a ejecutar
    opciones_menu_map = {
        "Dashboard General": lambda: mostrar_panel_vacio(panel_derecho, "Dashboard General"),
        "RFC1: Registro Diario": lambda: mostrar_registro_diario(panel_derecho),
        "RFC2: Análisis Estadístico": lambda: mostrar_panel_vacio(panel_derecho, "Análisis Estadístico"),
        "RFC4: Visualizaciones": lambda: mostrar_panel_vacio(panel_derecho, "Visualizaciones"),
        "RFC4: Simulación Dataset": lambda: mostrar_panel_vacio(panel_derecho, "Simulación Dataset"),
        "Mi Perfil": lambda: mostrar_perfil(panel_derecho),
    }

    def mostrar_panel_vacio(panel_contenedor, titulo):
        """Función temporal para limpiar y mostrar un título en el panel."""
        for widget in panel_contenedor.winfo_children():
            widget.destroy()
        tk.Label(panel_contenedor, text=f"Contenido de {titulo} (Próxima Implementación)", 
                 font=("Arial", 18), fg="gray", bg="white").pack(expand=True)
    
    def mostrar_perfil(panel_contenedor):
        """Crea y muestra el formulario de perfil."""
        for widget in panel_contenedor.winfo_children():
            widget.destroy()
            
        contenedor_perfil = tk.Frame(panel_contenedor, bg="white")
        contenedor_perfil.place(relx=0.5, rely=0.1, anchor="n")

        tk.Label(contenedor_perfil, text="Información del Paciente", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        info_usuario = USUARIOS_REGISTRADOS.get(usuario_actual, {})
        nombre_completo = f"{info_usuario.get('nombre', '')} {info_usuario.get('apellido', '')}"

        formulario = tk.Frame(contenedor_perfil, bg="white")
        formulario.pack()

        campos = [
            ("Nombre Completo:", nombre_completo.strip() if nombre_completo.strip() else "Usuario sin nombre"),
            ("Nombre de Usuario:", usuario_actual),
            ("Email:", info_usuario.get('email', 'No registrado')),
            ("Edad:", info_usuario.get('edad', 'No registrado')),
            ("Género:", info_usuario.get('genero', 'No registrado')),
            ("Fecha de Diagnóstico:", ""), 
            ("Reumatólogo:", "Dr. Juan Pérez"),
        ]

        entradas = {}
        for i, (etiqueta, valor) in enumerate(campos):
            tk.Label(formulario, text=etiqueta, bg="white", anchor="e", width=20).grid(row=i, column=0, padx=5, pady=5)
            entrada = tk.Entry(formulario, width=40)
            entrada.insert(0, valor)
            
            if etiqueta not in ("Fecha de Diagnóstico:", "Reumatólogo:"):
                 entrada.config(state='readonly') 

            entrada.grid(row=i, column=1, padx=5, pady=5)
            entradas[etiqueta] = entrada

        def actualizar_info():
            messagebox.showinfo("Actualización", "Información actualizada correctamente.", parent=panel_contenedor)

        tk.Button(contenedor_perfil, text="Actualizar Información", bg="#1976D2", fg="white",
                  font=("Arial", 10), width=25, command=actualizar_info).pack(pady=20)


    def resaltar(event):
        event.widget.config(bg="#E0E0E0")

    def restaurar(event):
        event.widget.config(bg="white")
        
    def seleccionar_opcion(event, opcion):
        # Ejecuta la función asociada a la opción seleccionada
        opciones_menu_map[opcion]()

    for opcion in opciones_menu_map.keys():
        btn = tk.Label(menu_lateral, text=opcion, bg="white", fg="black",
                       font=("Arial", 10), anchor="w", padx=10)
        btn.pack(fill="x", pady=2)
        btn.bind("<Enter>", resaltar)
        btn.bind("<Leave>", restaurar)
        btn.bind("<Button-1>", lambda event, o=opcion: seleccionar_opcion(event, o))
    
    mostrar_registro_diario(panel_derecho)
    
    ventana_principal.mainloop()

# --- FUNCIÓN DE REGISTRO CON SCROLLBAR IMPLEMENTADA (Se mantiene igual) ---

def abrir_ventana_registro(ventana_padre, entry_usuario, entry_contrasena):
    """Muestra la ventana modal de registro con una barra de desplazamiento."""
    
    ventana_registro = tk.Toplevel(ventana_padre)
    ventana_registro.title("MAC - Registrar Nuevo Usuario")
    ventana_registro.geometry("450x450")
    ventana_registro.resizable(False, False)
    ventana_registro.transient(ventana_padre)
    ventana_registro.grab_set()

    tk.Label(ventana_registro, text="Complete sus Datos de Registro", 
             font=("Arial", 14, "bold"), pady=10).pack()

    # 1. Crear el Canvas (Lienzo)
    canvas = tk.Canvas(ventana_registro)
    canvas.pack(side="left", fill="both", expand=True)

    # 2. Crear la Barra de Desplazamiento
    scrollbar = ttk.Scrollbar(ventana_registro, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # 3. Configurar el Canvas para que use la Scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    # Evento para reajustar el área de desplazamiento cuando cambia el tamaño del contenido
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

    # 4. Crear un Frame interior (form_registro) donde irá todo el contenido
    # Este Frame es el que se moverá dentro del Canvas
    form_registro = tk.Frame(canvas, padx=10, pady=10)
    
    # 5. Añadir el Frame interior al Canvas
    canvas.create_window((0, 0), window=form_registro, anchor="nw")

    # --- Contenido del Formulario (Añadido al form_registro) ---
    
    entradas = {}
    
    campos_registro = [
        ("Nombre de Usuario:", "usuario"),
        ("Contraseña:", "contrasena"),
        ("Nombre:", "nombre"),
        ("Apellido:", "apellido"),
        ("Email:", "email"),
        ("Edad:", "edad"),
        ("Género:", "genero")
    ]
    
    genero_var = tk.StringVar(ventana_registro)
    genero_var.set("-- Seleccionar --") 
    
    for i, (etiqueta_texto, clave) in enumerate(campos_registro):
        tk.Label(form_registro, text=etiqueta_texto, anchor="w", width=20).grid(row=i, column=0, padx=5, pady=5)
        
        if clave == "genero":
            opciones_genero = ["Femenino", "Masculino", "Otro", "No Especificado"]
            entrada = ttk.Combobox(form_registro, textvariable=genero_var, values=opciones_genero, state="readonly", width=25)
        else:
            entrada = tk.Entry(form_registro, width=30)
            if clave == "contrasena":
                entrada.config(show="*")
        
        entrada.grid(row=i, column=1, padx=5, pady=5)
        entradas[clave] = entrada

    def guardar_registro():
        """Valida **todos** los campos y guarda el usuario."""
        
        datos = {
            "usuario": entradas["usuario"].get().strip(),
            "contrasena": entradas["contrasena"].get(),
            "nombre": entradas["nombre"].get().strip(),
            "apellido": entradas["apellido"].get().strip(),
            "email": entradas["email"].get().strip(),
            "edad": entradas["edad"].get().strip(),
            "genero": genero_var.get()
        }
        
        # --- Validación de Campos Vacíos ---
        campos_a_revisar = ["usuario", "contrasena", "nombre", "apellido", "email", "edad"]
        if any(not datos[k] for k in campos_a_revisar) or datos["genero"] == "-- Seleccionar --":
            messagebox.showerror("Error de Registro", "Por favor, complete todos los campos obligatorios.", parent=ventana_registro)
            return
        
        # --- Validación de Existencia y Formato ---
        if datos["usuario"] in USUARIOS_REGISTRADOS:
            messagebox.showerror("Error de Registro", "El nombre de usuario ya existe.", parent=ventana_registro)
            return

        if not "@" in datos["email"] or not "." in datos["email"]:
             messagebox.showerror("Error de Registro", "Ingrese un email válido.", parent=ventana_registro)
             return
             
        try:
            datos["edad"] = int(datos["edad"])
        except ValueError:
            messagebox.showerror("Error de Registro", "La edad debe ser un número válido.", parent=ventana_registro)
            return
        
        # --- Almacenamiento ---
        USUARIOS_REGISTRADOS[datos["usuario"]] = {
            "contrasena": datos["contrasena"],
            "nombre": datos["nombre"],
            "apellido": datos["apellido"],
            "email": datos["email"],
            "edad": datos["edad"],
            "genero": datos["genero"]
        }
        
        messagebox.showinfo("Registro Exitoso", f"Usuario '{datos['usuario']}' registrado. ¡Ahora puedes iniciar sesión!", parent=ventana_registro)
        
        ventana_registro.destroy()
        
        # Rellenar los campos de la ventana de login automáticamente
        entry_usuario.delete(0, tk.END)
        entry_usuario.insert(0, datos["usuario"])
        entry_contrasena.delete(0, tk.END)
        entry_contrasena.insert(0, datos["contrasena"])


    btn_guardar = tk.Button(form_registro, text="Registrar y Volver", bg="#4CAF50", fg="white", width=25, 
              font=("Arial", 10, "bold"), command=guardar_registro)
    
    # Colocar el botón dentro del frame interior
    btn_guardar.grid(row=len(campos_registro), column=0, columnspan=2, pady=20)


def abrir_ventana_login():
    """Crea y muestra la ventana de inicio de sesión."""
    
    global ventana_login
    try:
        ventana_login.destroy()
    except:
        pass
        
    ventana_login = tk.Tk()
    ventana_login.title("MAC - Iniciar Sesión")
    ventana_login.geometry("800x400")
    ventana_login.resizable(False, False)

    frame_izquierdo = tk.Frame(ventana_login, width=400, height=400, bg="dark violet")
    frame_izquierdo.pack(side="left", fill="both")

    label_info = tk.Label(frame_izquierdo, text="Motor de Análisis de Correlación\npara Artritis Reumatoide",
                          font=("Arial", 16), bg="dark violet", fg="white", justify="center")
    label_info.place(relx=0.5, rely=0.5, anchor="center")

    frame_derecho = tk.Frame(ventana_login, width=400, height=400, bg="white")
    frame_derecho.pack(side="right", fill="both")

    contenedor_formulario = tk.Frame(frame_derecho, bg="white")
    contenedor_formulario.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(contenedor_formulario, text="Usuario o Email", bg="white").pack(pady=(10, 5))
    entry_usuario = tk.Entry(contenedor_formulario, width=30)
    entry_usuario.pack()

    tk.Label(contenedor_formulario, text="Contraseña", bg="white").pack(pady=(10, 5))
    entry_contrasena = tk.Entry(contenedor_formulario, show="*", width=30)
    entry_contrasena.pack()

    def verificar_credenciales():
        """Verifica si el usuario y contraseña coinciden con los datos registrados."""
        global usuario_actual
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()

        if usuario in USUARIOS_REGISTRADOS and USUARIOS_REGISTRADOS[usuario]["contrasena"] == contrasena:
            usuario_actual = usuario
            ventana_login.destroy()
            abrir_ventana_principal()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    btn_ingresar = tk.Button(contenedor_formulario, text="Ingresar", bg="#1976D2", fg="white", width=20, command=verificar_credenciales)
    btn_ingresar.pack(pady=20)

    # Botón para abrir la ventana de registro
    tk.Button(contenedor_formulario, text="¿No tienes cuenta? Regístrate aquí", fg="blue", bg="white", 
              cursor="hand2", borderwidth=0, 
              command=lambda: abrir_ventana_registro(ventana_login, entry_usuario, entry_contrasena)).pack()

    ventana_login.mainloop()

# Inicia la aplicación abriendo la ventana de login
abrir_ventana_login()