import os
import AlgorithmV1 as A
import threading 

from user_interface import UI


interface = UI()
if __name__ == "__main__":
	target=interface.run()


if(A.posible_inscribir(88,84,13) == True):
	print("es correcto")
else:
    print("es incorrecto")

if(A.posible_inscribir(88,84,2) == False):
	print("es correcto")
else:
    print("es incorrecto")