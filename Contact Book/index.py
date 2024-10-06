# Made by: Andrew Sameh
# A Simple Contact List
# Includes:
#   1] Add/Remove/Edit Contacts
#   2] View all saved contacts
#   3] Filter out viewed contacts using search bar
#   4] Allows for multiple numbers per contact
#   5] A short bio per contact

# Import necessary libraries for image handling and GUI creation
import PIL.Image as Image
from customtkinter import *
from tkinter import Label, Button
from pathlib import Path

from database import *

# Set appearance mode and default color theme for the application
set_appearance_mode('light')  # Sets the theme to light mode
set_default_color_theme('green')  # Sets a default green color theme

# Class to create a custom search bar widget
class SearchBar(CTkFrame):
    def __init__(self, master):
        # Call the parent class (CTkFrame) initializer and set up the frame
        super().__init__(master, height=50, fg_color=master.cget('fg_color'))
        
        # Load icons for dark and light modes
        self.icon_dark = Image.open(Path('assets/search_icon.png'))
        self.icon_light = Image.open(Path('assets/search_icon_light.png'))
        self.search_criteria = StringVar(value='')  # Holds the search input
        
        # Set up icon for the search bar
        self.icon_label = CTkLabel(self, 
                                   image=CTkImage(
                                       light_image=self.icon_light,
                                       dark_image=self.icon_dark,
                                       size=(20,20)
                                    ), 
                                   anchor='center',
                                   text='')
        self.icon_label.pack(side='left', anchor='e', expand=True)
        
        # Create the text input field for search criteria
        self.text_input = CTkEntry(self, textvariable=self.search_criteria)
        self.text_input.pack(side='right', anchor='e', expand=True)
        # Bind the KeyRelease event to the search method
        self.text_input.bind('<FocusIn>', lambda x: self.text_input.bind('<KeyRelease>', self.search))

    def search(self, key):
        # Checks if the key is alphanumeric, 'Return', or 'Backspace'
        # Triggers a search in the database
        if (key.char.isalnum()) or (key.keysym == 'Return') or (key.keysym == 'BackSpace'):
            filtered_contacts = search_for(self.search_criteria.get())  # Fetch matching contacts
            self.master.master.master.list.populate(filtered_contacts)  # Update contact list

# Class to create an input field with a label
class InfoInput(CTkFrame):
    def __init__(self, master, label, column, value='', width=200):
        super().__init__(master, fg_color=master.cget('fg_color'))
        self.input_var = StringVar(value=value if value != None else '')  # Input field variable
        self.recorded_value = self.input_var.get()  # Store initial value
        self.name = column  # Column name for database use

        # Create a label for the input field
        self.label = Label(self, 
                           text=label+': ', 
                           bg='gray92' if get_appearance_mode() == 'Light' else 'gray14', 
                           fg='black' if get_appearance_mode() == 'Light' else 'white',
                           anchor='w',
                           font=('Adobe Gothic Std B', 16),
                           )
        self.label.pack(side='left', anchor='w', expand=True, padx=10)
        
        # Create the entry widget for the input field
        self.entry = CTkEntry(self, textvariable=self.input_var, width=width)
        self.entry.pack(expand=True, padx=10, anchor='w', fill='x')

    def get_input(self):
        # Return the current value of the input field
        return self.input_var.get()
    
    def has_changed(self):
        # Check if the value of the input field has been modified
        return self.recorded_value != self.input_var.get()

# Class to create a window for adding new contacts
class AddWindow(CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        # Setting up window properties
        self.geometry('300x250')
        self.title('Add new contact')
        self.resizable(0,0)

        # Set up grid configuration for the window
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1,2), weight=1)

        # Create input fields for contact details
        self.first_name = InfoInput(self, 'First Name', 'first_name')
        self.first_name.grid(row=0, column=0, sticky='we')

        self.number = InfoInput(self, 'Number', 'numbers')
        self.number.grid(row=1, column=0, sticky='we')

        # Create button to confirm adding a contact
        self.confirm_btn = CTkButton(self, 
                                     text='Add Contact',
                                     font=('Adobe Gothic Std B', 18),
                                     command=self.commit_change)
        self.confirm_btn.grid(row=2, column=0, sticky='we', padx=20)

    def get_input(self):
        # Return the inputs for first name and number
        return (self.first_name.get_input(), self.number.get_input())
    
    def commit_change(self):
        # Add the contact to the database and update the contact list
        add_contact(*self.get_input())
        self.master.master.master.list.populate()
        self.destroy()

