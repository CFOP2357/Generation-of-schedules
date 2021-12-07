import Lectura
import ClaseHorario as cl

#instalar las librerias de pandas y de sqlalchemy "pi pandas y pi sqlalchemy"

engine = Lectura.conexion_BD() #guarda la conexion en un objeto de conexion 


#Leer todos los archivos
#df = Lectura.lee_csv("C:/Users/angel/Documents/python/archivos_csv/AlumnosOculto.csv") # se pasa como parametro la ubicacion del csv , obtiene el dataframework
#df = lee_csv("D:/Documentos/archivos_p/materiaspn.csv") # se pasa como parametro la ubicacion del csv , obtiene el dataframework
#LA LECTURA DE ARCHIVOS COMO CSV NO LEE CARACTERES ESPECIALES COMO ACENTOS O LA LETRA Ñ 

#print(df)
#Lectura.inserta_BD(df,"alumnos",engine) #para que inserte lo que leyo del csv en la BD es necesario mandar como parametro el dataFramework, nombre de la tabla y la conexion


#Lectura.Leeinserta("C:/Users/angel/Documents/python/archivos_csv/AlumnosOculto.csv", "alumnos", engine)
#Lectura.Leeinserta("C:/Users/angel/Documents/python/archivos_csv/carreras.csv","carreras",engine)
#Lectura.Leeinserta("C:/Users/angel/Documents/python/archivos_csv/materia_carrera.csv","materia_carrera",engine)
#Lectura.Leeinserta("C:/Users/angel/Documents/python/archivos_csv/materias.csv","materias",engine)

Lectura.BorrarHorarios()

#Algoritmo iterativo 
def AlgoritmoIterativoV1(o_self):
    #primero obtener todos los alumnos 
    df = Lectura.Consulta_Tabla("alumnos")
    contador = 0

    #La tabla alumnos contiene 2 columnas cve_unica y id_carrera por lo tanto df sera una matriz de 2*n alumnos por lo que 
    #por lo que el for que va mas afuera sera el de los alumnos 
    #Crear una lista de alumnos
    Al = cl.Horario(2000) #Alumno fake para inicializar la pila 
    PilaAlumnos = [Al]
    
    for cveunica,idcarrera in df:
        #con este for ya estariamos iterando en todos los alumnos, lo siquiente que hay que hacer es obtner cuales son las materias que se 
        #tienen que inscribir a este alumno segun su carrera
        o_self.progreso.set(contador)
        contador += 1
        o_self.master.update_idletasks()#esta funcion nos permite lograr percibir el avance de la barra
        #Instanciar un nuevo alumno 
        Alumno = cl.Horario(cveunica)
        
        materias = Lectura.MateriasdeCarreraSegunAlumno(cveunica)
        #Segundo iterador for para navegar entre las materias que necesita inscribir el alumno 
        for idmat, idcar, nom in materias: #for iterador de materias
            #por cada materia obtener los grupos que hay de ella y que aun tengan cupo 
            #verificar lo siguiente: 2. Es la primer materia del alumno?. 3 Si no es la primera, iterar en los demas grupos para ver cual grupo esta mas cerca
            # Cuando se encuentre el grupo mas cercano asignarle ese a su horario y 1. Bajarle el cupo. 2. Asignar a matriz horario del alumno
            grupos = Lectura.ObtieneGrupos(idmat) 
            #columnas       0       1       2         3       4       5       6       7         8       9       10
            #metadaro   idmateria  grupo   maestro  cupo    lun_i   lun_fin  mart_i  mart_fin  .......
            for item in grupos:
                #verificar el grupo no se empalma con el horario que ya se tiene
                dia=0
                bandera = 1
                for i in range(0,10,2):
                    if(item[i+4] != 0):
                        if(Alumno.VerificaOcupado(item[i+4],item[i+5],dia) == 0):
                            bandera=0
                            break
                    dia = dia + 1

                #Si la bandera se queda en 0 entonces significa que ya existe una clase en la hora de el grupo que se quiere meter si no
                #el algoritmo setea la clase con un 1 en las horas 
                if(bandera != 0):
                    #escribir en una tabla de BD el horario o guardar clave alumno, clave materia , grupo
                    dia=0
                    for i in range(0,10,2):
                        if(item[i+4] != 0):
                            Alumno.SetHora(item[i+4],item[i+5],dia)
                        dia = dia + 1
                    #Dentro de este if tendria que guardar en la base de datos al alumno con la materia y grupo que se acaba de crear 
                    Lectura.InsertaMateria(cveunica,idmat,item[1])
                    #Decrementar en uno el cupo de la materia
                    Lectura.DecrementaCupo(item[0],item[1])
                    break
                
    PilaAlumnos.append(Alumno) #Se asigna el alumno a la pila 


