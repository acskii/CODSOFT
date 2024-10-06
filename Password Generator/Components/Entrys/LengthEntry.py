from ttkbootstrap import Entry
from ttkbootstrap.validation import add_numeric_validation
from tkinter import StringVar, Label

class LengthLabel(Label):
    def __init__(self, master):
        super().__init__(master, 
                         text="Length: ", 
                         anchor="w", 
                         justify="left",
                         font=("Cascadia Code", 13))

class PasswordLengthEntry(Entry):
    DEFAULT = 8
    def __init__(self, master):
        self.input = StringVar(value='')

        super().__init__(master,
                         textvariable=self.input,
                         font=('Cascadia Code', 13),
                         bootstyle='info'
                         )
        
        # Validates that input to length field is only numeric (0-9)
        add_numeric_validation(self, when='focus')
    
    def check_auth(self):
        return self.input.get().isdigit()
    
    # If stored input is unaccepted or out of bounds, it is adjusted to an accepted value
    def get_input(self):
        if self.check_auth():
            try:
                res = int(self.input.get()) 
                return res if 4 <= res <= 100 else self.DEFAULT
            except ValueError:
                print("Authenticity check method isn't working bud")
                return 0
        else:
            return self.DEFAULT    # Default value
    
    # Second half of adjustion feature, updates field value
    def update(self, new_value):
        self.input.set(new_value)
        self.validate()