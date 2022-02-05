import pandas as pd
from sqlalchemy import create_engine
import mysql.connector

def inserta_BD(df,nt,cn):
    df.to_sql(name = nt , con = cn, if_exists = 'replace', index = False)


def conexion_BD():
    
    db= "horarios" #nombre de la tabla en la BD
    url = "mysql+mysqlconnector://root:1234@localhost/" #ruta de conexion
    return create_engine(url+db,echo = False)

def lee_csv(path):
    return pd.read_csv(path)

def BD_connector():
    return mysql.connector.connect(host="localhost", user="root", password="1234",database="horarios")


def Imprime_datos(datos):
    for fila in datos: #itera en cada fila de los datos leidos en la BD y los va imprimiendo
        print(fila)


def Crea_csv_horario(path): #este metodo tiene que recibir el objeto que tenga los datos 
    archivo = path + "/horariosUaslp.csv"
    csv = open(archivo,"w")
    csv.write("cve_alumno,cve_materia,grupo\n")
    #el dataframe seria df, ese seria el objeto que llega "datos"
    for cveal, cvemat, grupo in ObtieneHorario():
       hor= str(cveal) + "," + str(cvemat)  + "," + str(grupo) + "\n"
       print(hor)
       csv.write(hor)

def Leeinserta(path,tablename,engine):
    df = lee_csv(path)
    mensaje = 'Error desconocido, favor de informar a un programador'
    shape = df.shape
    if (tablename == 'alumnos'):
        if(shape[1]==2 and df.columns.values[0] == 'cve_unica' and df.columns.values[1] == 'id_carrera' ):
            mensaje = 'El archivo de los estudiantes fue cargado correctamente'
            inserta_BD(df,tablename,engine)
        else:
            mensaje= 'El archivo  debe tener dos columnas con encabecados: cve_unica, id_carrera'
    elif(tablename == 'materias'):
        if(shape[1]==16 and df.columns.values[0] == 'id_materia' and df.columns.values[1] == 'grupo' and df.columns.values[2] == 'maestro' and df.columns.values[3] == 'cupo' ):
            mensaje = 'El archivo de los grupos fue cargado correctamente'
            inserta_BD(df,tablename,engine)
        else:
            mensaje= 'El archivo debe tener 16 columnas con encabecados: id_materia, grupo, maestro, cupo y los campos de los dias'
            
    elif(tablename == 'carreras'):
        if(shape[1]==2 and df.columns.values[0] == 'id_carrera' and df.columns.values[1] == 'nombre' ):
            mensaje = 'El archivo de las carreras fue cargado correctamente'
            inserta_BD(df,tablename,engine)
        else:
            mensaje= 'El archivo  debe tener dos columnas con encabecados: id_carrera, nombre'

    elif(tablename == 'materia_carrera'):
        if(shape[1]==3 and df.columns.values[0] == 'id_materia' and df.columns.values[1] == 'id_carrera' and df.columns.values[2] == 'nombre' ):
            mensaje = 'El archivo de las materias fue cargado correctamente'
            inserta_BD(df,tablename,engine)
        else:
            mensaje= 'El archivo  debe tener tres columnas con encabecados: id_materia, id_carrera, nombre'

    return mensaje

#Consultas para menejo de datos SQL
#  -----------------------------------------------------------------
#Regresa cuantas materias tiene que llevar el alumno x 
def Materias_de_Alumno(cveunica):
    cnn = BD_connector() #crear conexion con la BD
    cur = cnn.cursor() #crear un objeto cursor para moverse en los datos de la BD
    cur.execute("SELECT count(m.id_materia) FROM horarios.materia_carrera as m WHERE m.id_carrera = ( select a.id_carrera from horarios.alumnos as a where a.cve_unica = "+str(cveunica)+ " )") # consulta en  SQL
    datos = cur.fetchall() # obtener en un objeto los datos de la tabla
    cur.close() #cerrar cursor
    cnn.close() #cerrar conexion 
    return datos #regresar los datos consultados

#Regresa cuantas materias tiene inscritas un alumno 
def Materias_inscritas(cveunica):
    cnn = BD_connector() #crear conexion con la BD
    cur = cnn.cursor() #crear un objeto cursor para moverse en los datos de la BD
    cur.execute("select count(h.cve_unica) from horarios.horarios as h where h.cve_unica = "+str(cveunica)+"") # consulta en  SQL
    datos = cur.fetchall() # obtener en un objeto los datos de la tabla
    cur.close() #cerrar cursor
    cnn.close() #cerrar conexion 
    return datos #regresar los datos consultados

