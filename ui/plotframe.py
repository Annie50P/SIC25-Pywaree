import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.backends._backend_tk import NavigationToolbar2Tk  # opcional


class PlotFrame(tk.Frame):
    """
    Un contenedor reutilizable que integra una figura de Matplotlib dentro de un Frame de Tkinter.

    Parámetros:
    -----------
    master : tk.Widget
        El contenedor padre (por ejemplo, una ventana o frame).
    plot_func : callable, opcional
        Función de graficado que debe aceptar como primer argumento el eje (ax),
        seguida de *args y **kwargs.
        Ejemplo: plot_func(ax, df)
    plot_args : tuple, opcional
        Argumentos posicionales a pasar a `plot_func`.
    plot_kwargs : dict, opcional
        Argumentos con nombre a pasar a `plot_func`.
    **frame_opts : dict
        Opciones estándar del Frame (bg, relief, etc.).
    """

    def __init__(self, master, plot_func=None, plot_args=None, plot_kwargs=None, **frame_opts):
        super().__init__(master, **frame_opts)

        self.plot_func = plot_func
        self.plot_args = plot_args or ()
        self.plot_kwargs = plot_kwargs or {}

        # Crear figura y ejes
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        # Canvas (puente entre Matplotlib y Tkinter)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Redibujar al redimensionar ventana
        self.bind("<Configure>", lambda event: self.canvas.draw())

        # Dibuja automáticamente si se pasó una función inicial
        if self.plot_func:
            self.draw_plot()

    # --------------------------------------------------------
    def set_plot(self, plot_func, *args, **kwargs):
        """Cambia la función de gráfica y la redibuja inmediatamente."""
        self.plot_func = plot_func
        self.plot_args = args
        self.plot_kwargs = kwargs
        self.draw_plot()

    # --------------------------------------------------------
    def draw_plot(self):
        """
        Limpia los ejes actuales, ejecuta `plot_func(ax, *args, **kwargs)`
        y actualiza el canvas. Si ocurre un error, lo muestra visualmente.
        """
        if self.plot_func is None:
            return

        self.ax.clear()
        try:
            self.plot_func(self.ax, *self.plot_args, **self.plot_kwargs)
        except Exception as e:
            self.ax.text(
                0.5, 0.5,
                f"Error al generar la gráfica:\n{e}",
                ha="center", va="center", wrap=True, fontsize=10, color="red",
            )
        self.canvas.draw_idle()

    # --------------------------------------------------------
    def clear_plot(self):
        """Limpia la figura completamente sin eliminar el Frame."""
        self.ax.clear()
        self.canvas.draw_idle()
