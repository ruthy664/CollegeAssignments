# Euler's Method with Error and Perturbation Analysis

import math

def funct(t, y, f):
    f = f.strip()

    if f == 'a':
        return (2/t) * y + (t**2) * (math.e**t)
    else:
        allowed = {"__builtins__": None}
        allowed.update(math.__dict__)
        try:
            return eval(f, allowed, {"t": t, "y": y})
        except Exception as e:
            print("Invalid function:", e)
            return None
        
def yof(t):
    return t**2*(math.e**t-math.e)
        
def out(t,w):
    y = yof(t)
    error = abs(w-y)
    print(f"t = {t:.2f} \tw = {w:.4f} \ty = {y:.4f} \terror = {error:.4f}")

def init_value(a,b,N,w,f):
    h = (b-a)/N
    t = a
    print(f"\nTable for h = {h} and f({a}) = {w}")
    out(t,w)
    for i in range(1,N+1):
        w = w + h*funct(t,w,f)
        t = a + h*i
        out(t,w)

def perturb(a,b,N,w1,w2,f):
    h = (b-a)/N
    t = a
    init1 = w1
    init2 = w2
    yval = []
    w1_value = []
    w2_value = []
    w1_error = []
    w2_error = []
    yval.append(yof(t))
    w1_value.append(w1)
    w2_value.append(w2)
    w1_error.append(abs(w1-yof(t)))
    w2_error.append(abs(w2-yof(t)))
    for i in range(1,N+1):
        w1 = w1 + h*funct(t,w1,f)
        w2 = w2 + h*funct(t,w2,f)
        t = a + h*i
        yval.append(yof(t))
        w1_value.append(w1)
        w2_value.append(w2)
        w1_error.append(abs(w1-yof(t)))
        w2_error.append(abs(w2-yof(t)))
    print(f"\nPerturb tables for f({a}) = {init1} and f({a}) = {init2} with h = {h}")
    print("actual value\tw1_value\tw2_value\tw1_error\tw2_error\terror difference")
    for i in range (N+1):
        print(f"{yval[i]: .4f}\t\t{w1_value[i]: .4f}\t\t{w2_value[i]: .4f}\t\t{w1_error[i]: .4f}\t\t{w2_error[i]:.4f}\t\t{abs(w1_error[i]-w2_error[i]): .4f}")

init_value(1,2,10,0,'a')
init_value(1,2,20,0,'a')
init_value(1,2,10,0.1,'a')
init_value(1,2,20,0.1,'a')
perturb(1,2,10,0,0.1,'a')
perturb(1,2,20,0,0.1,'a')