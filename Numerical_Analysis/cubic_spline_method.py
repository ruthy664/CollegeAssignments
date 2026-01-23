import matplotlib.pyplot as plt

def func(x):
    return (x**4)+(27*x)-2
def func1(x):
    return 1
def funcx(x):
    return x
def funcx2(x):
    return x**2
def funcx3(x):
    return x**3
def B10(x, a, b):
    return (b-x)/(b-a)
def B01(x, a, b):
    return (x-a)/(b-a)

def linearSpline(f, interval, n, funcText):
    if (len(interval)!=2):
        print("Invalid interval: ", interval, ". Length: ",len(interval))
        return
    left = interval[0]
    right = interval[1]
    if left>right:
        print("Invalid interval: ",interval)
        return
    intervalLen = right-left
    intervalStep = intervalLen / n
    b = left + intervalStep
    plt.figure(figsize=(14, 8))
    while left<right:
        x=left
        subIntervalStep = (b-left)/100
        while x<=b:
            if(b-x)==0:
                print('b - x == 0')
                return
            y = f(left)*B10(x, left, b)+f(b)*B01(x, left, b)
            plt.plot(x, y, "-o")
            x+=subIntervalStep
        b+=intervalStep
        left+=intervalStep

    legendLabels = f'\nLinear Spline\nFunction: '+funcText+f'\nInterval: [{interval[0]}, {interval[1]}]\nSub Intervals: {n}'
   
    plt.title(legendLabels)
    plt.xlabel("x-Axis")
    plt.ylabel("y-Axis")
    plt.show()
   

def B30(x, a, b):
    return B10(x, a, b)**3

def B21(x, a, b):
    return 3* (B10(x, a, b)**2)*B01(x, a, b)
def B12(x, a, b):
    return 3* (B01(x, a, b)**2)*B10(x, a, b)
def B03(x, a, b):
    return B01(x, a, b)**3

def derivative(f, x):
    h=1e-6
    return (f(x + h) - f(x - h)) / (2 * h)

def cubicSpline(f, interval, n, funcText):
    if (len(interval)!=2):
        print("Invalid interval: ", interval, ". Length: ",len(interval))
        return
    left = interval[0]
    right = interval[1]
    if left>right:
        print("Invalid interval: ",interval, ". Left > Right")
        return
    intervalLen = right-left
    intervalStep = intervalLen / n
    b = left + intervalStep
    plt.figure(figsize=(14, 8))
    while left<right:
        x=left
        subIntervalStep = (b-left)/100
        while x<=b:
            if(b-x)==0:
                print('b - x == 0')
                return
            y = (f(left)*B30(x, left, b))+((f(left)+((b-left)/3)*derivative(f, left))*B21(x, left, b)) + ((f(b)-((b-left)/3)*derivative(f,b))*B12(x, left, b))+(f(b)*B03(x, left, b))
            plt.plot(x, y, "-o")
            x+=subIntervalStep
        b+=intervalStep
        left+=intervalStep
    legendLabels = f'\nCubic Spline\nFunction: '+funcText+f'\nInterval: [{interval[0]}, {interval[1]}]\nSub Intervals: {n}'
   
    plt.title(legendLabels)
    plt.xlabel("x-Axis")
    plt.ylabel("y-Axis")
    plt.show()

#linearSpline(func, [-5, 2], 15, r'$x^4+27x-2$')
#cubicSpline(func, [-5, 2], 15, r'$x^4+27x-2$')

linearSpline(func1, [-5, 5], 15, r'$1$')
cubicSpline(func1, [-5, 5], 15, r'$1$')

#linearSpline(funcx, [-5, 5], 15, r'$1$')
#cubicSpline(funcx, [-5, 5], 15, r'$1$')
