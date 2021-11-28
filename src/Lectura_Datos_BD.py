import Lectura


#instalar las librerias de pandas y de sqlalchemy "pi pandas y pi sqlalchemy"

#Este comentario es para ver los cambios en mi rama

engine = Lectura.conexion_BD() #guarda la conexion en un objeto de conexion 

df = Lectura.lee_csv("D:/Documentos/archivos_p/AlumnosOculto.csv") # se pasa como parametro la ubicacion del csv , obtiene el dataframework
#df = lee_csv("D:/Documentos/archivos_p/materiaspn.csv") # se pasa como parametro la ubicacion del csv , obtiene el dataframework
#LA LECTURA DE ARCHIVOS COMO CSV NO LEE CARACTERES ESPECIALES COMO ACENTOS O LA LETRA Ñ 

Lectura.inserta_BD(df,"alumnos",engine) #para que inserte lo que leyo del csv en la BD es necesario mandar como parametro el dataFramework, nombre de la tabla y la conexion

#Imprime_datos(Consulta_Tabla("alumnos")) # imprime los datos que se guardaron en la BD

Lectura.Crea_csv_horario(Lectura.Consulta_Tabla("alumnos"))