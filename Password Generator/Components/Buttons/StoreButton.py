from ttkbootstrap import Button, StringVar
from Database.Database import AddPassword

# Button that invokes save function of database
# Only invoked when required inputs are valid (password/ StoreName)
class StoreButton(Button):
    def __init__(self, master, password_variable:StringVar, name_variable:StringVar):
        self.pwd = password_variable
        self.name = name_variable
             
        super().__init__(master,
                         text="Save Password",
                         bootstyle='success-outline',
                         command=self.invoke_store)
    # NOTE: TODO: Add a way to change button font
    
    def invoke_store(self):
        generated = self.pwd.get()
        associated = self.name.get()
        
        if generated not in ['test', ''] and associated != '':  # Criteria of invocation
            AddPassword(generated, associated)
            self.master.close()