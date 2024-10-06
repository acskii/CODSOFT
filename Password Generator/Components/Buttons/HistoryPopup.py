from ttkbootstrap import Button
from Levels.HistoryLevel import HistoryLevel

# Button that opens toplevel window of password history
class HistoryPopupButton(Button):
    def __init__(self, master):
        self.window = None

        super().__init__(master,
                         text="View Stored",
                         bootstyle='success',
                         command=self.popup,
                         )
    # NOTE: TODO: Add a way to change button font
    
    def onclose(self):
        self.window.destroy()
    
    def popup(self):
        if self.window is None or not self.window.winfo_exists():
            self.window = HistoryLevel(self)  # create window if its None or destroyed
            self.window.protocol("WM_DELETE_WINDOW", self.onclose)
        else:
            self.window.focus()  # if window exists focus it