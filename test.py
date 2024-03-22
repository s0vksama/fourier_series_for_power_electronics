import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_function():
    try:
        expression = entry.get()
        x = np.linspace(-10, 10, 400)
        y = eval(expression)

        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_title("Plot of " + expression)
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    except Exception as e:
        messagebox.showerror("Error", str(e))

window = tk.Tk()
window.title("Function Plotter")

label = tk.Label(window, text="Enter a function (e.g., x**2 + 2*x - 3):")
label.pack()

entry = tk.Entry(window)
entry.pack()

button = tk.Button(window, text="Plot", command=plot_function)
button.pack()

window.mainloop()
