from tkinter import *
from tkinter import filedialog

def ask_filename_csv(root: Tk):
	root.filename = filedialog.askopenfilename(title="Selecciona un archivo", 
											   filetypes=(("csv", "*.csv"), ("", "")))

class UI(object):
	"""docstring for UI"""

	def __init__(self, generate_function) -> None:
		self.root = Tk()
		self.root.title("Generación de Horarios")

		self.label_general = Label(self.root, text="Favor de assiganar todos los archivos para generar los horarios.")
		self.open_estudiantes_button = Button(self.root, text="Abrir CSV de Estudiantes", 
											  command=self.update_estudiantes_filename)
		self.open_grupos_button = Button(self.root, text="Abrir CSV de Grupos", 
										 command=self.update_grupos_filename)
		self.open_carreras_button = Button(self.root, text="Abrir CSV de Carreras", 
										   command=self.update_carreras_filename)
		self.open_materias_button = Button(self.root, text="Abrir CSV de Materias", 
										   command=self.update_materias_filename)

		self.generate_schedules_button = Button(self.root, text="Generar Horarios", 
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
		self.label_general.grid(ipadx=5,ipady=5, row=0, column=0, columnspan=3, sticky=S+N+E+W)
		self.open_estudiantes_button.grid(padx=5,pady=4,ipadx=5,ipady=5, row=1, column=0, sticky=W+E)
		self.open_grupos_button.grid(padx=5,pady=4,ipadx=5,ipady=5, row=2, column=0, sticky=W+E)
		self.open_carreras_button.grid(padx=5,pady=4,ipadx=5,ipady=5, row=3, column=0, sticky=W+E)
		self.open_materias_button.grid(padx=5,pady=4,ipadx=5,ipady=5, row=4, column=0, sticky=W+E)
		self.generate_schedules_button.grid(padx=5,pady=4,ipadx=5,ipady=5, row=5, column=2, sticky=W+E)

		