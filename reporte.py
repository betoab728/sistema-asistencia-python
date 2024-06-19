import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from informe import InformeViewer
import mysql.connector

class ReporteViewer:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("CONSULTA DE ASISTENCIAS")

        # Etiqueta para el título
        self.etiqueta_titulo = tk.Label(self.ventana, text="REPORTE DE ASISTENCIAS", font=("Arial", 14, "bold"))
        self.etiqueta_titulo.pack(pady=10)

        # ComboBox para seleccionar un trabajador
        self.etiqueta_trabajador = tk.Label(self.ventana, text="Seleccionar Trabajador", font=("Arial", 10, "bold"))
        self.etiqueta_trabajador.pack(pady=5)

        # Conexión a la base de datos MySQL (ajusta los parámetros según tu configuración)
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="asistencia"
        )
        self.cursor = self.conexion.cursor()

        # Consulta para obtener la lista de trabajadores
        query = "select concat_ws(' ',nombre,apellidoMaterno,apellidoPaterno) nombre FROM asistencia.trabajadores"
        self.cursor.execute(query)
        trabajadores = [row[0] for row in self.cursor.fetchall()]

        # ComboBox con la lista de trabajadores
        self.combobox_trabajador = ttk.Combobox(self.ventana, values=trabajadores,width=40)
        self.combobox_trabajador.pack(pady=10)

        # Contenedor para los calendarios
        self.frame_calendarios = tk.Frame(self.ventana)
        self.frame_calendarios.pack(padx=10, pady=10)

        # Etiqueta "Inicio" encima del calendario de inicio
        self.etiqueta_inicio = tk.Label(self.frame_calendarios, text="INICIO", font=("Arial", 10, "bold"))
        self.etiqueta_inicio.grid(row=0, column=0, padx=10, pady=5)

        # Calendario de inicio
        self.cal_inicio = Calendar(self.frame_calendarios, date_pattern='yyyy-mm-dd')
        self.cal_inicio.grid(row=1, column=0, padx=10, pady=10)

        # Etiqueta "Fin" encima del calendario de fin
        self.etiqueta_fin = tk.Label(self.frame_calendarios, text="FIN", font=("Arial", 10, "bold"))
        self.etiqueta_fin.grid(row=0, column=1, padx=10, pady=5)

        # Calendario de fin
        self.cal_fin = Calendar(self.frame_calendarios, date_pattern='yyyy-mm-dd')
        self.cal_fin.grid(row=1, column=1, padx=10, pady=10)

        self.btn_visualizar = tk.Button(self.ventana, text="Visualizar Reporte", command=self.visualizar_reporte)
        self.btn_visualizar.pack(pady=10)

        # Centrar la ventana en la pantalla
        self.ventana.update_idletasks()
        ancho_ventana = self.ventana.winfo_width()
        alto_ventana = self.ventana.winfo_height()
        x_pantalla = (self.ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
        y_pantalla = (self.ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
        self.ventana.geometry('{}x{}+{}+{}'.format(ancho_ventana, alto_ventana, x_pantalla, y_pantalla))

    def visualizar_reporte(self):
        # Obtener las fechas seleccionadas
        fecha_inicio = self.cal_inicio.get_date()
        fecha_fin = self.cal_fin.get_date()

        # Obtener el trabajador seleccionado del ComboBox
        trabajador_seleccionado = self.combobox_trabajador.get()

        # Construir y ejecutar la consulta SQL
        query = """
            SELECT id CODIGO,  fecha_hora
            FROM asistencias
            WHERE id_trabajador = (
                SELECT id
                FROM trabajadores
                WHERE concat_ws(' ', nombre, apellidoMaterno, apellidoPaterno) = %s
            )
            AND fecha_hora BETWEEN %s AND %s
        """
        params = (trabajador_seleccionado, fecha_inicio, fecha_fin)
        self.cursor.execute(query, params)
        resultados = self.cursor.fetchall()

        # Formatear las fechas después de obtener los resultados
        resultados_formateados = [(codigo, fecha.strftime("%d/%m/%Y %H:%M:%S %p")) for codigo, fecha in resultados]

        # Crear la ventana del informe
        report_window = tk.Toplevel(self.ventana)
        informe_viewer = InformeViewer(report_window, resultados_formateados)

    def iniciar(self):
        self.ventana.mainloop()

# Uso del visualizador de reportes
if __name__ == "__main__":
    reporte_viewer = ReporteViewer()
    reporte_viewer.iniciar()

