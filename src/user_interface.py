from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image
import Lectura as L 

def ask_filename_csv(root: Tk):
	filename = filedialog.askopenfilename(title="Selecciona un archivo", 
										  filetypes=(("csv", "*.csv"), ("", "")))
	return filename

class UI(object):
	"""docstring for UI"""
	def __init__(self, generate_function) -> None:
		
		self.root = Tk()
		self.root.title("Generación de Horarios")
		self.root.resizable(False,False)
		self.root.iconbitmap(r'G:/Mi unidad/GenerationofSchedules/Generation-of-schedules/src/icono.ico')
		self.root.config(bg="#E9E9F1")
		self.headerImg = ImageTk.PhotoImage(Image.open(r'G:/Mi unidad/GenerationofSchedules/Generation-of-schedules/src/UASLP.PNG'))
		self.headerLabel = Label(self.root, image=self.headerImg)

		self.label_general = Label(self.root, text="Favor de assiganar todos los archivos para generar los horarios.",bg="#E9E9F1")
		self.label_Metrica = Label(self.root, text=" ",bg="#E9E9F1")
		self.open_estudiantes_button = Button(self.root, text="Abrir CSV de Estudiantes", 
											  command=self.update_estudiantes_filename,bg="#E9E9F1")
		self.open_grupos_button = Button(self.root, text="Abrir CSV de Grupos", 
										 command=self.update_grupos_filename,bg="#E9E9F1")
		self.open_carreras_button = Button(self.root, text="Abrir CSV de Carreras", 
										   command=self.update_carreras_filename,bg="#E9E9F1")
		self.open_materias_button = Button(self.root, text="Abrir CSV de Materias", 
										   command=self.update_materias_filename,bg="#E9E9F1")

		self.generate_schedules_button = Button(self.root, text="Generar Horarios", 
												command=generate_function,bg="#E9E9F1")

		self.build_ui()
    
	global engine 
	engine  = L.conexion_BD() #guarda la conexion en un objeto de conexion

	def run(self) -> None:
		self.root.mainloop()

	def update_estudiantes_filename(self) -> None:
		self.estudiantes_filename = ask_filename_csv(self.root)
		L.Leeinserta(self.estudiantes_filename, "alumnos", engine)

	def update_grupos_filename(self) -> None:
		self.grupos_filename = ask_filename_csv(self.root)
		L.Leeinserta(self.grupos_filename, "materias", engine)

	def update_carreras_filename(self) -> None:
		self.carreras_filename = ask_filename_csv(self.root)
		L.Leeinserta(self.carreras_filename, "materia_carrera", engine)

	def update_materias_filename(self) -> None:
		self.materias_filename = ask_filename_csv(self.root)
		L.Leeinserta(self.materias_filename, "alumnos", engine)

	def build_ui(self) -> None:
		self.headerLabel.grid(				padx=5,pady=4,ipadx=5,ipady=5, row=0, column=0, columnspan=3, sticky=S+N+E+W)
		self.label_general.grid(			padx=5,pady=4,ipadx=5,ipady=5, row=1, column=0, sticky=W)
		#self.label_Metrica.grid(			padx=5,pady=4,ipadx=5,ipady=5, row=2, column=0, sticky=W)
		self.open_estudiantes_button.grid(	padx=5,pady=4,ipadx=5,ipady=5, row=3, column=0, sticky=E+W)
		self.open_grupos_button.grid(		padx=5,pady=4,ipadx=5,ipady=5, row=4, column=0, sticky=E+W)
		self.open_carreras_button.grid(		padx=5,pady=4,ipadx=5,ipady=5, row=5, column=0, sticky=E+W)
		self.open_materias_button.grid(		padx=5,pady=4,ipadx=5,ipady=5, row=6, column=0, sticky=E+W)
		self.generate_schedules_button.grid(padx=5,pady=4,ipadx=5,ipady=5, row=7, column=2, sticky=E+W)

		