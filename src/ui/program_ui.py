import customtkinter
from tkinter import filedialog
from tkinter import ttk 
import pandas as pd


class MySecondFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.button = customtkinter.CTkButton(self, text="Realizar Proyección HOLT")
        self.button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        


class ProgramUI(customtkinter.CTk):    
    def __init__(self):
        super().__init__()

        self.file = None

        self.title("Proyecto - Métodos Cuantitativos 2023")
        self.geometry("800x600")
        self.grid_columnconfigure(0, weight=1)

        customtkinter.set_appearance_mode("dark")

        label = customtkinter.CTkLabel(self, text="Selecciona un archivo para habilitar las acciones.", fg_color="transparent")
        label.grid(row=0, column=0, padx=20, pady=5, sticky="ew" )

        self.file_label = customtkinter.CTkLabel(self, text="No se ha seleccionado ningún archivo.", fg_color="transparent")
        self.file_label.grid(row=1, column=0, padx=20, pady=5, sticky="ew" )

        button = customtkinter.CTkButton(self, text="Seleccionar .csv", command=self.open_file_dialog)
        button.grid(row=2, column=0, padx=20, pady=15, sticky="ew")
        
        #Tabla de datos
        self.treeview = ttk.Treeview(self)
        self.treeview.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        self.treeview["columns"] = ("Fecha", "TAVG")  # Agrega las columnas necesarias
        self.treeview.heading("#0", text="C. Datos")
        self.treeview.column("#0", width=80, anchor="center", stretch=False, minwidth=80)
        for col in self.treeview["columns"]:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=80, anchor="center")
        #Scroll de la tabla
        scroll_y = customtkinter.CTkScrollbar(self, command=self.treeview.yview)
        scroll_y.grid(row=3, column=1, sticky="ns")
        self.treeview.configure(yscrollcommand=scroll_y.set)    


        self.frame = MySecondFrame(self)
        self.frame.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="nsw")

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
        
        