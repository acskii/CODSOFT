from tkinter import Label

# title... :)
class TitleLabel(Label):
    def __init__(self, master, text='Title'):
        super().__init__(master, 
                         text=text, 
                         anchor="w", 
                         justify="left",
                         font=("Cascadia Code", 16))