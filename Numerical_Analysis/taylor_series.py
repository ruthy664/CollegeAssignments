# Taylor Series Approximation of ln(x) at x = 1

import numpy as np
ln = np.log(1.5)

def Pn(N,x):
    summ = 0
    for i in range(1,N+1):
        sumi = (((-1)**(i+1))/i)*((x-1)**i)
        summ = summ + sumi
    return summ

for N in range(1,11):
    PN = Pn(N,1.5)
    if abs(ln-PN) < 10**(-3):
        print("Minimal Value for N is",N)
        break

# Output: Minimal Value for N is 6