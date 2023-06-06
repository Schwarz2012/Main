from Equation_configurate import Variables_list as vl
import Operations as oper #Additional operations and equations
from numbers import Real
from symtable import Symbol
import numpy
import scipy
import sympy

#Const
sig = 5.67*10**(-8)

#eq += (sig * ftwr['f' + str(i)]['FFW']*(var['Twi' + str(i)]**4 - var['Tfi']**4))/(oper.eps(wall[i-1].eps, floor.eps))

def flooreq(ceiling, ceilingRS, floor, floorRS, wall, wallRS, wallOp, cfr, ftwr):
    #Variables seting
    var = vl.variables(wallOp)
    #Equation configuration
    eq = 0
    #Ceiling to floor
    eq += (sig * cfr['FCF'] * (var['Tci']**4 - var['Tfi']**4))/(oper.eps(floor.eps, ceiling.eps))
    #Ceiling RS to floor
    if len(ceilingRS) != 0:
        eq += (sig * cfr['FCRSF'] *(ceilingRS[0].TRS**4 - var['Tfi']**4))/(oper.eps(ceilingRS[0].eps, floor.eps))
    #Wall to floor
    for i in range(1,5,1):
        eq += (sig * ftwr['f' + str(i)]['FFW']*(var['Twi' + str(i)]**4 - var['Tfi']**4))/(oper.eps(wall[i-1].eps, floor.eps))
    #Wall RS to floor
    for i in range(1,5,1):        
        if len(wallRS[i-1]) != 0:
            eq += (sig * ftwr['f' + str(i)]['FFWRS'] *(wallRS[i-1][0].TRS**4 - var['Tfi']**4))/(oper.eps(wallRS[i-1][0].eps, floor.eps))
    #Wall Op to floor
    for i in range(1,5,1):
        for j in range(len(wallOp[i-1])):
            eq += (sig * ftwr['f' + str(i)]['FFWOp'][j]*(var['TwOpi'][str(i)+str(j+1)]**4 - var['Tfi']**4))/(oper.eps(wallOp[i-1][j].eps, floor.eps))
    #Looses equation

    eq += floor.U * oper.areacf(floor, floorRS) * (floor.Tex - var['Tfi'])





    return(eq)
    #objects = 6 + len()
