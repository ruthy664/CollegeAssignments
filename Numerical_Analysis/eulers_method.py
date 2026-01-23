# Euler's Method

import math
e = math.e

def update(fb,w,h,f):
    fbn = fb.strip().lower()
    if f=='a':
        if fbn == 'backward':
            return w / (1 + 9*h)
        else:
            return w - h*9*w
    else:
        return 1

def sol(t, f):
    if f=='a':
        return e**(1-9*t)
    else:
        return 1

def euler_method(N,fb,f):
    w = e
    h = 1/N
    t = 0
    max_error = 0.0
    for i in range(1,N+1):
        w = update(fb,w,h,f)
        t = h*i
        solution = sol(t,f)
        error = abs(w - solution)
        if error > max_error:
            max_error = error
    return max_error

def find_errors(fb,f):
    accuracy = {0.1: -1, 0.01: -1, 0.001: -1}
    for N in range(10,5000,1):
        max_error = euler_method(N,fb,f)
        for key in accuracy:
            if max_error <= key and accuracy[key] == -1:
                accuracy[key] = N
        if accuracy[0.001] != -1:
            break
    print(f"{fb.capitalize()} Euler's Method:\n0.1\t{accuracy[0.1]}\n0.01\t{accuracy[0.01]}\n0.001\t{accuracy[0.001]}\n")

find_errors('forward','a')
find_errors('backward','a') 

