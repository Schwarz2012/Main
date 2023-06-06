from cmath import sqrt
from cmath import atan
import math
import MyModul

#Convert coordinates to view factors for each variant of surface connection [CMCi, CiCj, CiCk, ..., CiF]

def vfcomp(a, RW, RL, RH):

    F = []
    FF = []
    for j in range (0, len(a)-1):
        if j == 0:
            F.append(MyModul.vfpar(a[0], a[5], RH))
        else:
            for i in range(0, len(a)):
                if i == j:
                    continue
                elif i == 0:
                    if j%2 != 0:
                        F.append(MyModul.vfperp(MyModul.rot(a[j]), a[i]))
                    else:
                        F.append(MyModul.vfperp(MyModul.rot(a[j]), MyModul.rot(a[i])))
                elif i == 5:
                    if j%2 != 0:
                        F.append(MyModul.vfperp(MyModul.rot(a[j]), a[i]))
                    else:
                        F.append(MyModul.vfperp(MyModul.rot(a[j]), MyModul.rot(a[i])))
                elif i == j+2 and i != 5 and i != 0 and i%2 != 0 or i == j-2 and i != 5 and i != 0 and i%2 != 0:
                    F.append(MyModul.vfpar(a[j], a[i], RW))
                elif i == j+2 and i != 5 and i != 0 and i%2 == 0 or i == j-2 and i != 5 and i != 0 and i%2 == 0:
                    F.append(MyModul.vfpar(a[j], a[i], RL))
                else:
                    F.append(MyModul.vfperp(a[j], a[i]))
        
        FF.append(F[0:len(F)])
        F.clear()
    return(FF)


#eps convertion

def epsconv(epsz):
    c = []
    cc = []
    for j in range (0, len(epsz)-1):
        if j == 0:
            c.append(MyModul.eps(epsz[0], epsz[5]))
        else:
            for i in range(0, len(epsz)):
                if i == j:
                    continue
            
                else:
                    c.append(MyModul.eps(epsz[j], epsz[i]))
        
        cc.append(c[0:len(c)])
        c.clear()
    return(cc)

def uconv(a):
    Uval = []
    for i in range(0, len(a)):
        alpha = 0
        if i !=4:
            alpha = 0.13
        else:
            alpha = 0.1
        Uval.append(a[i]/(1-a[i]*alpha))
    return(Uval)