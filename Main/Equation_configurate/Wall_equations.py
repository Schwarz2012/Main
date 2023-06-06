import Operations as oper #Additional operations and equations
from numbers import Real
from symtable import Symbol
import numpy
import scipy
import sympy
#Const
sig = 5.67*10**(-8)


def walleq(wallnum, ceiling, ceilingRS, floor, floorRS, wall, wallRS, wallOp, ctwr, ftwr, wtwr, wtor):
    wn = str(wallnum)
    #Variables seting
    Twi = {}
    for i in range(1,5,1):
        Twi[i] = sympy.Symbol('Twi' + str(i), real=True, positive=True)
    Tfi = sympy.Symbol('Tfi', real=True, positive=True)
    Tci = sympy.Symbol('Tci', real=True, positive=True)
    TwOpi = {}
    for i in range(len(wallOp)):
        for j in range(len(wallOp[i])):
            TwOpi[str(i+1) + str(j+1)] = sympy.Symbol('Tw' + str(i+1) + 'Op' + str(j+1), real=True, positive=True)
    #Equation configuration
    eq = 0
    #Wall to wall
    for i in range(1,5,1):
        if i == wallnum:
            continue
        else:
            eq += (sig * wtwr[wn + str(i)]['FW' + wn + 'W' + str(i)]*(Twi[i]**4 - Twi[wallnum]**4))/(oper.eps(wall[i-1].eps, wall[wallnum-1].eps))
    #Ceiling RS to wall
    if len(ceilingRS) != 0:
        eq += (sig * ctwr['c' + wn]['FCRSW'] *(ceilingRS[0].TRS**4 - Twi[wallnum]**4))/(oper.eps(ceilingRS[0].eps, wall[wallnum-1].eps))
    #Ceiling to wall
    eq += (sig * ctwr['c' + wn]['FCW'] *(Tci**4 - Twi[wallnum]**4))/(oper.eps(ceiling.eps, wall[wallnum-1].eps))
    #Floor RS to wall
    if len(floorRS) != 0:
        eq += (sig * ftwr['f' + wn]['FFRSW'] *(floorRS[0].TRS**4 - Twi[wallnum]**4))/(oper.eps(floorRS[0].eps, wall[wallnum-1].eps))
    #Floor to wall
    eq += (sig * ftwr['f' + wn]['FFW'] *(Tfi**4 - Twi[wallnum]**4))/(oper.eps(floor.eps, wall[wallnum-1].eps))
    #Wall RS to wall
    for i in range(1,5,1):
        if i == wallnum:
            continue
        else:
            if len(wallRS[i-1]) != 0:
                eq += (sig * wtwr[wn + str(i)]['FW' + wn +'W' + str(i) + 'RS'] *(wallRS[i-1][0].__dict__['TRS']**4 - Twi[wallnum]**4))/(oper.eps(wallRS[i-1][0].eps, wall[wallnum-1].eps))
    #Wall Op to wall
    for i in range(1,5,1):
        if i != wallnum:
            for j in range(len(wallOp[i-1])):
                eq += (sig * wtor[wn + str(i)]['FW' + wn + 'W' + str(i) +'Op'+str(j+1)]*(TwOpi[str(i)+str(j+1)]**4 - Twi[wallnum]**4))/(oper.eps(wallOp[i-1][j].eps, wall[wallnum-1].eps))
    #Looses equation
    eq += wall[wallnum-1].U * oper.area(wallnum, wall, wallRS, wallOp) * (wall[wallnum-1].Tex - Twi[wallnum])

    return(eq)

