from tkinter import *
from tkinter import ttk
from decimal import *

root = Tk()
root.title("calculator")
content = ttk.Frame(root)


def press_button(button_identity):
    # initialize variables
    display_text = display.get()
    if display_text == 'ERROR':
        display_text = '0'

    display_num = Decimal(display_text)
    remember_text = remember.get()

    global display_delete
    global num1
    global num2
    global operation1
    global operation2

    try:
        button_identity = int(button_identity)
    except ValueError:
        pass

    # Handler for buttons that change the number display
    numberButtons = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '.', '+/-', '<-')
    if button_identity in numberButtons:
        if display_text == '0':
            display_delete = True

        if isinstance(button_identity, int):
            if display_delete:
                display_text = ''
                display_delete = False
            display_text = display_text + str(button_identity)
        if isinstance(button_identity, str):
            if display_delete:
                display_text = '0'
                display_delete = False

        # Handler for decimal button
        if button_identity == '.':
            if '.' not in display_text:
                display_text = display_text + '.'

        # Handler for backspace
        if button_identity == '<-':
            if display_text == '0':
                num1 = None
                num2 = None
                operation1 = None
                operation2 = None
                display_text = '0'
                remember_text = ''
            else:
                display_text = display_text[:-1]

        # Handler for negative button
        if button_identity == '+/-':
            if display_text[0] == '-':
                display_text = display_text[1:]
            else:
                display_text = '-' + display_text

        # Edge cases
        badDisplaySet = ('', '-', '-0', '00')
        if display_text in badDisplaySet:
            display_text = '0'
        if display_text == '0':
            display_delete = True

    # Operation handler
    if button_identity in ('+', '-', 'x', '/'):
        display_delete = True

        if num1 is None:
            num1 = display_num
            operation1 = button_identity

            remember_text = str(num1) + ' ' + operation1 + ' '
            display_text = str(num1)
        elif num2 is None:
            operation2 = button_identity
            num2 = display_num
            num1 = calculate()
            operation1 = operation2
            num2 = None

            remember_text = str(num1) + ' ' + operation1 + ' '
            display_text = str(num1)
        else:
            num1 = display_num
            num2 = None
            operation1 = button_identity
            operation2 = None

            remember_text = str(num1) + ' ' + operation1 + ' '

    # Equals handler
    if button_identity == '=':
        display_delete = True
        if num1 is None:
            remember_text = str(display_num) + ' = '
            display_text = str(display_num)
        elif num2 is None:
            if operation1 is not None:
                num2 = display_num
                remember_text = str(num1) + ' ' + operation1 + ' ' + str(num2) + ' = '
                num1 = calculate()
                display_text = str(num1)
        else:
            num1 = display_num
            remember_text = str(num1) + ' ' + operation1 + ' ' + str(num2) + ' = '
            display_text = str(calculate())

    global is_error
    if is_error:
        num1 = None
        num2 = None
        operation1 = None
        operation2 = None
        remember_text = ''
        display_text = 'ERROR'
        is_error = False

    display.set(display_text)
    remember.set(remember_text)


def calculate():
    global num1
    global num2
    global operation1
    global is_error

    answer = None

    if operation1 == '+':
        answer = num1 + num2
    if operation1 == '-':
        answer = num1 - num2
    if operation1 == 'x':
        answer = num1 * num2
    if operation1 == '/':
        if num2 == 0:
            is_error = True
            return None
        else:
            answer = num1 / num2

    # removes unnecessary zeroes
    answer = answer.quantize(Decimal(1)) if answer == answer.to_integral() else answer.normalize()

    return answer


display = StringVar()
remember = StringVar()
num1 = None
num2 = None
operation1 = None
operation2 = None
display_delete = True
is_error = False

# Create number display
display_label = ttk.Label(content, textvariable=display, padding=5, font=("TkDefaultFont", 30))
remember_label = ttk.Label(content, textvariable=remember, padding=(0, 0, 10, 0), font=("TkDefaultFont", 10))

display.set('0')
remember.set('')

buttonPadding = (0, 10)

# create number and operation buttons
one = ttk.Button(content, text='1', padding=buttonPadding, command=lambda: press_button('1'))
two = ttk.Button(content, text='2', padding=buttonPadding, command=lambda: press_button('2'))
three = ttk.Button(content, text='3', padding=buttonPadding, command=lambda: press_button('3'))
four = ttk.Button(content, text='4', padding=buttonPadding, command=lambda: press_button('4'))
five = ttk.Button(content, text='5', padding=buttonPadding, command=lambda: press_button('5'))
six = ttk.Button(content, text='6', padding=buttonPadding, command=lambda: press_button('6'))
seven = ttk.Button(content, text='7', padding=buttonPadding, command=lambda: press_button('7'))
eight = ttk.Button(content, text='8', padding=buttonPadding, command=lambda: press_button('8'))
nine = ttk.Button(content, text='9', padding=buttonPadding, command=lambda: press_button('9'))
zero = ttk.Button(content, text='0', padding=buttonPadding, command=lambda: press_button('0'))
point = ttk.Button(content, text='.', padding=buttonPadding, command=lambda: press_button('.'))
negative = ttk.Button(content, text='+/-', padding=buttonPadding, command=lambda: press_button('+/-'))
equals = ttk.Button(content, text='=', padding=(77, buttonPadding[1]), command=lambda: press_button('='))
plus = ttk.Button(content, text='+', padding=buttonPadding, command=lambda: press_button('+'))
minus = ttk.Button(content, text='-', padding=buttonPadding, command=lambda: press_button('-'))
times = ttk.Button(content, text='x', padding=buttonPadding, command=lambda: press_button('x'))
divide = ttk.Button(content, text='/', padding=buttonPadding, command=lambda: press_button('/'))
backspace = ttk.Button(content, text='<-', padding=buttonPadding, command=lambda: press_button('<-'))

# Assign widgets locations on grid
content.grid(column=0, row=0)
display_label.grid(column=0, row=1, columnspan=4, sticky=E)
remember_label.grid(column=0, row=0, columnspan=4, sticky=E)

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
