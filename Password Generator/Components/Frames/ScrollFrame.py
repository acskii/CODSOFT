from ttkbootstrap.scrolled import ScrolledFrame
from Components.Buttons.CopyPassButton import PasswordButton
from Database.Database import GetPasswords

# Scrollable frame that views all previously stored passwords
# Generates PasswordButtons for each pair
# Has clear function (I found no use for it till now, but I kept it)
class ScrollingFrame(ScrolledFrame):
    def __init__(self, master):
        super().__init__(master, autohide=False, padding=5)
        self.passwords = GetPasswords()
        
        btns = []
        
        for password in self.passwords:
            pwdbtn = PasswordButton(self, password.name, password.password)
            pwdbtn.pack(side='top', fill='x', expand=True, ipadx=2, pady=5)
            btns.append(pwdbtn)
            
        self.passwords = btns.copy()
        btns.clear()
    
    def clear(self):
        for btn in self.passwords:
            btn.destroy()
            
        self.passwords = []
        
            
    
        
