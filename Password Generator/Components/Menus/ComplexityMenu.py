from tkinter import StringVar, Label
from customtkinter import CTkOptionMenu

class ComplexityLabel(Label):
    def __init__(self, master):
        super().__init__(master, 
                         text="Complexity: ", 
                         anchor="w", 
                         justify="left",
                         font=("Cascadia Code", 10))

class ComplexityMenu(CTkOptionMenu):
    def __init__(self, master):
        self.chosen = StringVar(value='Select complexity')
        self.options = ['simple', 'normal', 'impossible', 'PIN']

        super().__init__(master, 
                         variable=self.chosen, 
                         values=self.options,
                         font=('Cascadia Code', 13)
                         )
        self.chosen.set(self.options[1])

    def get_chosen(self):
        return self.chosen.get()
    
    def view_options(self):
        print("Options: ")
        for option in self.options:
            print(f">> {option}")

    