from tkinter import *
from tkinter import filedialog

def ask_filename_csv(root: Tk):
	root.filename = filedialog.askopenfilename(title="Selecciona un archivo", 
											   filetypes=(("csv", "*.csv"), ("", "")))

class UI(object):
	"""docstring for UI"""
	def __init__(self, generate_function) -> None:
		self.root = Tk()
		self.root.title("Generación de horarios")

		self.open_estudiantes_button = Button(self.root, text="Abrir CSV de estudiantes", 
											  command=self.update_estudiantes_filename)
		self.open_grupos_button = Button(self.root, text="Abrir CSV de Grupos", 
										 command=self.update_grupos_filename)
		self.open_carreras_button = Button(self.root, text="Abrir CSV de Carreras", 
										   command=self.update_carreras_filename)
		self.open_materias_button = Button(self.root, text="Abrir CSV de materias", 
										   command=self.update_materias_filename)

		self.generate_schedules_button = Button(self.root, text="Generar horarios", 
												command=generate_function)

		self.build_ui()

	def run(self) -> None:
		self.root.mainloop()

	def update_estudiantes_filename(self) -> None:
		self.estudiantes_filename = ask_filename_csv(self.root)

	def update_grupos_filename(self) -> None:
		self.grupos_filename = ask_filename_csv(self.root)

	def update_carreras_filename(self) -> None:
		self.carreras_filename = ask_filename_csv(self.root)

	def update_materias_filename(self) -> None:
		self.materias_filename = ask_filename_csv(self.root)

	def build_ui(self) -> None:
		self.open_estudiantes_button.pack()
		self.open_grupos_button.pack()
		self.open_carreras_button.pack()
		self.open_materias_button.pack()
		self.generate_schedules_button.pack()

		
		