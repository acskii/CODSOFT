from tkinter import Label, Frame, Entry, StringVar, Menu, Tk

# Right-click -> Copy Password -> Copied to Clipboard!
class CopyOption(Menu):
    def __init__(self, master, input=''):
        self.input = input

        super().__init__(master,
                         tearoff=0)
        self.add_command(label='Copy Password', command=self.copy)

    def copy(self):
        # NOTE: Best way to copy to clipboard using tkinter and not show that annoying print...
        temp = Tk()
        temp.withdraw()
        temp.clipboard_clear()
        temp.clipboard_append(self.input)
        temp.update()
        temp.destroy()

# label :)
class DisplayLabel(Label):
    def __init__(self, master, text='', fg='#000000'):
        super().__init__(master,
                         text=text,
                         anchor="center", 
                         justify="center",
                         font=("Cascadia Code", 13),
                         fg=fg)

# Password field that displays generated password, and adds copy feature
class PasswordLabel(Entry):
    def __init__(self, master, text='', fg='#000000'):
        self.stored = StringVar(value=text)
        super().__init__(master,
                         textvariable=self.stored,
                         justify="center",
                         fg=fg,
                         font=("Cascadia Code", 13),
                         state='readonly',
                         relief='flat'
                         )
        
        self.bind('<Button-3>', self.popup)

    def popup(self, event):
        self.copyOption = CopyOption(self, self.stored.get())
        try:
            self.copyOption.tk_popup(event.x_root, event.y_root)
        finally:
            self.copyOption.grab_release()

# Class used to employ all above classes in one
# (Can you make private classes??)
class Display(Frame):
    def __init__(self, master, placeholder=''):
        super().__init__(master)

        self.label = DisplayLabel(master=self, text='Password: ')
        self.holder = PasswordLabel(master=self, text=placeholder, fg='#03a1fc')

        self.label.pack(side='left', anchor='center')
        self.holder.pack(side='right', fill='x', expand=True)
        
    def update(self, new_pass):
        self.holder.stored.set(new_pass)