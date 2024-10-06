from ttkbootstrap import Entry
from ttkbootstrap.validation import add_text_validation
from tkinter import StringVar, Label

class NameLabel(Label):
    def __init__(self, master):
        super().__init__(master, 
                         text="Associated: ", 
                         anchor="w", 
                         justify="left",
                         font=("Cascadia Code", 13))

class NameEntry(Entry):
    DEFAULT = 'Password'
    def __init__(self, master):
        self.input = StringVar(value='')

        super().__init__(master,
                         textvariable=self.input,
                         font=('Cascadia Code', 13),
                         bootstyle='info'
                         )

        # Validates that input to name field is only text (a-zA-Z)
        add_text_validation(self, when='key')

    def check_auth(self):
        return self.input.get().isalpha() 
    
    # If stored input is unaccepted or out of bounds, it is adjusted to an accepted value
    def get_input(self):
        if self.check_auth():
            res = self.input.get() 
            return res if res != '' else self.DEFAULT
        else:
            return self.DEFAULT
    
    # Second half of adjustion feature, updates field value
    def update(self, new_value):
        self.input.set(new_value)
        self.validate()