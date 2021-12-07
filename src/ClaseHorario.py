import numpy as np


class Horario: 

    def __init__(self,cveunica):
        self.cveu = cveunica
        #14 porque son las horas disponibles al dia, es decir de 7-8, 8-9 etc, 6 son los dias de lunes a sabado 
        #se inicializa en 0's ya que un 0 significa que no hay nada asignado y un 1 significa que ya esta ocupado ese lugar 
        self.matrizHor = np.zeros((14,6)) 
    
#Metodo para mapear el horario , pone un 1 en la hora y dia que le llega como parametro
    def SetHora(self, HoraInicio, HoraFinal, Dia):
        self.matrizHor[HoraInicio-7,Dia] = 1
        if(HoraFinal>HoraInicio+1):
            if(HoraFinal==HoraInicio+2):
                self.matrizHor[HoraFinal - (7 + 1),Dia] = 1
            elif(HoraFinal==HoraInicio+3):
                self.matrizHor[HoraFinal - (7 + 1),Dia] = 1
                self.matrizHor[HoraFinal - (7 + 2),Dia] = 1
    
    def QuitHora(self, HoraInicio, HoraFinal, Dia):
        self.matrizHor[HoraInicio-7,Dia] = 0
        if(HoraFinal>HoraInicio+1):
            if(HoraFinal==HoraInicio+2):
                self.matrizHor[HoraFinal - (7 + 1),Dia] = 0
            elif(HoraFinal==HoraInicio+3):
                self.matrizHor[HoraFinal - (7 + 1),Dia] = 0
                self.matrizHor[HoraFinal - (7 + 2),Dia] = 0

#Con base en los parametros que llegan checa en la matriz si tiene un 1 , si es asi
#esta ocupado.
    def VerificaOcupadoxDia(self, HoraInicio,HoraFinal,Dia):
        bandera = 1
        if(self.matrizHor[HoraInicio-7,Dia] == 1):
          bandera = 0
        elif(self.matrizHor[HoraFinal-8,Dia] == 1):
          bandera = 0
        return bandera
    
    def VerificaOcupado(self,item):
        dia=0
        bandera = 1
        for i in range(0,10,2):
            if(item[i+4] != 0):
                if(self.VerificaOcupadoxDia(item[i+4],item[i+5],dia) == 0):
                    bandera=0
                    break
            dia = dia + 1
        return bandera
    
    def Inscribe_materia_matriz(self, item):
        dia=0
        for i in range(0,10,2):
            if(item[i+4] != 0):
                self.SetHora(item[i+4],item[i+5],dia)
            dia = dia + 1

    def Desinscribe_materia_matriz(self, item):
        dia=0
        for i in range(0,10,2):
            if(item[i+4] != 0):
                self.QuitHora(item[i+4],item[i+5],dia)
            dia = dia + 1


#imprime matriz
    def ImprimeMatriz(self):
        print (self.matrizHor)

