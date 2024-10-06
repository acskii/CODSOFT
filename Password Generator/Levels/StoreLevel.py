# Dependencies
from ttkbootstrap import Toplevel, StringVar
from Components.Buttons.StoreButton import StoreButton
from Components.Entrys.NameEntry import NameEntry, NameLabel
from Components.Labels.TitleLabel import TitleLabel

# Window that allows interaction with database
# It is simply a compilation of other componenets that allow for storing of passwords into database
class StoreLevel(Toplevel):
    def __init__(self, password_variable:StringVar):
        super().__init__()
        self.minsize(300, 165)
        self.title('Create New Store')
        
        self.grid_columnconfigure((0,1), weight=1)
        
        self.title = TitleLabel(self, 'Create New Store')
        self.title.grid(row=0, column=0, columnspan=2, sticky='we', padx=10)
        
        self.label = NameLabel(self)
        self.label.grid(row=1, column=0, sticky='we', padx=10)
             
        self.input = NameEntry(self)
        self.input.grid(row=1, column=1, sticky='we', padx=10)
        
        self.btn = StoreButton(self, password_variable, self.input.input)
        self.btn.grid(row=2, column=0, columnspan=2, sticky='we', padx=10, pady=10)
        
    # Self-destruct :>
    def close(self):
        self.destroy()

