class Program: 
    def __init__(self, window):
        window.run_btn.config(command=self.run_program)
        window.run()
        
    def run_program(self):
        print("Running")