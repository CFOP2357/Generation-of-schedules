import os
import Lectura

from user_interface import UI

def generate_schedule():
	Lectura.Crea_csv_horario()
	
interface = UI(generate_function = generate_schedule)
if __name__ == "__main__":
	interface.run()