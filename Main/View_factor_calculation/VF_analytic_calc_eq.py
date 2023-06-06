#View factor calculation analytical equations 
import math
import numpy
#Parallel
def par(a, b, h):
    x = [a[0], a[1]]
    y = [a[2], a[3]]
    a = [b[0], b[1]]
    b = [b[2], b[3]]
    F = 0.0
    for i in range (1, 3):
        for j in range (1, 3):
            for k in range (1, 3):
                for l in range (1, 3):
                    summ = (((-1) ** (i + j + k + l))/(2*math.pi))*((b[k-1]-y[l-1])*abs(math.sqrt(((x[j-1]-a[i-1]) ** 2) + h**2))*math.atan((b[k-1]-y[l-1])/abs(math.sqrt(((x[j-1]-a[i-1]) ** 2) + h**2))) + (x[j-1]-a[i-1]) * abs(math.sqrt(((b[k-1]-y[l-1]) ** 2) + h**2)) *  math.atan((x[j-1]-a[i-1])/(abs(math.sqrt(((b[k-1]-y[l-1]) ** 2) + h**2)))) - ((h**2)/2) * math.log(((b[k-1]-y[l-1]) ** 2) + ((x[j-1]-a[i-1]) ** 2) + h**2))
                    F +=summ
    return(round(F, 4))

#Perpendicular
def perp(a, b):
    x = [a[0], a[1]]
    y = [a[2], a[3]]
    a = [b[0], b[1]]
    b = [b[2]+10**(-6), b[3]]
    F = 0.0
    for i in range (1, 3):
        for j in range (1, 3):
            for k in range (1, 3):
                for l in range (1, 3):
                    summ = (((-1) ** (i + j + k + l))/(math.pi))*((1/8) * ((x[k-1] - a[l-1])**2 - y[i-1] ** 2 - b[j-1] ** 2) * math.log((x[k-1] - a[l-1])**2 + y[i-1] ** 2 + b[j-1] ** 2) + ((1/2)*(x[k-1] - a[l-1]) * abs(math.sqrt(y[i-1] ** 2 + b[j-1] ** 2)) * math.atan((x[k-1] - a[l-1])/abs(math.sqrt(y[i-1] ** 2 + b[j-1] ** 2)))))
                    F +=summ
    return(round(F, 4))
