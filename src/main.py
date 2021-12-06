import os
import AlgorithmV1 as A
import threading 

from user_interface import UI

def generate_schedule():
	pass
	#A.AlgoritmoIterativoV2()
	#A.AlgoritmoIterativoV1()

interface = UI(generate_function = generate_schedule)
if __name__ == "__main__":
	target=interface.run()