# Made by Andrew Sameh
# Password Generator Interface
# Features:
#   1] Generate passwords with varying complexity / PINs
#   2] Uses a database to store all previously generated passwords
#   3] Allow copying of any generated password/PIN for immediate use
#   4] Clean, simple UI
#   5] All dependencies are encapsulated within this folder, so no need to download anything else
#   6] To run program: 
#           - open cmd
#           - change directory to folder e.g. 'cd Password Generator'
#           - run: 'python passgen.py'

# Dependencies
from tkinter import Tk
from Components.Menus.ComplexityMenu import *
from Components.Entrys.LengthEntry import *
from Components.Labels.DisplayLabel import *
from Components.Buttons.GenerateButton import *
from Components.Buttons.StorePopup import *
from Components.Buttons.HistoryPopup import *
from Components.Labels.TitleLabel import *

# Main window setup
root = Tk()
root.title("Generate Password")
root.minsize(300, 220)

root.grid_columnconfigure((0,1), weight=1)

# Loading components
titleLabel = TitleLabel(root, 'Generate Password')
titleLabel.grid(row=0, column=0, sticky='we', padx=10)

viewStoredButton = HistoryPopupButton(root)
viewStoredButton.grid(row=0, column=1, sticky='we', padx=10)

passwordDifficultyLabel = ComplexityLabel(root)
passwordDifficultyLabel.grid(row=1, column=0, sticky='we', padx=10, pady=10)

passwordDifficultyOptions = ComplexityMenu(root)
passwordDifficultyOptions.grid(row=1, column=1, sticky='we', padx=10)

passwordLengthLabel = LengthLabel(root)
passwordLengthLabel.grid(row=2, column=0, sticky='we', padx=10)

lengthEntry = PasswordLengthEntry(root)
lengthEntry.grid(row=2, column=1, sticky='we', padx=10)

passwordDisplay = Display(root, "test")
passwordDisplay.grid(row=3, column=0, columnspan=2, sticky='we', padx=10, pady=15)

generateButton = GenerateButton(root)
generateButton.grid(row=4, column=1, sticky='we', padx=10)

storeButton = StorePopupButton(root, passwordDisplay.holder.stored)
storeButton.grid(row=4, column=0, sticky='we', padx=10)

# callback function for generate button
def on_generate():
    length = lengthEntry.get_input()
    strength = passwordDifficultyOptions.get_chosen()
    
    generateButton.generator.edit_params(length, strength)
    passwordDisplay.update(generateButton.generator.generate())
    
    if strength == "PIN":
        lengthEntry.update(length if 4 <= length <= 8 else 4)
    else:
        lengthEntry.update(length if 8 <= length <= 100 else 8)

generateButton.configure(command=on_generate)

# Loading of main window
root.mainloop()