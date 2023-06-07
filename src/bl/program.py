import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.api import Holt


class Program: 
    def __init__(self, window):
        self.window = window
        # print(self.window.frame.button.cget("text"))
        self.window.frame.button.configure(command=self.holt)
        self.window.mainloop()

    def holt(self):
        datos = self.window.file["TAVG"]
        entrenamiento_porcentaje = 0.8
        num_entrenamiento = int(len(datos) * entrenamiento_porcentaje)
        entrenamiento = datos[:num_entrenamiento]
        prueba = datos[num_entrenamiento:]
        modelo = Holt(entrenamiento)
        ajuste = modelo.fit()
        proyeccion = ajuste.forecast(steps=len(prueba))
        plt.plot(range(num_entrenamiento), entrenamiento, label='Entrenamiento')
        plt.plot(range(num_entrenamiento, len(datos)), prueba, label='Prueba')
        plt.plot(range(num_entrenamiento, len(datos)), proyeccion, label='Proyección')
        plt.legend()
        plt.show()
    
    def obtainFile(self): 
        datos = self.window.file["TAVG"]
        modelo = Holt(datos)
        ajuste = modelo.fit(optimized=True)
        proyeccion = ajuste.forecast(steps=80)
        plt.plot(datos, label='Datos')
        plt.plot(range(len(datos), len(datos) + len(proyeccion)), proyeccion, label='Proyección')
        plt.legend()
        plt.show()