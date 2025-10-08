import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# -- opcional -- nevagicion 2D grafica
# from matplotlib.backends._backend_tk import NavigationToolbar2Tk


class PlotFrame(tk.Frame):
    """
    Un Frame que contiene una Figure de matplotlib y Canvas
    plot_func debe llamar como: plot_func(ax, *args, **kwargs)
    """

    def __init__(
        self, master, plot_func=None, plot_args=None, plot_kwargs=None, **frame_opts
    ):
        super().__init__(master, **frame_opts)
        self.plot_func = plot_func
        self.plot_args = plot_args or ()
        self.plot_kwargs = plot_kwargs or {}

        # Crea figura y ejes
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        # Canvas + toolbar
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        # -- opcional -- navegacion 2D grafica
        # self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        # self.toolbar.update()
        #
        # Layout: toolbar on top, canvas fills
        # self.toolbar.pack(side=tk.TOP, fill=tk.X)
        # -- opcional --
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Dibuja grafica inicial si no se provee grafica
        if self.plot_func:
            self.draw_plot()

    def set_plot(self, plot_func, *args, **kwargs):
        """Cambia la funcion de grafica y redibuja inmediatamente"""
        self.plot_func = plot_func
        self.plot_args = args
        self.plot_kwargs = kwargs
        self.draw_plot()

    def draw_plot(self):
        """Limpia ejes, llama grafica del usuario plot_func(ax, ...) y redibuja canvas"""
        if self.plot_func is None:
            return
        self.ax.cla()  # limpia contenido enterior
        # dibujar grafica enviada en el canvas
        self.plot_func(self.ax, *self.plot_args, **self.plot_kwargs)
        self.canvas.draw()
