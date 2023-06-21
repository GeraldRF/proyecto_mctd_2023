import pandas as pd
from statsmodels.tsa.api import Holt
from statsmodels.tsa.api import ExponentialSmoothing
from statsmodels.tsa.api import SimpleExpSmoothing
from sklearn.metrics import mean_absolute_error
from openpyxl import Workbook
from openpyxl.drawing.image import Image as xlImage
from PIL import Image
import io
import numpy as np

class Program: 
    def __init__(self, window):
        self.window = window
        # print(self.window.frame.button.cget("text"))
        self.window.buttonAnalyzeHolt.configure(command=self.holt)
        self.window.buttonAnalyzeWinters.configure(command=self.winters)
        self.window.buttonAnalyzeSimpleExp.configure(command=self.simplexExp)
        self.window.restartButton.configure(command=self.restartDataResumeAndGraphics)
        self.window.exportButton.configure(command=self.window.exportFileToExcel)
        self.window.mainloop()

   
    def holt(self):
        data = {}
        data['TAVG'] = self.window.file["TAVG"]
        training_percentage = 0.5
        training_count = int(len(data['TAVG']) * training_percentage)
        
        data['DATE'] = pd.to_datetime(self.window.file['DATE'])
        data = pd.DataFrame(data)  # Convierte el diccionario en un DataFrame de pandas
        data = data.set_index('DATE') 
        date_index = pd.date_range(start=self.window.file['DATE'][0], periods=len(self.window.file['DATE']), freq='D')
        data.index = date_index

        training_data = data[:training_count]
        test_data = data[training_count:]
        
        if self.window.alfa_entry_holt.get() != "":
            alpha = float(self.window.alfa_entry_holt.get())
        else:
            alpha = None
            
        if self.window.beta_entry_holt.get() != "":
            beta = float(self.window.beta_entry_holt.get())
        else:
            beta = None

        model = Holt(data, exponential=False)

        if alpha and beta:
            model_fit = model.fit(smoothing_level=alpha, smoothing_trend=beta, optimized=False)
        else:
            model_fit = model.fit()

        test_data.index = pd.date_range(start=test_data.index[0], periods=len(test_data), freq='D')

        forecast = model_fit.predict(start=test_data.index[0], end=test_data.index[-1])
        
        print(forecast)
        
        mae = mean_absolute_error(test_data, forecast)
    
        self.window.mca.configure(text=f"Error medio absolute: {mae}")
        self.window.mca.configure(state="normal")
        
        self.window.frameHolt.show_graph(data, forecast, training_data, test_data, training_count)
        self.window.theCanvas = self.window.frameHolt.canvas
        self.window.restartButton.configure(state="enabled")
        self.window.exportButton.configure(state="enabled")

    def winters(self):
        data = {}
        data['TAVG'] = self.window.file["TAVG"]
        training_percentage = 0.8
        training_count = int(len(data['TAVG']) * training_percentage)
        
        data['DATE'] = pd.to_datetime(self.window.file['DATE'])
        data = pd.DataFrame(data)  # Convierte el diccionario en un DataFrame de pandas
        data = data.set_index('DATE') 
        date_index = pd.date_range(start=self.window.file['DATE'][0], periods=len(self.window.file['DATE']), freq='D')
        data.index = date_index

        training_data = data[:training_count]
        test_data = data[training_count:]

        model = ExponentialSmoothing(training_data, trend="add", seasonal="mul", seasonal_periods=365)
        
        if self.window.alfa_entry_winters.get() != "":
            alpha = float(self.window.alfa_entry_winters.get())
        else:
            alpha = None
            
        if self.window.beta_entry_winters.get() != "":
            beta = float(self.window.beta_entry_winters.get())
        else:
            beta = None
            
        if self.window.gamma_entry_winters.get() != "":
            gamma = float(self.window.gamma_entry_winters.get())
        else:
            gamma = None
        
        if alpha and beta and gamma:
            model_fit = model.fit(smoothing_level=alpha, smoothing_trend=beta, smoothing_seasonal=gamma, optimized=False)
        else:
            model_fit = model.fit()

        test_data.index = pd.date_range(start=test_data.index[0], periods=len(test_data), freq='D')

        forecast = model_fit.predict(start=test_data.index[0], end=test_data.index[-1])
        
        print(forecast)
        
        mae = mean_absolute_error(test_data, forecast)
        
        self.window.mca.configure(text=f"Error medio absolute: {mae}")
        self.window.mca.configure(state="normal")

        self.window.frameWinters.show_graph(data, forecast, training_data, test_data, training_count)
        
        self.window.theCanvas = self.window.frameWinters.canvas
        self.window.restartButton.configure(state="enabled")
        self.window.exportButton.configure(state="enabled")

    def simplexExp(self):
        data = {}
        data['TAVG'] = self.window.file["TAVG"]
        training_percentage = 0.5
        training_count = int(len(data['TAVG']) * training_percentage)
        
        data['DATE'] = pd.to_datetime(self.window.file['DATE'])
        data = pd.DataFrame(data)  # Convierte el diccionario en un DataFrame de pandas
        data = data.set_index('DATE') 
        date_index = pd.date_range(start=self.window.file['DATE'][0], periods=len(self.window.file['DATE']), freq='D')
        data.index = date_index

        training_data = data[:training_count]
        test_data = data[training_count:]
        
        if self.window.alfa_entry_simple.get() != "":
            alpha = float(self.window.alfa_entry_simple.get())
        else:
            alpha = None
            
        model = SimpleExpSmoothing(data)
        
        if alpha:
            model_fit = model.fit(smoothing_level=alpha, optimized=False)
        else:
            model_fit = model.fit()
        
        test_data.index = pd.date_range(start=test_data.index[0], periods=len(test_data), freq='D')

        forecast = model_fit.predict(start=test_data.index[0], end=test_data.index[-1])
        
        print(forecast)
        
        mae = mean_absolute_error(test_data, forecast)

        self.window.mca.configure(text=f"Error medio absolute: {mae}")
        self.window.mca.configure(state="normal")

        self.window.frameSimpleExp.show_graph(data, forecast, training_data, test_data, training_count)
        self.window.theCanvas = self.window.frameSimpleExp.canvas
        self.window.restartButton.configure(state="enabled")
        self.window.exportButton.configure(state="enabled")

    @staticmethod
    def showDataResume(file):
        dataResume = []
        dataResume.append(file['TAVG'].mean())
        dataResume.append(file['TAVG'].max())
        dataResume.append(file['TAVG'].min())
        dataResume.append(file.loc[file['TAVG'].idxmax(), 'DATE'])
        dataResume.append(file.loc[file['TAVG'].idxmin(), 'DATE'])
        return dataResume
    
    def restartDataResumeAndGraphics(self):
        # self.window.labelLast.configure(text="Last analysis data results: " + " Press Analyze Data button to see your file analysis results.", state="disabled")
        # self.window.label_promedio_tavg.configure(text="Promedio de TAVG: N/A", state="disabled")
        # self.window.label_temp_max.configure(text="Temperatura máxima: N/A", state="disabled")
        # self.window.label_temp_min.configure(text="Temperatura mínima: N/A", state="disabled")
        # self.window.label_fecha_temp_max.configure(text="Fecha con temperatura máxima: N/A", state="disabled")
        # self.window.label_fecha_temp_min.configure(text="Fecha con temperatura mínima: N/A", state="disabled")
        self.window.frameHolt.removeFigure()
        self.window.frameWinters.removeFigure()
        self.window.frameSimpleExp.removeFigure()
        self.window.restartButton.configure(state="disabled")
        self.window.exportButton.configure(state="disabled")
        
    @staticmethod
    def exportFileToExcel(file_data, canvas):
        df = pd.DataFrame([file_data], columns=['TAVG Mean', 'TAVG Max', 'TAVG Min', 'DATE Max', 'DATE Min', 'File Name', 'File Path', 'Excel File'])
        columns_to_drop = ['File Name', 'File Path', 'Excel File']
        df = df.drop(columns=columns_to_drop)
        wb = Workbook()
        ws = wb.active
        headers = list(df.columns)
        ws.append(headers)
        values = list(df.iloc[0])
        ws.append(values)
        image_data = io.BytesIO()
        canvas.print_png(image_data)
        image_data.seek(0)
        pil_image = Image.open(image_data)
        xl_image = xlImage(pil_image)
        ws.add_image(xl_image, 'A10')
        wb.save("data_analysis.xlsx")

    # def obtainFile(self): 
    #     datos = self.window.file["TAVG"]
    #     modelo = Holt(datos)
    #     ajuste = modelo.fit(optimized=True)
    #     proyeccion = ajuste.forecast(steps=80)
    #     plt.plot(datos, label='Datos')
    #     plt.plot(range(len(datos), len(datos) + len(proyeccion)), proyeccion, label='Proyección')
    #     plt.legend()
    #     plt.show()