# Class to create a window for editing contacts
class EditWindow(CTkToplevel):
    def __init__(self, master, contact_id):
        super().__init__(master)
        # Setting up window properties
        self.geometry('300x380')
        self.title('Contact Details')
        self.resizable(0,0)

        # Fetch contact and numbers from the database
        self.contact, self.numbers = get_contact_from_id(contact_id)

        # Set up grid configuration
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1)

        # Create input fields for each contact attribute (e.g., name, email, etc.)
        self.comment = InfoInput(self, 'Comment', 'comment', self.contact.comment)
        self.comment.grid(row=0, column=0, columnspan=2, sticky='we')

        self.first_name = InfoInput(self, 'First Name', 'first_name', self.contact.first_name)
        self.first_name.grid(row=1, column=0, columnspan=2, sticky='we')

        self.middle_name = InfoInput(self, 'Middle Name', 'middle_name', self.contact.middle_name)
        self.middle_name.grid(row=2, column=0, columnspan=2, sticky='we')

        self.last_name = InfoInput(self, 'Last Name', 'last_name', self.contact.last_name)
        self.last_name.grid(row=3, column=0, columnspan=2, sticky='we')

        self.email = InfoInput(self, 'E-mail', 'email', self.contact.email)
        self.email.grid(row=4, column=0, columnspan=2, sticky='we')

        self.address = InfoInput(self, 'Address', 'address', self.contact.address)
        self.address.grid(row=5, column=0, columnspan=2, sticky='we')

        # Only allow editing of one number for simplicity
        self.number = InfoInput(self, 'Number', 'numbers', ', '.join([n.number for n in self.numbers]))
        self.number.grid(row=6, column=0, columnspan=2, sticky='we')

        # Buttons for saving changes or removing the contact
        self.edit_btn = CTkButton(self, 
                                     text='Save Changes',
                                     font=('Adobe Gothic Std B', 18),
                                     command=self.commit_change)
        self.edit_btn.grid(row=7, column=0, columnspan=1, pady=20)

        self.remove_btn = CTkButton(self, 
                                     text='Remove Contact',
                                     font=('Adobe Gothic Std B', 18),
                                     command=self.remove_contact)
        self.remove_btn.grid(row=7, column=1, columnspan=1, pady=20)

    def get_changed_inputs(self):
        # Gather all input fields and check for changes
        inputs = [self.first_name, self.middle_name, self.last_name, self.email, self.address, self.number, self.comment]
        changed = [entry for entry in inputs if entry.has_changed()]  # Return fields that have been modified
        return changed

    def commit_change(self):
        # Save changed inputs to the database
        inputs_changed = self.get_changed_inputs()

        for inpt in inputs_changed:
            column, new_value = inpt.name, inpt.get_input().strip()  # Column name and new value
            if column == 'numbers':  # Special handling for numbers
                new_value = new_value.split(',')
            update_contact_value(self.contact.id, column, new_value)  # Update the database
            self.master.list.populate()
        
        self.destroy()

    def remove_contact(self):
        # Remove the contact from the database and update the contact list
        delete_contact(self.contact.id)
        self.master.list.populate()
        self.destroy()

# Class to define the buttons in the top ribbon (e.g., Add)
class RibbonButton(CTkButton):
    def __init__(self, master, window:str):
        super().__init__(master, 
                         font=('Adobe Gothic Std B', 14),
                         anchor=CENTER,
                         text=f'{window} Contact',
                         width=100,
                         command=self.open_window)
        self.window = window  # Store the window type (e.g., Add or Edit)
        self.window_frame = None  # Store the window instance

    def open_window(self):
        if self.window_frame is None or not self.window_frame.winfo_exists():
            if self.window == 'Add':
                self.window_frame = AddWindow(self.master)
        else:
            self.window_frame.focus()

class TopRibbon(CTkFrame):
    def __init__(self, master):
        super().__init__(master,
                         height=50,
                         fg_color=master.cget('fg_color'),
                        )

        # Add new contacts button
        self.add_button = RibbonButton(master=self, window='Add')
        self.add_button.pack(side='left', expand=True, anchor='w')

        # Search bar
        self.search_bar = SearchBar(master=self)
        self.search_bar.pack(side='left', expand=True, anchor='e', padx=5)

class Contact(CTkFrame):
    def __init__(self, master, contact):
        super().__init__(master)
        self.contact = contact
        self.fg_color = 'black' if get_appearance_mode() == 'Light' else 'white'
        self.bg_color = 'gray92' if get_appearance_mode() == 'Light' else 'gray14'
        self.contact_name = self.contact.full_name
        self.window_frame = None

        # All information regearding a contact
        self.name_btn = Button(self, 
                                text=self.contact_name, 
                                anchor='w',
                                font=('Adobe Gothic Std B', 16),
                                bg=self.bg_color,
                                fg=self.fg_color,
                                command=self.open_menu
                                )
        self.name_btn.pack(side='top', fill='x')
        self.num_list = Label(self, 
                                text=", ".join([n.number for n in self.contact.numbers]), 
                                anchor='w',
                                font=('Adobe Gothic Std B', 12),
                                fg='gray60' if get_appearance_mode() == 'Light' else 'gray50',
                                bg=self.bg_color)
        self.num_list.pack(side='bottom', fill='x')

    def open_menu(self):
        # Open window for contact details
        if self.window_frame is None or not self.window_frame.winfo_exists():
            self.window_frame = EditWindow(self.master.master, self.contact.id)
        else:
            self.window_frame.focus()

# Class to display the contact list within a scrollable frame
class ContactList(CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.rendered_blocks = list()

        self.grid_columnconfigure(0, weight=1)
        self.populate()

    def populate(self, ids:list=[]):
        # Check if a contact list is provided (search feature) otherwise get from database
        if len(ids) > 0:
            recorded_contacts = ids
        else:    
            recorded_contacts = gather_all_contacts()

        # Clear existing buttons
        for contact in self.rendered_blocks:
            contact.destroy()
        self.rendered_blocks.clear()
        
        # Generate new contact buttons
        for i, contact in enumerate(recorded_contacts):
            contact = Contact(self, contact)
            contact.grid(row=i, column=0, sticky='we', pady=7)
            self.rendered_blocks.append(contact)

# Main window class
class ContactBook(CTk):
    def __init__(self):
        super().__init__()
        # Setting up properties
        self.geometry('600x500')
        self.title('Contacts')
        self.resizable(0,0)

        # Loading window UI components
        self.top_color = CTkFrame(self, fg_color=['#cfcfcf', '#4d4c4c'], height=60)
        self.top_color.place(relx=0, rely=0, relwidth=1)

        self.ribbon = TopRibbon(master=self.top_color)
        self.ribbon.pack(side='top', padx=5, pady=5)

        self.list = ContactList(self)
        self.list.place(relx=0.05, rely=0.125, relwidth=0.9, relheight=0.8)
    
if __name__ == "__main__":
    # Starting up main window
    app = ContactBook()
    app.mainloop()