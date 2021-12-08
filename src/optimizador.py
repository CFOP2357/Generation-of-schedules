import Lectura
import ClaseHorario
import AlgorithmV1

def get_metricas():
	claves_alumnos = range(1, 1141) #talvez se necesita una funcion que retorna las claves de los alumnos

	horarios_completos = 0
	for cveunica in claves_alumnos:
		print(cveunica, Lectura.alumno_completo(cveunica))
		horarios_completos += Lectura.alumno_completo(cveunica)

	distribucion = 0
	"""for cveunica in claves_alumnos:
		horario_booleano = AlgorithmV1.get_matriz_cupo(cveunica)"""

	return horarios_completos#, distribucion

print(get_metricas())