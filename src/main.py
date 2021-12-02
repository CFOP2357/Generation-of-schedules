import os
import AlgorithmV1 as A

from user_interface import UI

def generate_schedule():
	A.AlgoritmoIterativoV2()
	#A.AlgoritmoIterativoV1()

interface = UI(generate_function = generate_schedule)
if __name__ == "__main__":
	interface.run()