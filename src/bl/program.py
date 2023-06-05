import pandas as pd
import math

class Program: 
    def __init__(self, window):
        self.window = window
        window.run_btn.config(command=self.run_program)
        window.run()
        
    def run_program(self):
        if(self.window.file_path):
            file = pd.read_csv(self.window.file_path)
            count = 0
            for line in file["TAVG"]:
                if math.isnan(line):
                    count+=1
            print(count)
        else: 
            self.window.file_label.config(foreground="red", text="Please, select a file first!")