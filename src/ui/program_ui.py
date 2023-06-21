import os
from PIL import ImageTk, Image
import customtkinter
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import src.bl.program as program
from io import BytesIO

class MyGeneratedGraph(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.image_path_csv = os.path.join(self.project_dir, "assets/files/line-graph.png")
        self.image_csv = Image.open(self.image_path_csv)
       
        self.figure = plt.figure(figsize=(6, 3.5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        
        self.canvas.get_tk_widget().grid(row=2, column=0, padx=10, pady=10)
        self.placeholder_text = self.figure.text(
            0.5, 0.7, "The graph will be displayed here", ha='center', va='center', fontsize=12, color='gray'
        )
        self.image = ImageTk.PhotoImage(self.image_csv)
        self.figure.figimage(self.image_csv, 230, 80, zorder=2)
        
    
    def show_graph(self, datos, proyeccion, entrenamiento, prueba, num_entrenamiento):
        self.figure.clear() 
        ax = self.figure.add_subplot(111)
        ax.plot(entrenamiento, label='Entrenamiento')
        ax.plot(prueba, label='Prueba')
        ax.plot(proyeccion, label='Proyección')
        ax.legend()
        self.placeholder_text.set_text("") 
        self.canvas.draw()

    def show_graphWinters(self, datos, proyeccion, entrenamiento, prueba, num_entrenamiento):
        self.figure.clear() 
        ax = self.figure.add_subplot(111)
        ax.plot(entrenamiento, label='Entrenamiento')
        ax.plot(prueba, label='Prueba')
        ax.plot(proyeccion, label='Proyección')
        ax.legend()
        self.placeholder_text.set_text("")
        self.canvas.draw()

    def removeFigure(self):
        self.figure.clear()
        self.placeholder_text = self.figure.text(
            0.5, 0.7, "The graph will be displayed here", ha='center', va='center', fontsize=12, color='gray'
        )
        self.image = ImageTk.PhotoImage(self.image_csv)
        self.figure.figimage(self.image_csv, 230, 80, zorder=2)
        self.canvas.draw()
        
        
        
class ProgramUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.theCanvas = None
        self.file = None
        self.title("Proyecto - Métodos Cuantitativos 2023")
        self.geometry("1000x780")
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - 1000) // 2
        y = (screen_height - 780) // 2

        self.geometry(f"+{x}+{y}")
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=2)
        self.resizable(False, False)

        self.frameImage = customtkinter.CTkFrame(self)
        self.frameImage.grid(row=0, column=0, padx=10, pady=5, sticky="n")
        self.frameImage.grid_columnconfigure(0, weight=1)

        image_path_csv = os.path.join(self.project_dir, "assets/files/csv.png")
        image_csv = Image.open(image_path_csv)
        my_image = customtkinter.CTkImage(light_image=(image_csv), size=(28, 28))
        image_label = customtkinter.CTkLabel(self.frameImage, image=my_image, text="")  # display image with a CTkLabel
        image_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.labelSelectFile = customtkinter.CTkLabel(self.frameImage, text="Select a .csv file to analyze:")
        self.labelSelectFile.grid(row=0, column=0, padx=50, pady=5, sticky="w")

        self.file_label = customtkinter.CTkLabel(self, text="No file selected", text_color="orange")
        self.file_label.grid(row=1, column=0, padx=0, sticky="nsew")

        image_path_folder = os.path.join(self.project_dir, "assets/files/file-folder.png")
        image_folder = ImageTk.PhotoImage(file=image_path_folder)
        button = customtkinter.CTkButton(self, text="Select a file", image=image_folder, compound="right", command=self.open_file_dialog)
        button.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")

        self.treeview = ttk.Treeview(self)
        self.treeview.grid(row=3, column=0, padx=20, rowspan=7, pady=10, sticky="nsew")
        self.treeview["columns"] = ("Date", "TAVG")
        self.treeview.heading("#0", text="C. Datos")
        self.treeview.column("#0", width=70, anchor="center", stretch=False, minwidth=70)
        for col in self.treeview["columns"]:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=80, anchor="center", minwidth=80)
        scroll_y = customtkinter.CTkScrollbar(self, command=self.treeview.yview)
        scroll_y.grid(row=3, column=0, padx=2, rowspan=7, sticky="nse")
        self.treeview.configure(yscrollcommand=scroll_y.set)

        tabview = customtkinter.CTkTabview(self)
        tabview.grid(row=0, column=1, padx=20, rowspan=8, pady=10, sticky="nsew")

        tabview.add("Holt")
        tabview.add("Winters") 
        tabview.add("Simple Exp. Smoothing")  
        tabview.set("Holt") 

        #Componentes de la pestaña Holt
        self.labelHolt = customtkinter.CTkLabel(master=tabview.tab("Holt"), text="Configure the HOLT method")
        self.labelHolt.grid(row=0, column=1, padx=40, pady=5, sticky="w")
        self.alfa_entry_holt = customtkinter.CTkEntry(master=tabview.tab("Holt"), placeholder_text="Alfa - α")
        self.alfa_entry_holt.grid(row=1, column=1, padx=40, pady=5, sticky="w")
        self.beta_entry_holt = customtkinter.CTkEntry(master=tabview.tab("Holt"), placeholder_text="Beta - β")
        self.beta_entry_holt.grid(row=1, column=2, padx=0, pady=5, sticky="w")
        self.buttonAnalyzeHolt = customtkinter.CTkButton(master=tabview.tab("Holt"), text="Analyze data", command=None, state="disabled")
        self.buttonAnalyzeHolt.grid(row=1, column=4, padx=20, pady=5, sticky="w")
        self.frameHolt = MyGeneratedGraph(master=tabview.tab("Holt")) #Genera el gráfico en pantalla
        self.frameHolt.grid(row=2, column=1, columnspan=4, padx=20, pady=5, sticky="nsew")

        #Componentes de la pestaña Winters
        self.labelWinters = customtkinter.CTkLabel(master=tabview.tab("Winters"), text="Configure the WINTERS method")
        self.labelWinters.grid(row=0, column=1, padx=30, pady=5, sticky="w")
        self.alfa_entry_winters = customtkinter.CTkEntry(master=tabview.tab("Winters"), placeholder_text="Alfa - α", width=100)
        self.alfa_entry_winters.grid(row=1, column=1, padx=30, pady=5, sticky="nsew")
        self.beta_entry_winters = customtkinter.CTkEntry(master=tabview.tab("Winters"), placeholder_text="Beta - β", width=100)
        self.beta_entry_winters.grid(row=1, column=2, padx=0, pady=5, sticky="w")
        self.gamma_entry_winters = customtkinter.CTkEntry(master=tabview.tab("Winters"), placeholder_text="Gamma - γ", width=100)
        self.gamma_entry_winters.grid(row=1, column=3, padx=0, pady=5, sticky="w")
        self.buttonAnalyzeWinters = customtkinter.CTkButton(master=tabview.tab("Winters"), text="Analyze data", command=None, state="disabled")
        self.buttonAnalyzeWinters.grid(row=1, column=4, padx=20, pady=5, sticky="w")
        self.frameWinters = MyGeneratedGraph(master=tabview.tab("Winters")) #Genera el gráfico en pantalla
        self.frameWinters.grid(row=2, column=1, columnspan=4, padx=20, pady=5, sticky="nsew")

        #Componentes de la pestaña Simple Exp. Smoothing
        self.labelSimple = customtkinter.CTkLabel(master=tabview.tab("Simple Exp. Smoothing"), text="Configure the Simple Exp. Smoothing method")
        self.labelSimple.grid(row=0, column=1, padx=30, pady=5, sticky="w")
        self.alfa_entry_simple = customtkinter.CTkEntry(master=tabview.tab("Simple Exp. Smoothing"), placeholder_text="Alfa - α", width=100)
        self.alfa_entry_simple.grid(row=1, column=1, padx=30, pady=5, sticky="nsew")
        self.buttonAnalyzeSimpleExp = customtkinter.CTkButton(master=tabview.tab("Simple Exp. Smoothing"), text="Analyze data", command=None, state="disabled")
        self.buttonAnalyzeSimpleExp.grid(row=1, column=4, padx=20, pady=5, sticky="w")
        self.frameSimpleExp = MyGeneratedGraph(master=tabview.tab("Simple Exp. Smoothing")) #Genera el gráfico en pantalla
        self.frameSimpleExp.grid(row=2, column=1, columnspan=4, padx=20, pady=5, sticky="nsew")

        image_path_arrow = os.path.join(self.project_dir, "assets/files/reload.png")
        image_arrow = ImageTk.PhotoImage(file=image_path_arrow)
        self.restartButton = customtkinter.CTkButton(master=self, text="Restart Graphs", command=None, fg_color="gray4", border_width=1 ,border_color="light yellow", image=image_arrow, compound="right")
        self.restartButton.grid(row=8, column=1, padx=20, ipady=1, sticky="w")
        self.restartButton.configure(state="disabled")

        image_path_export = os.path.join(self.project_dir, "assets/files/app.png")
        image_export = ImageTk.PhotoImage(file=image_path_export)
        self.exportButton = customtkinter.CTkButton(master=self, text="Export as a .xlsx", command=None, fg_color="gray4", border_width=1,border_color="light yellow", image=image_export, compound="right")
        self.exportButton.grid(row=8, column=1, padx=180, pady=5, sticky="w")
        self.exportButton.configure(state="disabled")
        
        #Frame para mostrar los resultados del análisis
        self.frameResultResume = customtkinter.CTkFrame(self)
        self.frameResultResume.grid(row=9, column=1, padx=20, pady=10, sticky="nsew")
         
        #Last analys data resume
        self.labelLast = customtkinter.CTkLabel(master=self.frameResultResume, text="Last analysis data results:" + " Press Analyze Data button to see your file analysis results."
                                                , font=("Arial", 14, "bold"))
        self.labelLast.grid(row=0, column=0, padx=20, pady=5, sticky="w")

        # Imprimir los resultados en pantalla
        self.label_promedio_tavg = customtkinter.CTkLabel(self.frameResultResume, text=f"Average TAVG: " + "N/A")
        self.label_promedio_tavg.grid(row=1, column=0, padx=20, pady=0, sticky="w")
        self.label_promedio_tavg.configure(state="disabled")

        self.label_temp_max = customtkinter.CTkLabel(self.frameResultResume, text=f"Max. temperature: " + "N/A")
        self.label_temp_max.grid(row=2, column=0, padx=20, pady=0, sticky="w")
        self.label_temp_max.configure(state="disabled")

        self.label_temp_min = customtkinter.CTkLabel(self.frameResultResume, text=f"Min. Temperature: " + "N/A")
        self.label_temp_min.grid(row=3, column=0, padx=20, pady=0, sticky="w")
        self.label_temp_min.configure(state="disabled")

        self.mca = customtkinter.CTkLabel(self.frameResultResume, text=f"Mean absolute error: " + "Analize to see")
        self.mca.grid(row=4, column=0, padx=20, pady=0, sticky="w")
        self.mca.configure(state="disabled")

        
    #Acciones de la UI          
    def open_file_dialog(self):
        self.file_path = filedialog.askopenfilename(filetypes=[('CSV', '*.csv' )])
        if(self.file_path):
            self.file_label.configure(text="Route: ..." + self.file_path[50:], text_color="medium sea green")
            self.labelSelectFile.configure(text="File: *" + self.file_path.split("/")[-1] + "* selected")
            self.buttonAnalyzeHolt.configure(state="normal")
            self.buttonAnalyzeWinters.configure(state="normal")
            self.buttonAnalyzeSimpleExp.configure(state="normal")
            self.show_data()
            
    def saveHistogram(self):
        bufferHistogram = BytesIO()
        fileToHistogram = pd.read_csv(self.file_path)
        fileToHistogram.drop(['STATION', 'NAME'], axis=1, inplace=True)
        fileToHistogram.plot.hist(bins=12, alpha=0.5, figsize=(6, 3.5))
        plt.savefig(bufferHistogram,format='png')
        return bufferHistogram   
    
    def saveComparativMineGraph(self):
        bufferComparativeMin = BytesIO()
        fileToComparativeMin = pd.read_csv(self.file_path)
        fileToComparativeMin.drop(['STATION', 'NAME'], axis=1, inplace=True)
        fileToComparativeMin.plot.scatter(x= 'TAVG', y= 'TMIN', figsize=(6,4))
        plt.xlabel('Avg. Temperature')
        plt.ylabel('Min. Temperature')
        plt.savefig(bufferComparativeMin,format='png')
        return bufferComparativeMin
    
    def saveComparativeMaxGraph(self):
        bufferComparativeMax = BytesIO()
        fileToComparativeMax = pd.read_csv(self.file_path)
        fileToComparativeMax.drop(['STATION', 'NAME'], axis=1, inplace=True)
        fileToComparativeMax.plot.scatter(x= 'TAVG', y= 'TMAX', figsize=(6,4))
        plt.xlabel('Avg. Temperature')
        plt.ylabel('Max. Temperature')
        plt.savefig(bufferComparativeMax,format='png')
        return bufferComparativeMax
    
    def saveBarGraph(self):
        bufferBar = BytesIO()
        fileToBar = pd.read_csv(self.file_path)
        fileToBar.drop(['STATION', 'NAME'], axis=1, inplace=True)
        fileToBar.plot.line(subplots=True)
        plt.savefig(bufferBar,format='png')
        return bufferBar
    
    def show_data(self):
        if self.file_path:
            self.file = pd.read_csv(self.file_path)
            self.treeview.delete(*self.treeview.get_children())
            self.newData = program.Program.showDataResume(self.file)
            #Resume text labels
            self.labelLast.configure(text="Last analysis data results:")
            self.label_promedio_tavg.configure(text=f"Average TAVG: {self.newData[0]}")
            self.label_promedio_tavg.configure(state="normal")
            self.label_temp_max.configure(text=f"Max. temperature: {self.newData[1]}")
            self.label_temp_max.configure(state="normal")
            self.label_temp_min.configure(text=f"Min. Temperature: {self.newData[2]}")
            self.label_temp_min.configure(state="normal")
            for i, row in self.file.iterrows():
                date = row["DATE"]
                tavg = f"{row['TAVG']} C°"
                self.treeview.insert(parent="", index="end", iid=i, text=str(i), values=(date, tavg))  

    def exportFileToExcel(self):
       if self.file_path:
        # Exportar archivo y datos de resumen a Excel
        data_resume = program.Program.showDataResume(self.file)
        histogramImage = self.saveHistogram()
        comparativeMinImage = self.saveComparativMineGraph()
        comparativeMaxImage = self.saveComparativeMaxGraph()
        barImage = self.saveBarGraph()

        program.Program.exportFileToExcel(data_resume, self.mca.cget('text'), self.theCanvas, histogramImage, comparativeMinImage, comparativeMaxImage, barImage)
        messagebox.showinfo("File exported", "File exported successfully, check your project folder for the file.", parent=self)
            
