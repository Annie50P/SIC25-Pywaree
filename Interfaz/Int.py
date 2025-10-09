import tkinter as tk
from tkinter import messagebox

# Variable global para almacenar el nombre de usuario
usuario_actual = ""

# --- ALMACENAMIENTO DE DATOS ---
# Usaremos un diccionario simple para simular una base de datos de usuarios
# Clave: nombre_usuario, Valor: {contrasena, nombre, apellido, email, edad, genero}
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

# -------------------------------------------------------------------
# FUNCIÓN CLAVE: Cerrar sesión y volver al login
# -------------------------------------------------------------------

def cerrar_sesion(ventana_actual):
    """Destruye la ventana actual y llama a la función para abrir la ventana de login."""
    global usuario_actual
    usuario_actual = ""  # Limpia el usuario global
    ventana_actual.destroy()
    abrir_ventana_login()

# -------------------------------------------------------------------

# Función para abrir la interfaz principal
def abrir_ventana_principal():
    ventana_principal = tk.Tk()
    ventana_principal.title("MAC - Panel Principal")
    ventana_principal.geometry("1000x500")
    ventana_principal.resizable(False, False)

    # Encabezado superior con fondo dark violet
    encabezado = tk.Frame(ventana_principal, height=50, bg="dark violet")
    encabezado.pack(side="top", fill="x")

    tk.Label(encabezado, text="Motor de Análisis de Correlación (MAC)", font=("Arial", 14, "bold"),
             bg="dark violet", fg="white").pack(side="left", padx=20, pady=10)

    # Contenedor para el nombre de usuario y el botón de cerrar sesión
    contenedor_usuario = tk.Frame(encabezado, bg="dark violet")
    contenedor_usuario.pack(side="right", padx=10)
    
    # Nombre de usuario
    tk.Label(contenedor_usuario, text=usuario_actual, font=("Arial", 12),
             bg="dark violet", fg="white").pack(side="left", padx=10)

    # BOTÓN DE CERRAR SESIÓN
    btn_cerrar_sesion = tk.Button(contenedor_usuario, text="Cerrar Sesión 🚪", 
                                  bg="#DC3545", fg="white", 
                                  font=("Arial", 10), cursor="hand2",
                                  command=lambda: cerrar_sesion(ventana_principal))
    btn_cerrar_sesion.pack(side="left", padx=10)


    # Menú lateral izquierdo
    menu_lateral = tk.Frame(ventana_principal, width=200, bg="white")
    menu_lateral.pack(side="left", fill="y")
    # Línea divisoria
    linea_divisoria = tk.Frame(ventana_principal, width=1, bg="#CCCCCC")
    linea_divisoria.pack(side="left", fill="y")

    opciones_menu = [
        "Dashboard General",
        "RFC1: Registro Diario",
        "RFC2: Análisis Estadístico",
        "RFC4: Visualizaciones",
        "RFC4: Simulación Dataset",
        "Mi Perfil"
    ]

    def resaltar(event):
        event.widget.config(bg="#E0E0E0")

    def restaurar(event):
        event.widget.config(bg="white")

    for opcion in opciones_menu:
        btn = tk.Label(menu_lateral, text=opcion, bg="white", fg="black",
                       font=("Arial", 10), anchor="w", padx=10)
        btn.pack(fill="x", pady=2)
        btn.bind("<Enter>", resaltar)
        btn.bind("<Leave>", restaurar)

    # Panel principal derecho (Muestra 'Mi Perfil' por defecto)
    panel_derecho = tk.Frame(ventana_principal, bg="white")
    panel_derecho.pack(side="right", expand=True, fill="both")

    contenedor_perfil = tk.Frame(panel_derecho, bg="white")
    contenedor_perfil.place(relx=0.5, rely=0.1, anchor="n")

    tk.Label(contenedor_perfil, text="Información del Paciente", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

    # Formulario de Perfil (usando datos del usuario actual)
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
        messagebox.showinfo("Actualización", "Información actualizada correctamente.")

    tk.Button(contenedor_perfil, text="Actualizar Información", bg="#1976D2", fg="white",
              font=("Arial", 10), width=25, command=actualizar_info).pack(pady=20)

    ventana_principal.mainloop()

# --- FUNCIONALIDAD DE REGISTRO ---

def abrir_ventana_registro(ventana_padre, entry_usuario, entry_contrasena):
    """Muestra la ventana modal de registro."""
    
    ventana_registro = tk.Toplevel(ventana_padre)
    ventana_registro.title("MAC - Registrar Nuevo Usuario")
    ventana_registro.geometry("450x450")
    ventana_registro.resizable(False, False)
    ventana_registro.transient(ventana_padre)
    ventana_registro.grab_set()

    tk.Label(ventana_registro, text="Complete sus Datos de Registro", 
             font=("Arial", 14, "bold"), pady=10).pack()

    form_registro = tk.Frame(ventana_registro, padx=10, pady=10)
    form_registro.pack()

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
    genero_var.set("No Especificado")
    
    for i, (etiqueta_texto, clave) in enumerate(campos_registro):
        tk.Label(form_registro, text=etiqueta_texto, anchor="w", width=20).grid(row=i, column=0, padx=5, pady=5)
        
        if clave == "genero":
            opciones_genero = ["Femenino", "Masculino", "Otro", "No Especificado"]
            entrada = tk.OptionMenu(form_registro, genero_var, *opciones_genero)
            entrada.config(width=25)
        else:
            entrada = tk.Entry(form_registro, width=30)
            if clave == "contrasena":
                entrada.config(show="*")
        
        entrada.grid(row=i, column=1, padx=5, pady=5)
        entradas[clave] = entrada

    def guardar_registro():
        """Valida y guarda los datos, luego intenta iniciar sesión."""
        
        datos = {
            "usuario": entradas["usuario"].get().strip(),
            "contrasena": entradas["contrasena"].get(),
            "nombre": entradas["nombre"].get().strip(),
            "apellido": entradas["apellido"].get().strip(),
            "email": entradas["email"].get().strip(),
            "edad": entradas["edad"].get().strip(),
            "genero": genero_var.get()
        }
        
        # --- Validación de datos ---
        if any(not datos[k] for k in ["usuario", "contrasena", "nombre", "apellido", "email", "edad"]):
            messagebox.showerror("Error de Registro", "Por favor, complete todos los campos obligatorios.", parent=ventana_registro)
            return
        
        if datos["usuario"] in USUARIOS_REGISTRADOS:
            messagebox.showerror("Error de Registro", "El nombre de usuario ya existe.", parent=ventana_registro)
            return

        if not datos["email"].__contains__("@") or not datos["email"].__contains__("."):
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


    tk.Button(ventana_registro, text="Registrar y Volver", bg="#4CAF50", fg="white", width=25, 
              font=("Arial", 10, "bold"), command=guardar_registro).pack(pady=20)


# -------------------------------------------------------------------
# FUNCIÓN CLAVE: Abre la ventana de login (se llama al iniciar y al cerrar sesión)
# -------------------------------------------------------------------

def abrir_ventana_login():
    """Crea y muestra la ventana de inicio de sesión."""
    
    # Usar Toplevel si ya existe una ventana raíz, o Tk() si no (como en este caso al inicio)
    global ventana_login
    try:
        ventana_login.destroy()
    except:
        pass # Ignorar si no existe
        
    ventana_login = tk.Tk()
    ventana_login.title("MAC - Iniciar Sesión")
    ventana_login.geometry("800x400")
    ventana_login.resizable(False, False)

    # Marco izquierdo (Diseño)
    frame_izquierdo = tk.Frame(ventana_login, width=400, height=400, bg="dark violet")
    frame_izquierdo.pack(side="left", fill="both")

    label_info = tk.Label(frame_izquierdo, text="Motor de Análisis de Correlación\npara Artritis Reumatoide",
                          font=("Arial", 16), bg="dark violet", fg="white", justify="center")
    label_info.place(relx=0.5, rely=0.5, anchor="center")

    # Marco derecho (Formulario de Login)
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