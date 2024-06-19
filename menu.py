import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from tkinter import PhotoImage
from tkinter import ttk, PhotoImage, Tk, messagebox
import subprocess
from reporte import ReporteViewer

class MainForm(ThemedTk):
    def __init__(self):
        super().__init__()

        # Configura la ventana principal
        self.set_theme("arc")  # Puedes probar diferentes temas aquí
        self.title("Formulario Principal MDI")
        self.state("zoomed")  # Maximiza la ventana
        self.configure(bg="white")

        # Carga la imagen de fondo con Pillow
        image_path = "C:/Users/USER/Documents/ITD/pythonProject/Resources/fondo.png"
        img = Image.open(image_path)
        self.background_image = ImageTk.PhotoImage(img)

        # Configura un label para mostrar la imagen de fondo
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)

        # Menú principal
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Define el estilo para los botones en la Toolbar
        style = ttk.Style(self)
        style.configure("Toolbar.TButton", padding=(10, 5), font=('Helvetica', 10))

        # Crea una Toolbar
        self.image_trabajador = PhotoImage(file=r"C:\Users\USER\Documents\ITD\pythonProject\Resources\trabajador.png")
        self.image_marca = PhotoImage(file=r"C:\Users\USER\Documents\ITD\pythonProject\Resources\clock.png")
        self.image_reporte = PhotoImage(file=r"C:\Users\USER\Documents\ITD\pythonProject\Resources\reporte.png")
        self.image_exit = PhotoImage(file=r"C:\Users\USER\Documents\ITD\pythonProject\Resources\exit.png")

        toolbar = ttk.Frame(self, style="Toolbar.TFrame")
        toolbar.pack(side="top", fill="x")

        # Añade botones a la Toolbar con imágenes y texto
        new_button = ttk.Button(toolbar, image=self.image_trabajador, text="Trabajadores", compound="top",
                                command=self.on_new, style="Toolbar.TButton")
        new_button.pack(side="left", padx=5)

        open_button = ttk.Button(toolbar, image=self.image_marca, text="Asistencia", compound="top", command=self.on_open,
                                 style="Toolbar.TButton")
        open_button.pack(side="left", padx=5)

        reporte_button = ttk.Button(toolbar, image=self.image_reporte, text="Reporte", compound="top",
                                  command=self.on_reporte, style="Toolbar.TButton")
        reporte_button.pack(side="left", padx=5)

        exit_button = ttk.Button(toolbar, image=self.image_exit, text="Salir", compound="top",
                                  command=self.on_exit, style="Toolbar.TButton")
        exit_button.pack(side="left", padx=5)

    def on_new(self):
        print("Se seleccionó Nuevo")

    def on_open(self):
        # Abre main.py como un proceso secundario y configura el tamaño de la ventana
        subprocess.run(['python', 'main.py', '--resize'])

    def on_reporte(self):
        reporte_viewer = ReporteViewer()
        reporte_viewer.iniciar()

    def on_exit(self):
        # Muestra un messagebox para confirmar la salida
        confirmar_salida = messagebox.askokcancel("Confirmar salida", "¿Estás seguro de que deseas salir?")
        if confirmar_salida:
            self.destroy()  # Cierra la ventana principal

if __name__ == "__main__":
    app = MainForm()
    app.mainloop()
