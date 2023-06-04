import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class ProgramUI:
    
    def __init__(self):
        self.file_path = None
        
        self.root = tk.Tk()
        
        self.mainFrame = ttk.Frame(self.root, padding=10)
        self.mainFrame.pack()        
        
        self.selectFileFrame = ttk.Frame(self.mainFrame)
        self.file_label = ttk.Label(self.selectFileFrame)
        
        self.run_btn = ttk.Button(self.mainFrame)
        
        self.init_components()
        
    def init_components(self):
        ttk.Label(self.mainFrame, text="Hello user, please select a csv file.").pack(pady=10)
        
        
        self.selectFileFrame.pack(pady=30, padx=20)
        
        ttk.Button(self.selectFileFrame, text="Select", command=self.open_file_dialog, width=30).pack(padx=20)
        self.run_btn.pack()
        self.file_label.config(text="You don't selected any file")
        self.file_label.pack()
        
        self.run_btn.config(text="Run program", width=30)
        
        ttk.Button(self.mainFrame, text="Close", width=30, command=self.root.destroy).pack()
        

    def open_file_dialog(self):
        self.file_path = filedialog.askopenfilename()
        self.file_label.config(text=self.file_path)
        
    def run(self):
        self.root.mainloop()