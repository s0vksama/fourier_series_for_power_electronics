import tkinter
from customtkinter import*
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import symbols, sympify
import sympy as sym
import math
import numpy as np

from sympy import pi

furrbtn = None
fig1 = None

root = CTk()
root.geometry("500X400")

def graph_graphics():
    # Customize the grid color with a custom RGB value
    grid_color = (0.4275, 0.4275, 0.4118)  # RGB values between 0 and 1
    fig.set_facecolor('#242424')  # Set the background color to a light gray
    # Customize the background color of the graph
    ax.set_facecolor('#242424')
    plt.grid(color=grid_color, linestyle='--', linewidth=0.5)
    plt.axhline(y=0, color='white', linestyle='-', linewidth=2)
    plt.axvline(x=0, color='white', linestyle='-', linewidth=2)

    # Customize axis and label colors
    ax.tick_params(axis='both', which='both', colors='white')  # Change axis tick color
    ax.spines['bottom'].set_color('white')  # Change color of the x-axis
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')  # Change color of the y-axis
    ax.spines['right'].set_color('white')
    ax.xaxis.label.set_color('white')  # Change color of the x-axis label
    ax.yaxis.label.set_color('white')  # Change color of the y-axis label

def add_function_button_clicked():
    global row_count

    row_count+=1
    if row_count ==2:
        global deltbtn
        deltbtn = CTkButton(master = root, text = "delete interval", command=delete_function_button_clicked)
        deltbtn.grid(row=1, column=1)
        global b1
        b1 = CTkButton(master = root, text = "Plot", command = plot_graph)
        b1.grid(row=1, column=2)

    e1 = CTkEntry(master = root)
    e1.insert(END, 'f(t)')
    e1.grid(row = row_count, column =0)

    e2 = CTkEntry(master = root)
    e2.grid(row = row_count, column =1)

    l1 =CTkLabel(master = root, text="<  t  <", font=("Helvetica", 25))
    l1.grid(row= row_count, column=2)

    e3 = CTkEntry(master = root)
    e3.grid(row = row_count, column =3)

    entry_boxes.append((e1, e2, l1, e3))

def delete_function_button_clicked():
    global row_count
    global deltbtn
    global fig1
    global canvas1
    global my_frame

    if entry_boxes:
        last_row = entry_boxes.pop()
        for widget in last_row:
            widget.destroy()
        row_count-=1

    if row_count == 1:
        deltbtn.destroy()
        b1.destroy()

    if furrbtn:
        furrbtn.destroy()

    ax.clear()
    graph_graphics()
    canvas.draw()

    if my_frame:
        my_frame.grid_forget()

def plot_graph():
    global all_values
    global my_function
    global max_value
    global min_value
    global furrbtn
    global ax
    global fig

    all_values = []
    max_value = -99999
    min_value = 99999

    for entry1, entry2, _, entry3 in entry_boxes:
        value1 = entry1.get()
        value2 = entry2.get()
        if float(value2) < min_value:
            min_value = float(value2)

        value3 = entry3.get()
        if float(value3) > max_value:
            max_value = float(value3)

        condition_str = "((t>="+value2+")&(t<="+value3+"))"
        expression = sympify(value1)
        condition_str = sympify(condition_str)
        all_values.append((expression, condition_str))

    if len(all_values) != 1:
        my_function = sym.Piecewise(*all_values)
    else:
        my_function = all_values[0][0]

    t = sym.symbols('t')
    # clearing the graph
    ax.clear()


    # to plot the graph we need the x values and y values:
    # getting x values
    x_values = np.linspace(min_value, max_value, 100)

    # getting y values
    y_values = [my_function.subs(t, val) for val in x_values]

    cr = "#E18528"
    line = ax.plot(x_values, y_values, color = cr, linewidth=2.5)

    # shifting function
    shift = max_value - min_value
    ax.plot(x_values-(max_value-min_value), y_values, color = cr, linewidth=2.5)
    ax.plot(x_values+(max_value-min_value), y_values, color = cr, linewidth=2.5)

    # Connect the -shift graph to the start of the original graph
    ax.plot([x_values[0], x_values[-1] - shift], [y_values[-1], y_values[0]], color=cr, linewidth=2.5)

    # Connect the end of the original graph to the +shift graph
    ax.plot([x_values[-1], x_values[0] + shift], [y_values[-1], y_values[0]], color=cr, linewidth=2.5)

    graph_graphics()
    canvas.draw()
    # appearing fourier button
    furrbtn = CTkButton(master = root, text = "Fourier Series", command=fourier_clicked, fg_color=("#de8202", "#de8202") )
    furrbtn.grid(row=1, column=3, pady=10)

def fourier_clicked():
    global fig1
    global canvas1
    global my_frame
    t = sym.symbols('t')
    ser = sym.fourier_series(my_function, (t, min_value, max_value))

    # Convert coefficients to fractions
    ser_frac = ser.truncate(5).rewrite(sym.cos).rewrite(sym.sin)
    ser_frac = sym.nsimplify(ser_frac)
    len_ser_frac = len(str(ser_frac))

    # Convert the Fourier series expression to a LaTeX string
    latex_eqn = sym.latex(ser_frac)

    # creatign a frame to scroll
    my_frame = CTkScrollableFrame(root, orientation="horizontal", width = 700, height = 200,)
    my_frame.grid(row=row_count+1, column=0, columnspan=11, pady = 50, padx=50)

    # Add the LaTeX equation as text on the plot
    fig1, ax1 = plt.subplots(figsize=(25, 1.5))
    ax1.axis('off')
    fig1.set_facecolor('#242424')
    fig1.tight_layout()
    canvas1 = FigureCanvasTkAgg(fig1, master=my_frame)
    canvas1.get_tk_widget().grid(row=row_count+1, column=0, columnspan=4, pady = 50, padx=50)

    equation_text = f'${latex_eqn}$'
    ax1.text(-0.1, 0.2, equation_text, horizontalalignment='left', verticalalignment='top', transform=ax.transAxes, fontsize=17, color='white')

set_appearance_mode("Dark")
#Graph graphics
fig, ax = plt.subplots(figsize=(11,3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, pady = 50, padx=50)
graph_graphics()

# root.grid_columnconfigure(1, minsize=100)
row_count = 1;
entry_boxes = []
addbtn = CTkButton(master = root, text = "add interval", command=add_function_button_clicked)
addbtn.grid(row=1, column=0, pady=10)

root.mainloop()
