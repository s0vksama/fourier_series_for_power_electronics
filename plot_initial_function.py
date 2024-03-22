import sympy as sym
from sympy import pi
import numpy as np
import matplotlib.pyplot as plt

t = sym.symbols('t')

def periodic_plot(i, a1, a2):
    time_period = a2-a1
    if i <= a1:
        return periodic_plot(i+time_period, a1, a2)
    elif i >=a2:
        return periodic_plot(i-time_period, a1, a2)
    else:
        # write codr for normal interval
        return x.subs(t, i)

x = sym.Piecewise(  (-t-2, ((t>=-2) & (t<=-1 ))),
                    (t,   ((t>=-1) & (t<= 1 ))),
                    (-t+2, ((t>=1 ) & (t<=2  ))))

x_values = np.linspace(-8, 8, 1000)
y_values = [periodic_plot(x,-2, 2) for x in x_values]


plt.plot(x_values, y_values)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Piecewise periodic function')
plt.grid(True)
plt.show()
