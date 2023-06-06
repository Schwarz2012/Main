from Equation_configurate import Variables_list as vl
import Operations as oper #Additional operations and equations
from numbers import Real
from symtable import Symbol
import numpy
import scipy
import sympy

#Const
sig = 5.67*10**(-8)

def ceilingeq(ceiling, ceilingRS, floor, floorRS, wall, wallRS, wallOp, cfr, ctwr):
    #Variables seting
    var = vl.variables(wallOp)
    #Equation configuration
    eq = 0
    #Floor to ceiling
    eq += (sig * cfr['FCF'] * (var['Tfi']**4  - var['Tci']**4))/(oper.eps(floor.eps, ceiling.eps))
    #Floor RS to ceiling
    if len(floorRS) != 0:
        eq += (sig * cfr['FCFRS'] *(floorRS[0].TRS**4 - var['Tci']**4))/(oper.eps(floorRS[0].eps, ceiling.eps))
    #Wall to ceiling
    for i in range(1,5,1):
        eq += (sig * ctwr['c' + str(i)]['FCW']*(var['Twi' + str(i)]**4 - var['Tci']**4))/(oper.eps(wall[i-1].eps, ceiling.eps))
    #Wall RS to ceiling
    for i in range(1,5,1):        
        if len(wallRS[i-1]) != 0:
            eq += (sig * ctwr['c' + str(i)]['FCWRS'] *(wallRS[i-1][0].TRS**4 - var['Tci']**4))/(oper.eps(wallRS[i-1][0].eps, ceiling.eps))
    #Wall Op to ceiling
    for i in range(1,5,1):
        for j in range(len(wallOp[i-1])):
            eq += (sig * ctwr['c' + str(i)]['FCWOp'][j]*(var['TwOpi'][str(i)+str(j+1)]**4 - var['Tci']**4))/(oper.eps(wallOp[i-1][j].eps, ceiling.eps))
    #Looses equation

    eq += ceiling.U * oper.areacf(ceiling, ceilingRS) * (ceiling.Tex - var['Tci'])





    return(eq)
    #objects = 6 + len()
