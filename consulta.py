import tkinter as tk
from tkinter import ttk
from datetime import datetime

class ReporteViewer:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Visualizador de Reportes")

        self.cal_inicio = ttk.Calendario(self.ventana, datepattern='yyyy-mm-dd')
        self.cal_inicio.pack(padx=10, pady=10)

        self.cal_fin = ttk.Calendario(self.ventana, datepattern='yyyy-mm-dd')
        self.cal_fin.pack(padx=10, pady=10)

        self.btn_visualizar = tk.Button(self.ventana, text="Visualizar Reporte", command=self.visualizar_reporte)
        self.btn_visualizar.pack(pady=10)

    def visualizar_reporte(self):
        fecha_inicio = self.cal_inicio.get_date()
        fecha_fin = self.cal_fin.get_date()

        print("Fecha de inicio:", fecha_inicio)
        print("Fecha de fin:", fecha_fin)
        # Agrega la lógica para generar y mostrar el reporte aquí

    def iniciar(self):
        self.ventana.mainloop()

# Puedes probar el visualizador de reportes ejecutando la siguiente línea
# reporte_viewer = ReporteViewer()
# reporte_viewer.iniciar()