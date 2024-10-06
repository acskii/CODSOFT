# Made by: Andrew Sameh Adel
# Purpose: Internship Program for CODSOFT Python Programming Internship Program
# What is it?
#   A Calculator program that includes multiple intuitive features:
#   1] A UI that looks simple and doesn't have unneccessary clutter
#   2] Supports Keyboard input to control buttons within app
#   3] Provides user a range of mathematical operations such as: multiplication/addition/subtraction/addition/mod
#   4] Other features such as: Clear / Erase previous / Floating point calculations
#   5] Can re-use answer of a previous equation in a new one
#   6] Evaluates a sequence of operations, and obeys order of operations 

# Using Tk for UI
from tkinter import *

# Class for buttons to add custom methods/design
class CalculatorButton(Button):
    def __init__(self, master, text, value=None):
        self.value = text if value == None else value
        super().__init__(master, 
                         text=text, 
                         font=('Cascadia Code', 18),    #Font style and size can be changed here
                         justify='center',
                         command=self.on_button_press,
                         relief='sunken',
                         borderwidth=3,
                        )

    def on_button_press(self):
        # Sends input to App for processing        
        self.master.process_input(self.value)
        self.click_animate()

    def click_animate(self): 
        # Change button colour and revert it to show user that it was clicked/selected
        self.config(bg='#b0b3b8')
        self.after(400, lambda: self.config(bg='#f0f0f0'))

 
# Class for calculator display/screen
class CalculatorDisplay:
    def __init__(self, master):
        # StringVariables to update display labels
        self.entry_var = StringVar(value='')
        self.history_var = StringVar(value='')
    
        # Display UI Components
        self.entry_frame = Frame(master=master, bg='#949191', height=200, highlightthickness=5)
        self.entry_frame.grid(row=0, column=0, rowspan=2, columnspan=4, sticky='we', padx=5, pady=0)

        self.entry_label = Label(master=self.entry_frame, textvariable=self.entry_var, bg='#949191', fg='#ffffff', font=('Cascadia Code', 18), anchor='e')
        self.entry_label.pack(side='bottom', fill='x')

        self.history_label = Label(master=self.entry_frame, textvariable=self.history_var, bg='#949191', fg='#ffffff', font=('Cascadia Code', 10), anchor='e')
        self.history_label.pack(side='bottom', fill='x')

    def update_entry(self, text:str):
        # Edits Entry Label for display
        self.entry_var.set(text)

    def update_history(self, inputs:list, result=False):            # Has option to show answer
        self.history_var.set( ' '.join(inputs) + (f' = {self.entry_var.get()}' if result else ''))

    def clear_history(self):                # clear history only
        self.history_var.set('')

    def clear(self):                        # empty contents of BOTH history and entry variables
        self.update_entry('')
        self.clear_history()