#regresa todas las claves de los alumnos
def Regresa_cves_alumnos():
    cnn = BD_connector() #crear conexion con la BD
    cur = cnn.cursor() #crear un objeto cursor para moverse en los datos de la BD
    cur.execute("select cve_unica from horarios.alumnos") # consulta en  SQL
    datos = cur.fetchall() # obtener en un objeto los datos de la tabla
    cur.close() #cerrar cursor
    cnn.close() #cerrar conexion 
    return datos #regresar los datos consultados


def Numero_Alumnos():
    cnn = BD_connector() #crear conexion con la BD
    cur = cnn.cursor() #crear un objeto cursor para moverse en los datos de la BD
    cur.execute("SELECT count(*) FROM alumnos") # consulta en  SQL
    datos = cur.fetchall() # obtener en un objeto los datos de la tabla
    cur.close() #cerrar cursor
    cnn.close() #cerrar conexion 
    return datos #regresar los datos consultados

def Lista_materias():
    cnn = BD_connector() #crear conexion con la BD
    cur = cnn.cursor() #crear un objeto cursor para moverse en los datos de la BD
    cur.execute("select distinct id_materia from horarios.materia_carrera order by id_materia") # consulta en  SQL
    datos = cur.fetchall() # obtener en un objeto los datos de la tabla
    cur.close() #cerrar cursor
    cnn.close() #cerrar conexion 
    return datos #regresar los datos consultados

def Consulta_Tabla(tablename):
    cnn = BD_connector() #crear conexion con la BD
    cur = cnn.cursor() #crear un objeto cursor para moverse en los datos de la BD
    cur.execute("SELECT * FROM "+ tablename) # consulta en  SQL
    datos = cur.fetchall() # obtener en un objeto los datos de la tabla
    cur.close() #cerrar cursor
    cnn.close() #cerrar conexion 
    return datos #regresar los datos consultados

def MateriasdeCarreraSegunAlumno(cveunica):
    cnn = BD_connector() #crear conexion con la BD
    cur = cnn.cursor() #crear un objeto cursor para moverse en los datos de la BD
    cur.execute( "SELECT m.id_materia, m.id_carrera, m.Nombre FROM materia_carrera as m WHERE m.id_carrera = ( select a.id_carrera from alumnos as a where a.cve_unica =" + str(cveunica) + ")" ) # consulta en  SQL
    datos = cur.fetchall() # obtener en un objeto los datos de la tabla
    cur.close() #cerrar cursor
    cnn.close() #cerrar conexion 
    return datos #regresar los datos consultados

def Obtiene_Grupo(idmateria,grupo):
    cnn = BD_connector() #crear conexion con la BD
    cur = cnn.cursor() #crear un objeto cursor para moverse en los datos de la BD
    cur.execute("select * from horarios.materias where id_materia ="+str(idmateria)+" and grupo = "+str(grupo)) # consulta en  SQL
    datos = cur.fetchall() # obtener en un objeto los datos de la tabla
    cur.close() #cerrar cursor
    cnn.close() #cerrar conexion 
    return datos #regresar los datos consultados


def ObtieneGrupos(idmateria):
    cnn = BD_connector() #crear conexion con la BD
    cur = cnn.cursor() #crear un objeto cursor para moverse en los datos de la BD
    cur.execute("SELECT * FROM materias as m  WHERE m.id_materia = " + str(idmateria) + " and cupo != 0") # consulta en  SQL
    datos = cur.fetchall() # obtener en un objeto los datos de la tabla
    cur.close() #cerrar cursor
    cnn.close() #cerrar conexion 
    return datos #regresar los datos consultados

def ObtieneGruposEquitativo(idmateria):
    cnn = BD_connector() #crear conexion con la BD
    cur = cnn.cursor() #crear un objeto cursor para moverse en los datos de la BD
    cur.execute("SELECT * FROM horarios.materias as m  WHERE m.id_materia = " + str(idmateria) + " and cupo != 0 order by m.cupo desc") # consulta en  SQL
    datos = cur.fetchall() # obtener en un objeto los datos de la tabla
    cur.close() #cerrar cursor
    cnn.close() #cerrar conexion 
    return datos #regresar los datos consultados

def ObtieneHorario():
    cnn = BD_connector() #crear conexion con la BD
    cur = cnn.cursor() #crear un objeto cursor para moverse en los datos de la BD
    cur.execute("SELECT * FROM horarios.horarios") # consulta en  SQL
    datos = cur.fetchall() # obtener en un objeto los datos de la tabla
    cur.close() #cerrar cursor
    cnn.close() #cerrar conexion 
    return datos #regresar los datos consultados


