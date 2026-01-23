# Bisection Method 

import math
import tkinter as tk
from tkinter import ttk
e = math.e
pi = math.pi

def F(x,f):
    if f == 'a':
        return 3*x - e**x
    elif f =='b':
        return 2*x + 3*math.cos(x) - e**x
    elif f == 'c':
        return x**2 + 4*x + 4 - math.log(x)
    elif f == 'd':
        return x + 1 - 2*math.sin(pi*x)

def Bisection (a,b,f,N=17):
    root = tk.Tk()
    root.title("Tables")
    columns = ("Iterations","a","b","p","f(p)")
    table = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        table.heading(col, text=col)
    
    i = 1
    FA = F(a,f)
    
    while i<N:
        p = (a+b)/2
        FP = F(p,f)
        table.insert("", "end", values=(i,a,b,p,FP))
        i = i+1
        if FA*FP>0:
            a = p
        else:
            b = p
    table.pack(expand=True, fill="both")
    root.mainloop()

Bisection(1,2,'a')
Bisection(0,1,'b')
Bisection(1,2,'c')
Bisection(2,4,'c')
Bisection(0,.5,'d')
Bisection(.5,1,'d')


