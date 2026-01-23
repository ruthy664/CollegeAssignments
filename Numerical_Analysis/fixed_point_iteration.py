import math
import tkinter as tk
from tkinter import ttk
e = math.e
pi = math.pi

def G(x,g):
    if g == '14a':
        return 2 + math.sin(x)
    elif g == '14b':
        return (2*x+5)**(1/3)
    elif g == '2a':
        return (3+x-2*x**2)**(1/4)
    elif g == '2b':
        return ((x+3-x**4)/2)**(1/2)
    elif g == '2c':
        return ((x+3)/(x**2+2))**(1/2)
    elif g == '2d':
        return (3*x**4+2*x**2+3)/(4*x**3+4*x-1)

def FixedPointIteration(g,p0,TOL=10**(-5),N=10):
    root = tk.Tk()
    root.title(f"Table for {g}")
    columns = ("Iterations","p")
    table = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        table.heading(col, text=col)
    table.insert("", "end", values=(0,p0))
    i = 1
    pm = 0
    while i<=N and pm<TOL:
        p = G(p0,g)
        table.insert("", "end", values=(i,p))
        i = i+1
        p0=p
    pm = abs(p-p0)
    table.pack(expand=True, fill="both")
    root.mainloop()
    
FixedPointIteration('14a',2.5)
FixedPointIteration('14aa',2.5)
#FixedPointIteration('14b',2.15)
#FixedPointIteration('2a',1)
#FixedPointIteration('2b',1)
#FixedPointIteration('2c',1)
#FixedPointIteration('2d',1)