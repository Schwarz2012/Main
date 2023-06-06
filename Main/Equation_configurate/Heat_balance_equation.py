from Equation_configurate import Variables_list as vl
import Operations as oper #Additional operations and equations
from numbers import Real
from symtable import Symbol
import numpy
import scipy
import sympy

#Const
sig = 5.67*10**(-8)

def heatbaleq(ceiling, ceilingRS, floor, floorRS, wall, wallRS, wallOp, cfr, ctwr, ftwr, wtwr, wtor):
    #Variables seting
    var = vl.variables(wallOp)
    #Equation configuration
    eq = 0
    #Floor
    #Floor RS to ceiling
    if len(floorRS) != 0:
        eq += (sig * cfr['FCFRS'] *(floorRS[0].TRS**4 - var['Tci']**4))/(oper.eps(floorRS[0].eps, ceiling.eps))
    #Floor RS to wall
    if len(floorRS) != 0:
        for i in range(1,5,1):
            eq += (sig * ftwr['f' + str(i)]['FFRSW'] *(floorRS[0].TRS**4 - var['Twi' + str(i)]**4))/(oper.eps(floorRS[0].eps, wall[i-1].eps))
    #Ceiling
    #Ceiling RS to floor
    if len(ceilingRS) != 0:
        eq += (sig * cfr['FCRSF'] *(ceilingRS[0].TRS**4 - var['Tfi']**4))/(oper.eps(ceilingRS[0].eps, floor.eps))
    #Ceiling RS to walls
    if len(ceilingRS) != 0:
        for i in range(1,5,1):
            eq += (sig * ctwr['c' + str(i)]['FCRSW'] *(ceilingRS[0].TRS**4 - var['Twi' + str(i)]**4))/(oper.eps(ceilingRS[0].eps, wall[i-1].eps))
    #Walls
    #Wall RS to walls
    for j in range(1,5,1):
        for i in range(1,5,1):
            if i == j:
                continue
            else:
                if len(wallRS[i-1]) != 0:
                    eq += (sig * wtwr[str(j) + str(i)]['FW' + str(j) +'W' + str(i) + 'RS'] *(wallRS[i-1][0].TRS**4 - var['Twi' + str(j)]**4))/(oper.eps(wallRS[i-1][0].eps, wall[j-1].eps))
    #Wall RS to ceiling
    for i in range(1,5,1):        
        if len(wallRS[i-1]) != 0:
            eq += (sig * ctwr['c' + str(i)]['FCWRS'] *(wallRS[i-1][0].TRS**4 - var['Tci']**4))/(oper.eps(wallRS[i-1][0].eps, ceiling.eps))
    #Wall RS to floor
    for i in range(1,5,1):        
        if len(wallRS[i-1]) != 0:
            eq += (sig * ftwr['f' + str(i)]['FFWRS'] *(wallRS[i-1][0].TRS**4 - var['Tfi']**4))/(oper.eps(wallRS[i-1][0].eps, floor.eps))
    #Looses
    #Floor
    eq += floor.U * oper.areacf(floor, floorRS) * (floor.Tex - var['Tfi'])
    #Ceiling
    eq += ceiling.U * oper.areacf(ceiling, ceilingRS) * (ceiling.Tex - var['Tci'])
    #Walls
    for i in range(1,5,1):
        eq += wall[i-1].U * oper.area(i, wall, wallRS, wallOp) * (wall[i-1].Tex - var['Twi' + str(i)])
    return(eq)