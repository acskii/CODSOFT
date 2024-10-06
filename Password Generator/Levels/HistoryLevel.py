from ttkbootstrap import Toplevel 
from Components.Labels.TitleLabel import *
from Components.Frames.ScrollFrame import ScrollingFrame

# Window that compiles all neccessary components to view all previously stored passwords.
class HistoryLevel(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.minsize(300, 200)
        self.title('Password History')
        
        self.grid_columnconfigure(0, weight=1)
        
        self.title = TitleLabel(self, 'Stored Passwords')
        self.title.grid(row=0, column=0, columnspan=2, sticky='we', padx=10)
        
        # TODO: Scrollable frame here
        self.frame = ScrollingFrame(self)
        self.frame.grid(row=1, column=0, sticky='we', padx=10, pady=10)
        
    # Self-destruct :>
    def close(self):
        self.destroy()