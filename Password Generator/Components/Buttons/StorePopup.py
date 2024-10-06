from ttkbootstrap import Button, StringVar
from Levels.StoreLevel import StoreLevel
from Database.Database import PasswordExists

# Button that opens top level Store on press
# Only opens when password generated doesn't already exists
class StorePopupButton(Button):
    def __init__(self, master, password_variable:StringVar):
        self.var = password_variable

        super().__init__(master,
                         text="Store",
                         bootstyle='success-outline',
                         command=self.popup,
                         )
    # NOTE: TODO: Add a way to change button font
    
    def popup(self):
        if not PasswordExists(self.var.get()) and self.var.get() not in ['test', '']:
            StoreLevel(self.var)
        else:
            print('[POPUP] Attempted to store an already stored password.')