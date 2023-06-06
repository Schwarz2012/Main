from Equation_configurate import Variables_list as vl
import Operations as oper #Additional operations and equations
from numbers import Real
from symtable import Symbol
import numpy
import scipy
import sympy
#Const
sig = 5.67*10**(-8)


def openingeq(wallnum, opnum, ceiling, ceilingRS, floor, floorRS, wall, wallRS, wallOp, ctwr, ftwr, wtor):
    wn = str(wallnum)
    on = str(opnum)
    #Variables seting
    var = vl.variables(wallOp)
    #Equation configuration
    eq = 0 
    #Ceiling RS to wall Op
    if len(ceilingRS) != 0:
        eq += (sig * ctwr['c' + wn]['FCRSWOp'][opnum-1] * (ceilingRS[0].TRS**4 - var['TwOpi'][wn + on]**4))/(oper.eps(ceilingRS[0].eps, wallOp[wallnum-1][opnum-1].eps))   
    #Ceiling to wall Op
    eq += (sig * ctwr['c' + wn]['FCWOp'][opnum-1] * (var['Tci']**4 - var['TwOpi'][wn + on]**4))/(oper.eps(ceiling.eps, wallOp[wallnum-1][opnum-1].eps))
    #Floor RS to wall Op
    if len(floorRS) != 0:
        eq += (sig * ftwr['f' + wn]['FFRSWOp'][opnum-1] * (floorRS[0].TRS**4 - var['TwOpi'][wn + on]**4))/(oper.eps(floorRS[0].eps, wallOp[wallnum-1][opnum-1].eps))
    #Floor to wall Op
    eq += (sig * ftwr['f' + wn]['FFWOp'][opnum-1] * (var['Tfi']**4 - var['TwOpi'][wn + on]**4))/(oper.eps(floor.eps, wallOp[wallnum-1][opnum-1].eps)) 
    #Wall RS to wall Op
    for i in range(1,5,1):
        if i != wallnum:
            if len(wallRS[i-1]) != 0:
                eq += (sig * wtor[str(i) + wn]['FW' + str(i) +'RSW' + wn + 'Op' + on] *(wallRS[i-1][0].TRS**4 - var['TwOpi'][wn + on]**4))/(oper.eps(wallRS[i-1][0].eps, wallOp[wallnum-1][opnum-1].eps))
    #Wall Op to wall Op
    for i in range(1,5,1):
        if i != wallnum:
            for j in range(len(wallOp[i-1])):
                eq += (sig * wtor[wn + str(i)]['FW' + wn + 'Op' + on + 'W' + str(i) +'Op' + str(j+1)]*(var['TwOpi'][str(i)+str(j+1)]**4 - var['TwOpi'][wn + on]**4))/(oper.eps(wallOp[i-1][j].eps, wallOp[wallnum-1][opnum-1].eps))
    #Wall to wall Op   
    for i in range(1,5,1):
        if i != wallnum:
            eq += (sig* wtor[str(i) + wn]['FW' + str(i) + 'W' + wn + 'Op' + on]*(var['Twi' + str(i)]**4 - var['TwOpi'][wn + on]**4))/(oper.eps(wall[i-1].eps, wallOp[wallnum-1][opnum-1].eps))
                
    #Looses equation

    eq += wallOp[wallnum-1][opnum-1].U * wallOp[wallnum-1][opnum-1].area * (wallOp[wallnum-1][opnum-1].Tex - var['TwOpi'][wn + on])


    return(eq)
