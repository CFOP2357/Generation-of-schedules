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


def Crea_csv_horario(): #este metodo tiene que recibir el objeto que tenga los datos 
    archivo = "horariosUaslp.csv"
    csv = open(archivo,"w")
    csv.write("cve_alumno,cve_materia,grupo\n")

    #creando un data framework con datos fake
    claves_alumnos = pd.Series(['275648','275648','275648','271864','271864','271864','264821','264821','264821'])
    cve_materias = pd.Series(['5486','8799','5487','6548','2658','4568','5646','6458','6521'])
    gpo = pd.Series(['01','02','01','01','01','01','02','04','02'])
    
    horarios = {'cve_alumno':claves_alumnos,'cve_materias':cve_materias,'grupo':gpo}
    df = pd.DataFrame(data=horarios)
   
    #el dataframe seria df, ese seria el objeto que llega "datos"
    for indice, fila in df.iterrows():
       hor= fila['cve_alumno'] + "," + fila['cve_materias'] + "," + fila['grupo'] + "\n"
       csv.write(hor)

def Leeinserta(path,tablename,engine):
    df = lee_csv(path)
    inserta_BD(df,tablename,engine)

#Consultas para menejo de datos SQL
#  
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


def ObtieneGrupos(idmateria):
    cnn = BD_connector() #crear conexion con la BD
    cur = cnn.cursor() #crear un objeto cursor para moverse en los datos de la BD
    cur.execute("SELECT * FROM horarios.materias as m  WHERE m.id_materia = " + str(idmateria) + "and cupo <> 0") # consulta en  SQL
    datos = cur.fetchall() # obtener en un objeto los datos de la tabla
    cur.close() #cerrar cursor
    cnn.close() #cerrar conexion 
    return datos #regresar los datos consultados

def DecrementaCupo(idmateria,grupo):
    cnn = BD_connector() #crear conexion con la BD
    cur = cnn.cursor() #crear un objeto cursor para moverse en los datos de la BD
    cur.execute("UPDATE horarios.materias as m SET m.cupo = 0 where m.id_materia = "+ str(idmateria) +" and m.grupo = "+ str(grupo)) # consulta en  SQL
    datos = cur.fetchall() # obtener en un objeto los datos de la tabla
    cur.close() #cerrar cursor
    cnn.close() #cerrar conexion 
    return datos #regresar los datos consultados


#grups = ObtieneGrupos(4500)
#for item in grups: 
#    print(item[0])


#for i in range(0,10,2):
#    print(i)