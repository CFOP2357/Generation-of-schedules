import random
import math

import numpy as np

import Lectura
import ClaseHorario
import AlgorithmV1



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

def get_claves_alumnos():
	"""retorna una lista de las claves unicas de los alumnos"""
	return range(1, 1141) #talvez se necesita una funcion que retorna las claves de los alumnos

def get_metricas():
	claves_alumnos = get_claves_alumnos()

	horarios_completos = 0
	for cveunica in claves_alumnos:
		horarios_completos += alumno_completo(cveunica)

	return horarios_completos

def genera_siguiente_solucion(T):
	"""se dan de baja todas las materias de T alumnos seleccionados de forma aleatoria
	despues en un orden aleatorio se empiezan a llenar los alumnos
	"""
	claves_alumnos = random.sample(get_claves_alumnos(), 5)
	random.shuffle(claves_alumnos)

	for cveunica in claves_alumnos:
		materias = Lectura.tabla_materias_inscritas(cveunica)
		for id_materia, grupo in materias:
			AlgorithmV1.desinscribe_materia(cveunica, id_materia, grupo)
			bajas_en_movimiento.append((cveunica, id_materia, grupo))

		materias_inscritas[cveunica] = 0

	for cveunica in claves_alumnos:
		materias = Lectura.MateriasdeCarreraSegunAlumno(cveunica)
		for idmat, idcar, nom in materias:
			grupos = Lectura.ObtieneGruposEquitativo(idmat) 
			for item in grupos:
				if(AlgorithmV1.posible_inscribir(cveunica, idmat, item)):
					AlgorithmV1.inscribe_materia(cveunica, idmateria, grupo)
					inscripciones_en_movimiento.append((cveunica, idmateria, grupo))
					materias_inscritas[cveunica] += 1
					break

def mover_solucion():
	inscripciones_en_movimiento = []
	bajas_en_movimiento = []

def mantener_solucion_actual():
	for cveunica, idmateria, grupo in inscripciones_en_movimiento:
		AlgorithmV1.desinscribe_materia(cveunica, idmateria, grupo)
		materias_inscritas[cveunica] -= 1

	for cveunica, idmateria, grupo in bajas_en_movimiento:
		AlgorithmV1.inscribe_materia(cveunica, idmateria, grupo)
		materias_inscritas[cveunica] += 1

	inscripciones_en_movimiento = []
	bajas_en_movimiento = []

def enfriamiento_simulado(o_self, T_inicial = 1000, alpha = 0.80, L = 10, T_final = 1):
	print("empieza a optimizar2")

	funcion_objetivo_actual = get_metricas()
	mejor_funcion_objetivo = funcion_objetivo_actual

	contador = 0;
	total = 32*L

	T = T_inicial
	while T >= T_final:
		print(T, funcion_objetivo_actual)

		for i in range(1, L):
			contador += 1;
			progreso = 95*contador/total
			o_self.progreso.set(progreso)

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

	print(mejor_funcion_objetivo)

	return mejor_funcion_objetivo

#print(get_metricas())