def DecrementaCupo(idmateria,grupo):
    cnn = BD_connector() #crear conexion con la BD
    cur = cnn.cursor() #crear un objeto cursor para moverse en los datos de la BD
    consql = "UPDATE horarios.materias as m SET m.cupo = m.cupo - 1 where m.id_materia = "+ str(idmateria) +" and m.grupo = "+ str(grupo)
    #print(consql)
    cur.execute(consql) # consulta en  SQL
    cnn.commit() #cerrar conexion 
    cur.close() #cerrar cursor

def AumentaCupo(idmateria,grupo):
    cnn = BD_connector() #crear conexion con la BD
    cur = cnn.cursor() #crear un objeto cursor para moverse en los datos de la BD
    consql = "UPDATE horarios.materias as m SET m.cupo = m.cupo + 1 where m.id_materia = "+ str(idmateria) +" and m.grupo = "+ str(grupo)
    #print(consql)
    cur.execute(consql) # consulta en  SQL
    cnn.commit() #cerrar conexion 
    cur.close() #cerrar cursor

def Elimina_materia(cveunica,idmateria):
    cnn = BD_connector() #crear conexion con la BD
    cur = cnn.cursor() #crear un objeto cursor para moverse en los datos de la BD
    consql = "delete from horarios.horarios where cve_unica = "+str(cveunica)+" and id_materia = " + str(idmateria)
    #print(consql)
    cur.execute(consql) # consulta en  SQL
    cnn.commit() #cerrar conexion 
    cur.close() #cerrar cursor
    

def InsertaMateria(cveunica, idmateria, grupo):
    cnn = BD_connector() #crear conexion con la BD
    cur = cnn.cursor() #crear un objeto cursor para moverse en los datos de la BD
    cur.execute("insert into horarios.horarios(cve_unica, id_materia, grupo) values('"+ str(cveunica)+ "', '"+str(idmateria)+"', '"+str(grupo)+"')") # consulta en  SQL
    cnn.commit() #cerrar conexion 
    cur.close() #cerrar cursor
    
def BorrarHorarios():
    cnn = BD_connector() #crear conexion con la BD
    cur = cnn.cursor() #crear un objeto cursor para moverse en los datos de la BD
    cur.execute("truncate table horarios") # consulta en  SQL
    cnn.commit() #cerrar conexion 
    cur.close() #cerrar cursor

##-------Pruebas en comentarios Ignorar---------

#count = 0
#for a,b,c in ObtieneHorario():
#    print(str(a),str(b),str(c))
#    count += 1
#    if(count == 100):
#        break
    


#DecrementaCupo(0,1)
#Alumno = cl.Horario(275507)

#grupos = Lectura.ObtieneGrupos(0) 
#columnas       0       1       2         3       4       5       6       7         8       9       10
#metadaro   idmateria  grupo   maestro  cupo    lun_i   lun_fin  mart_i  mart_fin  .......
#for item in grupos:
    #verificar el grupo no se empalma con el horario que ya se tiene
#    dia=0

    #Si la bandera se queda en 0 entonces significa que ya existe una clase en la hora de el grupo que se quiere meter si no
    #el algoritmo setea la clase con un 1 en las horas 
        #escribir en una tabla de BD el horario o guardar clave alumno, clave materia , grupo
    #dia=0
    #for i in range(0,10,2):
    #    if(item[i+4] != 0):
    #        Alumno.SetHora(item[i+4],item[i+5],dia)
    #    dia = dia + 1
    #break

#Alumno.ImprimeMatriz()

#InsertaMateria(2542,4588,1)

#grups = ObtieneGrupos(4500)
#for item in grups: 
#    print(item[0])


#for i in range(0,10,2):
#    print(i)

#numero = Numero_Alumnos()
#for num in numero:
#   numero = num[0]
            
#print (numero)
def tabla_materias_inscritas(cveunica):
    cnn = BD_connector() #crear conexion con la BD
    cur = cnn.cursor() #crear un objeto cursor para moverse en los datos de la BD
    cur.execute("select id_materia, grupo from horarios.horarios where cve_unica = "+str(cveunica)+"") # consulta en  SQL
    datos = cur.fetchall() # obtener en un objeto los datos de la tabla
    cur.close()
    return datos #regresar los datos consultados

def alumno_completo(cveunica):
    return Materias_inscritas(cveunica) == Materias_de_Alumno(cveunica)