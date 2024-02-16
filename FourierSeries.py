import tkinter as tk
import sympy as sym
from sympy import symbols, sympify
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import numpy as np
import re

from sympy import pi
x_labelsPi = ['-T', '-3T/4', '-T/2', '-T/4', '0', 'T/4', 'T/2', '3T/4']

Answer = None
def graph_graphics():
    # Customize the grid color with a custom RGB value
    grid_color = (0.4275, 0.4275, 0.4118)  # RGB values between 0 and 1
    fig.set_facecolor('#2D2C39')  # Set the background color to a light gray
    # Customize the background color of the graph
    ax.set_facecolor('#2D2C39')
    plt.grid(color=grid_color, linestyle='--', linewidth=0.5)
    plt.axhline(y=0, color='white', linestyle='-', linewidth=2)
    plt.axvline(x=2 * pi, color=grid_color, linestyle='--', linewidth=1)
    plt.axvline(x=-2 * pi, color=grid_color, linestyle='--', linewidth=1)
    plt.axvline(x=0, color='white', linestyle='-', linewidth=2)
    plt.xticks(np.arange(-2 * pi, 2 * pi, pi / 2), labels=x_labelsPi)
    # Customize axis and label colors
    ax.tick_params(axis='both', which='both', colors='white')  # Change axis tick color
    ax.spines['bottom'].set_color('white')  # Change color of the x-axis
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')  # Change color of the y-axis
    ax.spines['right'].set_color('white')
    ax.xaxis.label.set_color('white')  # Change color of the x-axis label
    ax.yaxis.label.set_color('white')  # Change color of the y-axis label

def add_entry_boxes():
    global row_count
    global Answer
    if Answer:
        Answer.destroy()

    entry1 = tk.Entry(root)
    entry2 = tk.Entry(root)
    entry3 = tk.Entry(root)
    extra_button = ttk.Button(root, text="Plot", command=lambda: on_extra_button_click(entry1.get(), entry2.get(), entry3.get()))

    entry1.grid(row=row_count, column=2, padx=5, pady=5)
    entry2.grid(row=row_count, column=3, padx=5, pady=5, sticky='w')
    entry3.grid(row=row_count, column=3, padx=140, pady=5, sticky='w')
    extra_button.grid(row=row_count, column=3, padx=270, pady=5, sticky='w')

    entry_boxes.append((entry1, entry2, entry3, extra_button))

    # Move the "Remove Entry Box" button to the end of the row
    remove_button.grid(row=row_count, column=4, padx=300, pady=5, sticky='w')

    # Increment row_count for the next set of entry boxes
    row_count += 1

    # Move both "Add Entry Boxes" and "Remove Entry Box" buttons to the next row
    add_button.grid(row=row_count, column=2, padx=5, pady=10)
    remove_button.grid(row=row_count, column=3, padx=5, pady=10, sticky='w')

    # Create a new "Get Entry Values" button each time entry boxes are added
    get_values_button.grid(row=row_count, column=3, padx=150, pady=10, sticky='w')

def get_entry_values():
    # Extract the values from all entry boxes
    global Answer
    all_values = []
    T = symbols("T")
    for entry1, entry2, entry3, _ in entry_boxes:
        value1 = entry1.get()
        value2 = entry2.get()
        value3 = entry3.get()

        try:
            expr = sympify(value2)
            st = str(expr.subs(T, 2*pi))
            expr = sympify(value3)
            en = str(expr.subs(T, 2*pi))

        except Exception as e:
            # print(f"Error: {e}")
            pass

        condition_str = "((t>="+st+")&(t<="+en+"))"

        t = symbols('t')
        expression = sympify(value1)
        condition_str = sympify(condition_str)
        all_values.append((expression, condition_str))

    if len(all_values) != 1:
        my_function = sym.Piecewise(*all_values)
    else:
        my_function = all_values[0][0]

    ser = sym.fourier_series(my_function, (t, 0, 2*pi))
    z = ser.truncate(5)
    # print(z)
    larger_font = ("Helvetica", 16)

    if Answer:
        Answer.destroy()

    Answer = tk.Label(root, text=str(z), font=larger_font)
    Answer.grid(row=row_count+1, column=0, columnspan=4, padx=5, pady=10)
    Answer.configure(bg='#2D2C39', fg='white')

# ploting graph and data manupulation function
def on_extra_button_click(expression_str, a, b):
    T = symbols("T")
    try:
        expr = sympify(a)
        st = float(expr.subs(T, 2*pi))
        expr = sympify(b)
        en = float(expr.subs(T, 2*pi))

    except Exception as e:
        # print(f"Error: {e}")
        pass

    try:
        x = symbols('t')
        expression = sympify(expression_str)
        # Generate x values
        x_values = np.linspace(st, en, 500)
        # Evaluate the expression for each x value
        y_values = [expression.subs(x, val) for val in x_values]

        # Plot the expression
        line = ax.plot(x_values, y_values, label=str(expression))
        cr = line[0].get_color()
        # sifted function
        ax.plot(x_values-2*pi, y_values, label=str(expression), color = cr)
        # Display the updated plot
        canvas.draw()
    except Exception as e:
        # print("Error:", e)
        pass

def remove_entry_boxes():
    global row_count  # Declare row_count as global
    if entry_boxes:
        last_row = entry_boxes.pop()
        for widget in last_row:
            widget.destroy()

        Answer.destroy()
        # Move both "Add Entry Boxes" and "Remove Entry Box" buttons to the previous row
        row_count -= 1
        add_button.grid(row=row_count, column=2, padx=5, pady=10)
        remove_button.grid(row=row_count, column=3, padx=5, pady=10)

        # Create a new "Get Entry Values" button each time entry boxes are added
        get_values_button.grid(row=row_count, column=3, padx=150, pady=10)

    # clear the previous graph
    ax.cla()
    plt.draw()
    graph_graphics()

root = tk.Tk()
root.title("Fourier Transform")
root.configure(bg='#2D2C39')

style = ttk.Style()
# style.theme_use('clam')
style.configure("TButton", foreground="black", background="white")  # Configure TButton widget


#Graph graphics
fig, ax =plt.subplots(figsize=(11,3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=4)
graph_graphics()

# The buttons
entry_boxes = []
row_count = 1

add_button = ttk.Button(root, text="Add Function", command=add_entry_boxes)
add_button.grid(row=row_count, column=2, padx=5, pady=10)

remove_button = ttk.Button(root, text="Remove Function", command=remove_entry_boxes)
get_values_button = ttk.Button(root, text="Fourier Transform", command=get_entry_values)

root.mainloop()
