import random
import math

import numpy as np

import Lectura
import ClaseHorario
import AlgorithmV1



global materias_inscritas
global materias_de_alumno
materias_inscritas = dict()
materias_de_alumno = dict()

global inscripciones_en_movimiento#cveunica, idmateria, grupo
global bajas_en_movimiento
inscripciones_en_movimiento = []
bajas_en_movimiento = []

global incompletos
incompletos = []

def alumno_completo(cveunica):
	global materias_de_alumno
	global materias_inscritas

	if not cveunica in materias_inscritas.keys():
		materias_inscritas[cveunica] = int(0)
		materias_inscritas[cveunica] = Lectura.Materias_inscritas(cveunica)[0][0]
	if not cveunica in materias_de_alumno.keys():
		materias_de_alumno[cveunica] = int(0)
		materias_de_alumno[cveunica] = Lectura.Materias_de_Alumno(cveunica)[0][0]

	return materias_inscritas[cveunica] == materias_de_alumno[cveunica]

def get_claves_alumnos():
	"""retorna una lista de las claves unicas de los alumnos"""
	return range(1, 1141) #talvez se necesita una funcion que retorna las claves de los alumnos

def dar_de_baja_alumno(cveunica):
	global inscripciones_en_movimiento
	global bajas_en_movimiento
	global materias_inscritas

	materias = Lectura.tabla_materias_inscritas(cveunica)
	for id_materia, grupo in materias:
		AlgorithmV1.desinscribe_materia(cveunica, id_materia, grupo)
		bajas_en_movimiento.append((cveunica, id_materia, grupo))
		materias_inscritas[cveunica] -= 1

def get_metricas():
	global incompletos
	incompletos = []
	claves_alumnos = get_claves_alumnos()

	horarios_completos = 0
	for cveunica in claves_alumnos:
		horarios_completos += alumno_completo(cveunica)
		if not alumno_completo(cveunica):
			incompletos.append(cveunica)

	return horarios_completos

def quita_alumnos_incompletos():
	claves_alumnos = get_claves_alumnos()

	for cveunica in claves_alumnos:
		if not alumno_completo(cveunica):
			dar_de_baja_alumno(cveunica)

def genera_siguiente_solucion(T):
	"""se dan de baja todas las materias de T alumnos seleccionados de forma aleatoria
	despues en un orden aleatorio se empiezan a llenar los alumnos
	"""
	global inscripciones_en_movimiento
	global bajas_en_movimiento
	global materias_inscritas

	global incompletos

	claves_alumnos = random.sample(get_claves_alumnos(), 5)

	for cveunica in claves_alumnos:
		dar_de_baja_alumno(cveunica)

	otros_alumnos = random.sample(incompletos, 5)
	for cveunica in otros_alumnos:
		claves_alumnos.append(cveunica)

	random.shuffle(claves_alumnos)

	for cveunica in claves_alumnos:
		materias = Lectura.MateriasdeCarreraSegunAlumno(cveunica)
		for idmat, idcar, nom in materias:
			grupos = Lectura.ObtieneGruposEquitativo(idmat) 
			for item in grupos:
				if(AlgorithmV1.posible_inscribir(cveunica, idmat, item[1])):
					AlgorithmV1.inscribe_materia(cveunica, idmat, item[1])
					inscripciones_en_movimiento.append((cveunica, idmat, item[1]))
					materias_inscritas[cveunica] += 1
					break

def mover_solucion():
	global inscripciones_en_movimiento
	global bajas_en_movimiento
	global materias_inscritas

	inscripciones_en_movimiento = []
	bajas_en_movimiento = []

def mantener_solucion_actual():
	global inscripciones_en_movimiento
	global bajas_en_movimiento
	global materias_inscritas

	for cveunica, idmateria, grupo in inscripciones_en_movimiento:
		AlgorithmV1.desinscribe_materia(cveunica, idmateria, grupo)
		materias_inscritas[cveunica] -= 1

	for cveunica, idmateria, grupo in bajas_en_movimiento:
		AlgorithmV1.inscribe_materia(cveunica, idmateria, grupo)
		materias_inscritas[cveunica] += 1

	inscripciones_en_movimiento = []
	bajas_en_movimiento = []

def enfriamiento_simulado(o_self, T_inicial = 600, alpha = 0.9, L = 5, T_final = 1):
	# print("empieza a optimizar2", get_metricas())
	
	# genera_siguiente_solucion(10)
	# print('#', get_metricas())

	# print(bajas_en_movimiento)

	# mantener_solucion_actual()
	# print('#', get_metricas())

	# return
	funcion_objetivo_actual = get_metricas()
	mejor_funcion_objetivo = funcion_objetivo_actual

	contador = 0;
	total = 100*L

	quita_alumnos_incompletos()

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
			S = funcion_objetivo_actual - funcion_objetivo_siguiente
			aceptacion = pow(math.e, -S/T)
			if U <= aceptacion or S < 0:
				print('#', U, S, funcion_objetivo_actual, funcion_objetivo_siguiente)
				mover_solucion()
				funcion_objetivo_actual = funcion_objetivo_siguiente
			else:
				mantener_solucion_actual()

			mejor_funcion_objetivo = max(mejor_funcion_objetivo, funcion_objetivo_actual)

		T *= alpha

	print(mejor_funcion_objetivo)

	claves_alumnos = random.sample(get_claves_alumnos(), 1100)
	random.shuffle(claves_alumnos)

	quita_alumnos_incompletos()

	for cveunica in claves_alumnos:
		if alumno_completo(cve):
			continue

		materias = Lectura.MateriasdeCarreraSegunAlumno(cveunica)
		for idmat, idcar, nom in materias:
			grupos = Lectura.ObtieneGruposEquitativo(idmat) 
			for item in grupos:
				if(AlgorithmV1.posible_inscribir(cveunica, idmat, item[1])):
					AlgorithmV1.inscribe_materia(cveunica, idmat, item[1])
					inscripciones_en_movimiento.append((cveunica, idmat, item[1]))
					materias_inscritas[cveunica] += 1
					break

	return mejor_funcion_objetivo

#print(get_metricas())