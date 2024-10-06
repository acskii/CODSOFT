from ttkbootstrap import Button
from tkinter import Tk

# Button component that stores one (password, name) pair
# Copies to clipboard on press
class PasswordButton(Button):
    def __init__(self, master, name, password):     
        self.password = password
        self.name = name
   
        super().__init__(master,
                         text=f"[{name}]:: \n{password}",
                         bootstyle='success-outline',
                         command=self.copy,
                         )
        
    def copy(self):
        temp = Tk()
        temp.withdraw()
        temp.clipboard_clear()
        temp.clipboard_append(self.password)
        temp.update()
        temp.destroy()