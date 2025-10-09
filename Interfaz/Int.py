import tkinter as tk
from tkinter import messagebox

# Variable global para almacenar el nombre de usuario
usuario_actual = ""

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

    tk.Label(encabezado, text=usuario_actual, font=("Arial", 12),
             bg="dark violet", fg="white").pack(side="right", padx=20)

    # Menú lateral izquierdo sin fondo, texto negro, con resaltado al pasar el mouse
    menu_lateral = tk.Frame(ventana_principal, width=200, bg="white")
    menu_lateral.pack(side="left", fill="y")
    # Línea divisoria entre el menú lateral y el panel principal
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

    # Panel principal derecho
    panel_derecho = tk.Frame(ventana_principal, bg="white")
    panel_derecho.pack(side="right", expand=True, fill="both")

    contenedor_perfil = tk.Frame(panel_derecho, bg="white")
    contenedor_perfil.place(relx=0.5, rely=0.1, anchor="n")

    tk.Label(contenedor_perfil, text="Información del Paciente", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

    # Formulario en dos columnas
    formulario = tk.Frame(contenedor_perfil, bg="white")
    formulario.pack()

    campos = [
        ("Nombre Completo:", "María González"),
        ("Fecha de Diagnóstico:", ""),
        ("Reumatólogo:", "Dr. Juan Pérez"),
        ("Email:", "maria.gonzalez@gmail.com")
    ]

    entradas = {}
    for i, (etiqueta, valor) in enumerate(campos):
        tk.Label(formulario, text=etiqueta, bg="white", anchor="e", width=20).grid(row=i, column=0, padx=5, pady=5)
        entrada = tk.Entry(formulario, width=40)
        entrada.insert(0, valor)
        entrada.grid(row=i, column=1, padx=5, pady=5)
        entradas[etiqueta] = entrada

    def actualizar_info():
        messagebox.showinfo("Actualización", "Información actualizada correctamente.")

    tk.Button(contenedor_perfil, text="Actualizar Información", bg="#1976D2", fg="white",
              font=("Arial", 10), width=25, command=actualizar_info).pack(pady=20)

    ventana_principal.mainloop()

# Ventana de inicio de sesión
ventana_login = tk.Tk()
ventana_login.title("MAC - Iniciar Sesión")
ventana_login.geometry("800x400")
ventana_login.resizable(False, False)

# Marco izquierdo
frame_izquierdo = tk.Frame(ventana_login, width=400, height=400, bg="dark violet")
frame_izquierdo.pack(side="left", fill="both")

label_info = tk.Label(frame_izquierdo, text="Motor de Análisis de Correlación\npara Artritis Reumatoide",
                      font=("Arial", 16), bg="dark violet", fg="white", justify="center")
label_info.place(relx=0.5, rely=0.5, anchor="center")

# Marco derecho
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
    global usuario_actual
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    if usuario == "andres" and contrasena == "1234":
        usuario_actual = usuario  # Guarda el nombre para mostrarlo en la siguiente ventana
        ventana_login.destroy()
        abrir_ventana_principal()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

btn_ingresar = tk.Button(contenedor_formulario, text="Ingresar", bg="#1976D2", fg="white", width=20, command=verificar_credenciales)
btn_ingresar.pack(pady=20)

# tk.Label(contenedor_formulario, text="¿No tienes cuenta? Regístrate aquí", fg="blue", bg="white", cursor="hand2").pack()

ventana_login.mainloop()
