from tkinter import *
from tkinter import ttk
from decimal import *
import re

root = Tk()
root.title("calculator")
content = ttk.Frame(root)


def buttonPressed(buttonPushed):
    # initialize variables
    displayText = display.get()
    displayNum = Decimal(displayText)
    rememberText = remember.get()

    global displayDelete
    global num1
    global num2
    global operation1
    global operation2

    try:
        buttonPushed = int(buttonPushed)
    except ValueError:
        pass

    # Handler for number buttons
    numberButtons = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '.', '+/-', '<-')
    if buttonPushed in numberButtons:
        if displayText == '0':
            displayDelete = True

        if isinstance(buttonPushed, int):
            if displayDelete:
                displayText = ''
                displayDelete = False
            displayText = displayText + str(buttonPushed)
        if isinstance(buttonPushed, str):
            if displayDelete:
                displayText = '0'
                displayDelete = False

        # Handler for decimal button
        if buttonPushed == '.':
            if '.' not in displayText:
                displayText = displayText + '.'

        # Handler for backspace
        if buttonPushed == '<-':
            if displayText == '0':
                num1 = None
                num2 = None
                operation1 = None
                operation2 = None
                displayText = '0'
                rememberText = ''
            else:
                displayText = displayText[:-1]

        # Handler for negative button
        if buttonPushed == '+/-':
            if displayText[0] == '-':
                displayText = displayText[1:]
            else:
                displayText = '-' + displayText

        # Edge cases
        badDisplaySet = ('', '-', '-0', '00')
        if displayText in badDisplaySet:
            displayText = '0'
        if displayText == '0':
            displayDelete = True

    # Operation handler
    if buttonPushed in ('+', '-', 'x', '/'):
        displayDelete = True

        if num1 is None:
            num1 = displayNum
            operation1 = buttonPushed

            rememberText = numText(str(num1)) + ' ' + operation1 + ' '
            displayText = numText(str(num1))
        elif num2 is None:
            operation2 = buttonPushed
            num2 = displayNum
            num1 = calculate()
            operation1 = operation2
            num2 = None

            rememberText = numText(str(num1)) + ' ' + operation1 + ' '
            displayText = numText(str(num1))
        else:
            num1 = displayNum
            num2 = None
            operation1 = buttonPushed
            operation2 = None

            rememberText = numText(str(num1)) + ' ' + operation1 + ' '

    # Equals handler
    if buttonPushed == '=':
        displayDelete = True
        if num1 is None:
            num1 = displayNum
            rememberText = numText(str(num1)) + ' = '
            displayText = numText(str(num1))
        elif num2 is None:
            if operation1 is not None:
                num2 = displayNum
                rememberText = numText(str(num1)) + ' ' + operation1 + ' ' + numText(str(num2)) + ' = '
                num1 = calculate()
                displayText = numText(str(num1))
        else:
            num1 = displayNum
            rememberText = numText(str(num1)) + ' ' + operation1 + ' ' + numText(str(num2)) + ' = '
            displayText = numText(str(calculate()))

    display.set(displayText)
    remember.set(rememberText)


def numText(numText):
    if float(numText).is_integer():
        return str(int(Decimal(numText)))
    else:
        return str(Decimal(numText))


def calculate():
    global num1
    global num2
    global operation1
    global operation2

    if operation1 == '+':
        return num1 + num2
    if operation1 == '-':
        return num1 - num2
    if operation1 == 'x':
        return num1 * num2
    if operation1 == '/':
        return num1 / num2


display = StringVar()
remember = StringVar()
num1 = None
num2 = None
operation1 = None
operation2 = None
displayDelete = True

# Create number display
displayLabel = ttk.Label(content, textvariable=display, padding=5, font=("TkDefaultFont", 30))
rememberLabel = ttk.Label(content, textvariable=remember, padding=(0, 0, 10, 0), font=("TkDefaultFont", 10))

display.set('0')
remember.set('')

buttonPadding = (0, 10)

# create number and operation buttons
one = ttk.Button(content, text='1', padding=buttonPadding, command=lambda: buttonPressed('1'))
two = ttk.Button(content, text='2', padding=buttonPadding, command=lambda: buttonPressed('2'))
three = ttk.Button(content, text='3', padding=buttonPadding, command=lambda: buttonPressed('3'))
four = ttk.Button(content, text='4', padding=buttonPadding, command=lambda: buttonPressed('4'))
five = ttk.Button(content, text='5', padding=buttonPadding, command=lambda: buttonPressed('5'))
six = ttk.Button(content, text='6', padding=buttonPadding, command=lambda: buttonPressed('6'))
seven = ttk.Button(content, text='7', padding=buttonPadding, command=lambda: buttonPressed('7'))
eight = ttk.Button(content, text='8', padding=buttonPadding, command=lambda: buttonPressed('8'))
nine = ttk.Button(content, text='9', padding=buttonPadding, command=lambda: buttonPressed('9'))
zero = ttk.Button(content, text='0', padding=buttonPadding, command=lambda: buttonPressed('0'))
point = ttk.Button(content, text='.', padding=buttonPadding, command=lambda: buttonPressed('.'))
negative = ttk.Button(content, text='+/-', padding=buttonPadding, command=lambda: buttonPressed('+/-'))
equals = ttk.Button(content, text='=', padding=(77, buttonPadding[1]), command=lambda: buttonPressed('='))
plus = ttk.Button(content, text='+', padding=buttonPadding, command=lambda: buttonPressed('+'))
minus = ttk.Button(content, text='-', padding=buttonPadding, command=lambda: buttonPressed('-'))
times = ttk.Button(content, text='x', padding=buttonPadding, command=lambda: buttonPressed('x'))
divide = ttk.Button(content, text='/', padding=buttonPadding, command=lambda: buttonPressed('/'))
backspace = ttk.Button(content, text='<-', padding=buttonPadding, command=lambda: buttonPressed('<-'))

# Assign widgets locations on grid
content.grid(column=0, row=0)
displayLabel.grid(column=0, row=1, columnspan=4, sticky=(E))
rememberLabel.grid(column=0, row=0, columnspan=4, sticky=(E))

seven.grid(column=0, row=2)
eight.grid(column=1, row=2)
nine.grid(column=2, row=2)
divide.grid(column=3, row=3)
four.grid(column=0, row=3)
five.grid(column=1, row=3)
six.grid(column=2, row=3)
times.grid(column=3, row=4)
one.grid(column=0, row=4)
two.grid(column=1, row=4)
three.grid(column=2, row=4)
minus.grid(column=3, row=5)
negative.grid(column=0, row=5)
zero.grid(column=1, row=5)
point.grid(column=2, row=5)
plus.grid(column=3, row=6)
backspace.grid(column=3, row=2)
equals.grid(column=0, row=6, columnspan=3)

root.mainloop()
