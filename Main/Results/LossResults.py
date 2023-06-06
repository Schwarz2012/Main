import numpy as np
import scipy
import sympy
import Operations as oper #Additional operations and equations
from Equation_configurate import Variables_list as vl
sig = 5.67*10**(-8)


def results(sol, ceilingRS, floorRS, wallRS, wallOp, cfr, ctwr, ftwr, wtwr, wtor, ceiling, floor, wall):

    var_list = oper.varkey(vl.variables(wallOp))
    temp_res_list = dict(zip(var_list, sol))
    #Losses   
    Res = {}
    #Walls
    for i in range(1,5,1):
        Res['Wall ' + str(i)] = str(round(wall[i-1].U * oper.area(i, wall, wallRS, wallOp) * (wall[i-1].Tex - temp_res_list['Twi' + str(i)]),2))        
    #Floor
    Res['Floor'] = str(round(floor.U * oper.areacf(floor, floorRS) * (floor.Tex - temp_res_list['Tfi']), 2))
    #Ceiling    
    Res['Ceiling'] = str(round(ceiling.U * oper.areacf(ceiling, ceilingRS) * (ceiling.Tex - temp_res_list['Tci']), 2))
    #Openings    
    for wallnum in range(1,5,1):
        if len(wallOp[wallnum-1]) !=0:
            for opnum in range(len(wallOp[wallnum-1])):
                Res['Wall ' + str(wallnum) + ' Window/Door ' + str(opnum+1)] = str(round(wallOp[wallnum-1][opnum].U * wallOp[wallnum-1][opnum].area * (wallOp[wallnum-1][opnum].Tex - temp_res_list['Tw' + str(wallnum) + 'Op' + str(opnum+1)]), 2))

    Res = dict(sorted(Res.items()))                  
    #Sum
    SumP = 0
    for key in Res:
        SumP += float(Res[key])
    Res['Total'] = str(round(SumP, 2))
    return(Res)