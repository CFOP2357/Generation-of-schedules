import Lectura
import ClaseHorario
import AlgorithmV1

import random
import math

def get_metricas():
	claves_alumnos = range(1, 1141) #talvez se necesita una funcion que retorna las claves de los alumnos

	horarios_completos = 0
	for cveunica in claves_alumnos:
		print(cveunica, Lectura.alumno_completo(cveunica))
		horarios_completos += Lectura.alumno_completo(cveunica)

	return horarios_completos

def genera_siguiente_solucion(T):
	pass

def mover_solucion():
	pass

def mantener_solucion_actual():
	pass

def enfriamiento_simulado(T_inicial = 1000, alpha = 0.965, L = 500, T_final = 1):
	mejor_funcion_objetivo = get_metricas()

	T = T_inicial
	while T_inicial >= T_final:
		for i in range(1, L):
			genera_siguiente_solucion(T)
			funcion_objetivo_siguiente = get_metricas()

			U = random.uniform(0, 1)
			delta_objetivo = funcion_objetivo_actual - funcion_objetivo_siguiente
			aceptacion = pow(math.e, -delta_objetivo/T)
			if U <= aceptacion or funcion_objetivo_siguiente > funcion_objetivo_actual:
				mover_solucion()
				funcion_objetivo_actual = funcion_objetivo_siguiente
			else:
				mantener_solucion_actual()

			mejor_funcion_objetivo = min(mejor_funcion_objetivo, funcion_objetivo_actual)
			T *= alpha

	return mejor_funcion_objetivo

print(get_metricas())
enfriamiento_simulado()