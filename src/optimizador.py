import Lectura
import ClaseHorario
import AlgorithmV1

import random
import math

materias_inscritas = dict()
materias_de_alumno = dict()

inscripciones_en_movimiento = [] #cveunica, idmateria, grupo
bajas_en_movimiento = []

def alumno_completo(cveunica):
	if not cveunica in materias_inscritas.keys():
		materias_inscritas[cveunica] = Lectura.Materias_inscritas(cveunica)
	if not cveunica in materias_de_alumno.keys():
		materias_de_alumno[cveunica] = Lectura.Materias_de_Alumno(cveunica)

	return materias_inscritas[cveunica] == materias_de_alumno[cveunica]

def get_metricas():
	claves_alumnos = range(1, 1141) #talvez se necesita una funcion que retorna las claves de los alumnos

	horarios_completos = 0
	for cveunica in claves_alumnos:
		horarios_completos += alumno_completo(cveunica)

	return horarios_completos

def genera_siguiente_solucion(T):
"""se dan de baja todas las materias de T alumnos seleccionados de forma aleatoria"""
	pass

def mover_solucion():
	inscripciones_en_movimiento = []
	bajas_en_movimiento = []

def mantener_solucion_actual():
	for cveunica, idmateria, grupo in inscripciones_en_movimiento:
		AlgorithmV1.desinscribe_materia(cveunica, idmateria, grupo)

	for cveunica, idmateria, grupo in bajas_en_movimiento:
		AlgorithmV1.inscribe_materia(cveunica, idmateria, grupo)

	inscripciones_en_movimiento = []
	bajas_en_movimiento = []

def enfriamiento_simulado(T_inicial = 1000, alpha = 0.95, L = 10, T_final = 1):
	funcion_objetivo_actual = get_metricas()
	mejor_funcion_objetivo = funcion_objetivo_actual

	T = T_inicial
	while T >= T_final:
		print(T)

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

#print(get_metricas())
print(enfriamiento_simulado())
#print(get_metricas())

Lectura.close()