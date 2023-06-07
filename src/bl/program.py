import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.api import Holt
from statsmodels.tsa.api import SimpleExpSmoothing
from statsmodels.tsa.api import ExponentialSmoothing

class Program: 
    def __init__(self, window):
        
        self.window = window
        
        self.window.Holt.activator.configure(command=self.holt)
        self.window.Winters.activator.configure(command=self.winters)
        self.window.SimpleExpSmoothing.activator.configure(command=self.simple_exp_smoothing)
        
        self.window.mainloop()

    def holt(self):
    
        data = self.window.file["TAVG"]
        
        training_percent = 0.8
        nom_training = int(len(data) * training_percent)
        training = data[:nom_training]
        
        prueba = data[nom_training:]
        
        modelo = Holt(training)
        ajuste = modelo.fit()
        proyeccion = ajuste.forecast(steps=len(prueba))
        
        plt.plot(range(nom_training), training, label='Entrenamiento')
        plt.plot(range(nom_training, len(data)), prueba, label='Prueba')
        plt.plot(range(nom_training, len(data)), proyeccion, label='Proyección')
        plt.legend()
        plt.show()

    def winters(self):
        
        data = self.window.file["TAVG"]
        
        modelo = ExponentialSmoothing(data, seasonal_periods=4, trend='add', seasonal='add')

        ajuste = modelo.fit()

        proyeccion = ajuste.forecast(steps=5)

        plt.plot(data, label='data')
        plt.plot(range(len(data), len(data) + len(proyeccion)), proyeccion, label='Proyección')
        plt.legend()
        plt.show()
        
    def simple_exp_smoothing(self):
        
        data = self.window.file["TAVG"]
        
        modelo = SimpleExpSmoothing(data)

        ajuste = modelo.fit()

        proyeccion = ajuste.forecast(steps=5)

        plt.plot(data, label='datos')
        plt.plot(range(len(data), len(data) + len(proyeccion)), proyeccion, label='Proyección')
        plt.legend()
        plt.show()