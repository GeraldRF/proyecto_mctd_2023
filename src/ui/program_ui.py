import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class ProgramUI:
    
    def __init__(self):
        self.file_path = None
        
        self.root = tk.Tk()
        
        self.mainFrame = ttk.Frame(self.root, padding=10)
        self.mainFrame.grid()        
        
        self.run_btn = ttk.Button(self.mainFrame)
        
        self.selectFileFrame = ttk.Frame(self.mainFrame)
        self.file_label = ttk.Label(self.selectFileFrame)
        
        self.init_components()
        
    def init_components(self):
        ttk.Label(self.mainFrame, text="Hello user, please select a csv file.").grid(column=0, row=0, pady=10)
        
        self.run_btn.grid(column=0, row=2)
        self.run_btn.config(text="Run program")
        
        ttk.Button(self.mainFrame, text="Close", command=self.root.destroy).grid(column=1, row=2)
        
        self.selectFileFrame.grid(column=0, row=1)
        
        ttk.Button(self.selectFileFrame, text="Select", command=self.open_file_dialog).grid(column=0, row=0)
        
        self.file_label.grid(column=1, row=0)
        self.file_label.config(text="You don't selected any file")

    def open_file_dialog(self):
        self.file_path = filedialog.askopenfilename()
        self.file_label.config(text=self.file_path)
        
    def run(self):
        self.root.mainloop()