# Main class for calculator, handles inputs and outputs
class Calculator(Tk):
    def __init__(self):
        super().__init__()
        # Setting up window
        self.title("Calculator")
        self.geometry('400x500')
        self.icon = PhotoImage(file='./icon.png')
        self.iconphoto(False, self.icon)
        self.minsize(400, 500)
        self.maxsize(700, 700)
        self.config(bg='#b0acac')

        # Setting up variables
        self.inputs = list()
        self.already_answer = False         # Flag used to clear content if an answer has been evaluated already
        self.error_caught = False           # To catch errors

        # Setting up rows and columns in the grid
        self.columnconfigure((0,1,2,3), weight=1)
        self.rowconfigure((0,1,2,3,4,5,6), weight=1)

        # Creating operation/results display
        self.display = CalculatorDisplay(master=self)

        # Creating 1st row of buttons   (C,%,<,/)
        self.btn_clear = CalculatorButton(master=self, text='C')
        self.btn_clear.grid(row=2, column=0, sticky='nswe', padx=5, pady=5)

        self.btn_remainder = CalculatorButton(master=self, text='%')
        self.btn_remainder.grid(row=2, column=1, sticky='nswe', padx=5, pady=5)

        self.btn_left_delete = CalculatorButton(master=self, text='<', value='del')     # Previous symbol: '\u232B'
        self.btn_left_delete.grid(row=2, column=2, sticky='nswe', padx=5, pady=5)

        self.btn_divide = CalculatorButton(master=self, text='\u00F7', value='/')
        self.btn_divide.grid(row=2, column=3, sticky='nswe', padx=5, pady=5)

        # Creating 2nd row of buttons (7,8,9,*)
        self.btn7 = CalculatorButton(master=self, text='7')
        self.btn7.grid(row=3, column=0, sticky='nswe', padx=5, pady=5)

        self.btn8 = CalculatorButton(master=self, text='8')
        self.btn8.grid(row=3, column=1, sticky='nswe', padx=5, pady=5)

        self.btn9 = CalculatorButton(master=self, text='9')
        self.btn9.grid(row=3, column=2, sticky='nswe', padx=5, pady=5)

        self.btn_multiply = CalculatorButton(master=self, text='*')
        self.btn_multiply.grid(row=3, column=3, sticky='nswe', padx=5, pady=5)

        # Creating 3rd row of buttons (4,5,6,-)
        self.btn4 = CalculatorButton(master=self, text='4')
        self.btn4.grid(row=4, column=0, sticky='nswe', padx=5, pady=5)

        self.btn5 = CalculatorButton(master=self, text='5')
        self.btn5.grid(row=4, column=1, sticky='nswe', padx=5, pady=5)

        self.btn6 = CalculatorButton(master=self, text='6')
        self.btn6.grid(row=4, column=2, sticky='nswe', padx=5, pady=5)

        self.btn_sub = CalculatorButton(master=self, text='-')
        self.btn_sub.grid(row=4, column=3, sticky='nswe', padx=5, pady=5)

        # Creating 4th row of buttons (1,2,3,+)
        self.btn1 = CalculatorButton(master=self, text='1')
        self.btn1.grid(row=5, column=0, sticky='nswe', padx=5, pady=5)

        self.btn2 = CalculatorButton(master=self, text='2')
        self.btn2.grid(row=5, column=1, sticky='nswe', padx=5, pady=5)

        self.btn3 = CalculatorButton(master=self, text='3')
        self.btn3.grid(row=5, column=2, sticky='nswe', padx=5, pady=5)

        self.btn_add = CalculatorButton(master=self, text='+')
        self.btn_add.grid(row=5, column=3, sticky='nswe', padx=5, pady=5)

        # Creating last row of buttons (0, ., =)
        self.btn0 = CalculatorButton(master=self, text='0')
        self.btn0.grid(row=6, column=0, columnspan=2, sticky='nswe', padx=5, pady=5)

        self.btn_point = CalculatorButton(master=self, text='.')
        self.btn_point.grid(row=6, column=2, sticky='nswe', padx=5, pady=5)

        self.btn_solve = CalculatorButton(master=self, text='=')
        self.btn_solve.grid(row=6, column=3, sticky='nswe', padx=5, pady=5)

        #Keyboard listener
        self.bind("<Key>", self.key_press)

    def process_input(self, input:str):
        # Check if an answer has been already given, and refresh display
        if self.already_answer:
            # If the next input after solving was an number
            if input.isdigit():     # then restart calculator
                self.inputs.clear()
                self.display.clear()
            else:                   # else use answer as the first number
                self.inputs = [self.inputs[-1]]
            self.already_answer = False

        elif self.error_caught:         # Make sure calculator is refreshed after error
            self.inputs.clear()
            self.display.clear()
            self.error_caught = False

        if input.isdigit():     # Input is a number/float
            if (len(self.inputs) == 0) or (not self.inputs[-1].isdigit()):    # If the latest input was the first, or an operation
                if (len(self.inputs) > 0) and (self.inputs[-1].find('.') != -1):    # If latest input was a floating point, add on input normally
                    self.inputs[-1] += input
                    self.display.update_entry(self.inputs[-1])
                else:                                                             # Otherwise
                    self.inputs.append(input)                                     # Add input in a new slot
                    self.display.update_entry(input)

            elif (len(self.inputs) > 0) and (self.inputs[-1].isdigit()):      # If latest input was a number -> add digit to the end of this number
                #if len(self.inputs[-1]) < self.max_number_len:
                self.inputs[-1] += input
                self.display.update_entry(self.inputs[-1])
        else:
            if input in ['-', '+', '/', '*', '%']:      # Standard mathematical operations that can be displayed
                if len(self.inputs) > 0:                # Not the first input
                    if (self.inputs[-1].isdigit()) or (self.inputs[-1].find('.')):       # latest input is a digit
                        self.inputs.append(input)
                    else:
                        self.inputs[-1] = input         # Replace operation if latest was one too

                    self.display.update_history(self.inputs)

            elif input == '.':
                # If floating point was inputted -> make sure the previous input was a number NOT the first input
                if (len(self.inputs) > 0) and (self.inputs[-1].isdigit()):
                    self.inputs[-1] += input
                    self.display.update_entry(self.inputs[-1])
                
            else:       # Special operation inputted
                #TODO: Add automatic equal ( eg. 9 - 1 = 8 --> = 7 --> = 6 --> etc.)  AND KEYBOARD INPUT
                if input == '=':    # Get answer
                    if len(self.inputs) >= 3:         # All neccessary components have been inputted
                        if all((self.inputs[-1].isdigit() or self.inputs[-1].find('.'), not self.inputs[-2].isdigit(), self.inputs[-3].isdigit() or self.inputs[-3].find('.'))):
                            try:    # To avoud zero and leading zeros errors
                                # Collect all inputs and join them into an expression
                                exp = ''.join(self.inputs)
                                # use eval to evaluate the answer
                                answer = round(eval(exp), 5)
                                # update display history
                                self.display.update_entry(answer)
                                self.display.update_history(self.inputs, result=True)       # Show full equation in history
                                self.already_answer = True
                                self.inputs.append(str(answer))
                            except Exception as e:
                                print(f'ERROR: [{e}]')
                                self.error_caught = True
                                self.display.update_entry('ERROR')
                                self.display.clear_history()
                
                elif input.lower() == 'c':  # Clear inputs
                    self.display.clear()
                    self.inputs.clear()

                elif input == 'del':  # Erase previous input
                    if len(self.inputs) > 0:                     # Makes sure that there is an input to erase
                        if len(self.inputs[-1]) > 1:                    # If it is a number -> remove last digit inputted
                            self.inputs[-1] = self.inputs[-1][:-1]
                            
                            self.display.update_entry(self.inputs[-1])
                        else:                                           # Only one number/operation -> remove from list
                            self.inputs.pop()
                            self.display.update_history(self.inputs)      
                            self.display.update_entry(self.inputs[-1] if len(self.inputs) > 0 and self.inputs[-1].isdigit() else '')      # Fail-safe in case first digit is erased

    def key_press(self, event):
        # Determine if key pressed was a number or an operation
        # Process input directly without pressing on buttons
        # Is there a better way for this?
        key = event.char

        if (key == '1'):
            self.btn1.click_animate()
        if (key == '2'):
            self.btn2.click_animate()
        if (key == '3'):
            self.btn3.click_animate()
        if (key == '4'):
            self.btn4.click_animate()
        if (key == '5'):
            self.btn5.click_animate()
        if (key == '6'):
            self.btn6.click_animate()
        if (key == '7'):
            self.btn7.click_animate()
        if (key == '8'):
            self.btn8.click_animate()
        if (key == '9'):
            self.btn9.click_animate()
        if (key == '0'):
            self.btn0.click_animate()
        if (key.lower() == 'c'):
            self.btn_clear.click_animate()
        if (key == '%'):
            self.btn_remainder.click_animate()
        if (key == '*'):
            self.btn_multiply.click_animate()
        if (key == '/'):
            self.btn_divide.click_animate()
        if (key == '-'):
            self.btn_sub.click_animate()
        if (key == '.'):
            self.btn_point.click_animate()
        if (key == '+'):
            self.btn_add.click_animate()
        if (key == '=') or (event.keysym == 'Return'):
            self.btn_solve.click_animate()
            self.process_input('=')
        if (key == '\x08'):
            self.btn_left_delete.click_animate()
            self.process_input('del')
        
        if (key != '=') and (event.keysym != 'Return') and (key != '\x08'):
            self.process_input(key)

if __name__ == "__main__":
    # Create and run the calculator window
    c = Calculator()
    # Start app
    c.mainloop()

# Any feedback is appreciated :)