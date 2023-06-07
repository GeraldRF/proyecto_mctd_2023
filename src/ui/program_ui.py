import customtkinter
from tkinter import filedialog
from tkinter import ttk 
import pandas as pd

class Holt(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.activator = customtkinter.CTkButton(self, text="HOLT")
        self.activator.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
class Winters(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.activator = customtkinter.CTkButton(self, text="Winters")
        self.activator.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
class SimpleExpSmoothig(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.activator = customtkinter.CTkButton(self, text="Simple Exp. Smoothing")
        self.activator.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
class ProgramUI(customtkinter.CTk):    
    def __init__(self):
        super().__init__()
        
        self.title("Proyecto - Métodos Cuantitativos 2023")
        self.geometry("1200x600")

        customtkinter.set_appearance_mode("dark")

        left_pane = customtkinter.CTkFrame(self, width=400)
        left_pane.pack(side="left", fill="y", expand=True, padx=0)
        
        right_pane = customtkinter.CTkFrame(self, width=600)
        right_pane.pack(side="right", fill="both", expand=True)

        self.file = None

        label = customtkinter.CTkLabel(left_pane, text="Selecciona un archivo para habilitar las acciones.", fg_color="transparent")
        label.pack(padx=20, pady=5)
        label.pack(padx=20, pady=5)

        self.file_label = customtkinter.CTkLabel(left_pane, text="No se ha seleccionado ningún archivo.", fg_color="transparent")
        self.file_label.pack(padx=20, pady=5)

        button = customtkinter.CTkButton(left_pane, text="Seleccionar .csv", command=self.open_file_dialog)
        button.pack(padx=20, pady=15)
        
        #Tabla de datos
        data_pane = customtkinter.CTkFrame(left_pane)
        data_pane.pack(fill='x', expand=True)
        
        self.treeview = ttk.Treeview(data_pane)
        self.treeview.pack(side="left", padx=20, pady=10, fill="x", expand=True)
        self.treeview["columns"] = ("Fecha", "TAVG")  # Agrega las columnas necesarias
        self.treeview.heading("#0", text="C. Datos")
        self.treeview.column("#0", width=80, anchor="center", stretch=False, minwidth=80)
        for col in self.treeview["columns"]:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=80, anchor="center")
        #Scroll de la tabla
        scroll_y = customtkinter.CTkScrollbar(data_pane, command=self.treeview.yview)
        scroll_y.pack(side="right")
        self.treeview.configure(yscrollcommand=scroll_y.set)    
        
        methodsCotainer = customtkinter.CTkFrame(left_pane)
        methodsCotainer.pack()
        
        self.Holt = Holt(methodsCotainer)
        self.Holt.grid(row=1, column=1, padx=20, pady=(10, 0))
        
        self.Winters = Winters(methodsCotainer)
        self.Winters.grid(row=1, column=2, padx=20, pady=(10, 0))
        
        self.SimpleExpSmoothing = SimpleExpSmoothig(methodsCotainer)
        self.SimpleExpSmoothing.grid(row=1, column=3, padx=20, pady=(10, 0))
        

    #Acciones de la UI        
    def button_callback(self):
         print("button pressed")    
    def open_file_dialog(self):
        self.file_path = filedialog.askopenfilename(filetypes=[('CSV', '*.csv' )])
        if(self.file_path):
            self.file_label.configure(text=self.file_path)
            self.show_data()

    def show_data(self):
        if self.file_path:
            self.file = pd.read_csv(self.file_path)
            # Borra las filas existentes en la tabla
            self.treeview.delete(*self.treeview.get_children())
            # Inserta los datos
            for i, row in self.file.iterrows():
                date = row["DATE"]
                tavg = f"{row['TAVG']} C°"
                self.treeview.insert(parent="", index="end", iid=i, text=str(i), values=(date, tavg))  
        
        