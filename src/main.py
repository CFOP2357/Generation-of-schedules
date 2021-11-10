import os

from user_interface import UI
#########un cambio
def generate_schedule():
	pass

if __name__ == "__main__":
	interface = UI(generate_function = generate_schedule)
	interface.run()