import os
import Lectura

from user_interface import UI
#########un cambio
def generate_schedule():
	Lectura.Crea_csv_horario()

if __name__ == "__main__":
	interface = UI(generate_function = generate_schedule)
	interface.run()