def AlgoritmoIterativoV2(o_self):
    #primero obtener todos los alumnos 
    df = Lectura.Consulta_Tabla("alumnos")
    contador = 0
    #La tabla alumnos contiene 2 columnas cve_unica y id_carrera por lo tanto df sera una matriz de 2*n alumnos por lo que 
    #por lo que el for que va mas afuera sera el de los alumnos 
    #Crear una lista de alumnos

    
    for cveunica,idcarrera in df:
        #con este for ya estariamos iterando en todos los alumnos, lo siquiente que hay que hacer es obtner cuales son las materias que se 
        #tienen que inscribir a este alumno segun su carrera

        #Instanciar un nuevo alumno 
        Alumno = cl.Horario(cveunica)
        o_self.progreso.set(contador)
        contador += 1
        o_self.root.update_idletasks()#esta funcion nos permite lograr percibir el avance de la barra
        materias = Lectura.MateriasdeCarreraSegunAlumno(cveunica)
        #Segundo iterador for para navegar entre las materias que necesita inscribir el alumno 
        for idmat, idcar, nom in materias: #for iterador de materias
            #por cada materia obtener los grupos que hay de ella y que aun tengan cupo 
            #verificar lo siguiente: 2. Es la primer materia del alumno?. 3 Si no es la primera, iterar en los demas grupos para ver cual grupo esta mas cerca
            # Cuando se encuentre el grupo mas cercano asignarle ese a su horario y 1. Bajarle el cupo. 2. Asignar a matriz horario del alumno
            grupos = Lectura.ObtieneGruposEquitativo(idmat) 
            #columnas       0       1       2         3       4       5       6       7         8       9       10
            #metadaro   idmateria  grupo   maestro  cupo    lun_i   lun_fin  mart_i  mart_fin  .......
            for item in grupos:
                #verificar el grupo no se empalma con el horario que ya se tiene
                dia=0
                bandera = 1
                for i in range(0,10,2):
                    if(item[i+4] != 0):
                        if(Alumno.VerificaOcupado(item[i+4],item[i+5],dia) == 0):
                            bandera=0
                            break
                    dia = dia + 1

                #Si la bandera se queda en 0 entonces significa que ya existe una clase en la hora de el grupo que se quiere meter si no
                #el algoritmo setea la clase con un 1 en las horas 
                if(bandera != 0):
                    #escribir en una tabla de BD el horario o guardar clave alumno, clave materia , grupo
                    dia=0
                    for i in range(0,10,2):
                        if(item[i+4] != 0):
                            Alumno.SetHora(item[i+4],item[i+5],dia)
                        dia = dia + 1
                    #Dentro de este if tendria que guardar en la base de datos al alumno con la materia y grupo que se acaba de crear 
                    Lectura.InsertaMateria(cveunica,idmat,item[1])
                    #Decrementar en uno el cupo de la materia
                    Lectura.DecrementaCupo(item[0],item[1])
                    break
                


#AlgoritmoIterativoV2()
#Lectura.Imprime_datos(Lectura.Consulta_Tabla("alumnos")) # imprime los datos que se guardaron en la BD

#Lectura.Crea_csv_horario(Lectura.Consulta_Tabla("alumnos"))
