import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import pandas as pd
from reportlab.pdfgen import canvas
from tkinter import filedialog

class InformeViewer:
    def __init__(self, root, resultados):
        self.root = root
        self.root.title("Reporte de asistencia")
        # Guarda los resultados como variable de instancia
        self.resultados = resultados

        # Crear el Treeview (tabla)
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("CODIGO", "FECHA y HORA")
        for col in self.tree["columns"]:
            self.tree.column(col, anchor=tk.CENTER)
            self.tree.heading(col, text=col, anchor=tk.CENTER)

        for i, row in enumerate(resultados):
            self.tree.insert('', i, values=row)

        # Añadir Scrollbars
        y_scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        y_scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscroll=y_scrollbar.set)

        x_scrollbar = ttk.Scrollbar(self.root, orient="horizontal", command=self.tree.xview)
        x_scrollbar.pack(side="bottom", fill="x")
        self.tree.configure(xscroll=x_scrollbar.set)

        # Mostrar Treeview
        self.tree.pack(expand=True, fill="both")

        # Botón para exportar a PDF
        self.btn_exportar = tk.Button(self.root, text="Exportar a PDF", command=self.exportar_a_pdf)
        self.btn_exportar.pack(pady=10)

        # Centrar la ventana en la pantalla después de que se haya creado
        self.root.update_idletasks()
        ancho_ventana = self.root.winfo_reqwidth()
        alto_ventana = self.root.winfo_reqheight()
        x_pantalla = (self.root.winfo_screenwidth() // 2) - (ancho_ventana // 2)
        y_pantalla = (self.root.winfo_screenheight() // 2) - (alto_ventana // 2)
        self.root.geometry('{}x{}+{}+{}'.format(ancho_ventana, alto_ventana, x_pantalla, y_pantalla))

    def exportar_a_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])

        if file_path:
            # Crear un lienzo PDF
            c = canvas.Canvas(file_path)

            # Encabezado
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, 800, "Reporte de Asistencias")

            # Contenido del informe (usando los datos actuales)
            row_height = 20
            y_position = 750

            for row in self.resultados:
                y_position -= row_height
                for col, value in enumerate(row):
                    c.drawString(100, y_position, f"{self.tree['columns'][col]}: {value}")
                    y_position -= row_height

            # Guardar el PDF
            c.save()

if __name__ == "__main__":
    root = tk.Tk()
    resultados = [("1", "2023-01-01 12:00:00"), ("2", "2023-01-02 14:30:00")]
    informe_viewer = InformeViewer(root, resultados)

    # Ocultar la ventana temporalmente
    root.withdraw()

    # Mostrar la ventana centrada
    root.update_idletasks()
    ancho_ventana = root.winfo_reqwidth()
    alto_ventana = root.winfo_reqheight()
    x_pantalla = (root.winfo_screenwidth() // 2) - (ancho_ventana // 2)
    y_pantalla = (root.winfo_screenheight() // 2) - (alto_ventana // 2)
    root.geometry('{}x{}+{}+{}'.format(ancho_ventana, alto_ventana, x_pantalla, y_pantalla))

    root.mainloop()
