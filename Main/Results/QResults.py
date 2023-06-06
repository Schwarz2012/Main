import numpy as np
import scipy
import sympy
import Operations as oper #Additional operations and equations
from Equation_configurate import Variables_list as vl
sig = 5.67*10**(-8)


def results(sol, ceilingRS, floorRS, wallRS, wallOp, cfr, ctwr, ftwr, wtwr, wtor, ceiling, floor, wall):

    var_list = oper.varkey(vl.variables(wallOp))
    temp_res_list = dict(zip(var_list, sol))
    #Heat power
    Res = {'Heat power':{}, 'Heat flux':{}}
    #Ceiling RS
    if len(ceilingRS) != 0:
        QCRS = (sig * cfr['FCRSF'] * (ceilingRS[0].TRS**4 - temp_res_list['Tfi']**4))/(oper.eps(ceilingRS[0].eps, floor.eps))
        for i in range(1,5,1):
            QCRS += (sig * ctwr['c' + str(i)]['FCRSW'] *(ceilingRS[0].TRS**4 - temp_res_list['Twi' + str(i)]**4))/(oper.eps(ceilingRS[0].eps, wall[i-1].eps))
        for i in range(1,5,1):
            for j in range(len(wallOp[i-1])):
                QCRS += (sig * ctwr['c' + str(i)]['FCRSWOp'][j-1] * (ceilingRS[0].TRS**4 - temp_res_list['Tw' + str(i) + 'Op' + str(j+1)]**4))/(oper.eps(ceilingRS[0].eps, wallOp[i-1][j].eps))
        Res['Heat power']['Ceiling'] = str(round(QCRS, 2))
        Res['Heat flux']['Ceiling'] = str(round(QCRS/oper.parsum(ceilingRS, 'area'), 2))
    else:
        Res['Heat power']['Ceiling'] = '0'
        Res['Heat flux']['Ceiling'] = '0'
    
    #Floor RS
    if len(floorRS) != 0:
        QFRS = (sig * cfr['FCFRS'] * (floorRS[0].TRS**4 - temp_res_list['Tci']**4))/(oper.eps(floorRS[0].eps, ceiling.eps))
        for i in range(1,5,1):
            QFRS += (sig * ftwr['f' + str(i)]['FFRSW'] *(floorRS[0].TRS**4 - temp_res_list['Twi' + str(i)]**4))/(oper.eps(floorRS[0].eps, wall[i-1].eps))
        for i in range(1,5,1):
            for j in range(len(wallOp[i-1])):
                QFRS += (sig * ftwr['f' + str(i)]['FFRSWOp'][j-1] * (floorRS[0].TRS**4 - temp_res_list['Tw' + str(i) + 'Op' + str(j+1)]**4))/(oper.eps(floorRS[0].eps, wallOp[i-1][j].eps))
        Res['Heat power']['Floor'] = str(round(QFRS, 2))
        Res['Heat flux']['Floor'] = str(round(QFRS/oper.parsum(floorRS, 'area'), 2))
    else:
        Res['Heat power']['Floor'] = '0'
        Res['Heat flux']['Floor'] = '0'
    #Walls RS
    for i in range(1,5,1):       
        if len(wallRS[i-1]) != 0:
            QWRS = 0
            for wallnum in range(1,5,1):
                wn = str(wallnum)
                if wallnum != i:
                    QWRS += (sig * wtwr[wn + str(i)]['FW' + wn +'W' + str(i) + 'RS'] *(wallRS[i-1][0].TRS**4 - temp_res_list['Twi' + wn]**4))/(oper.eps(wallRS[i-1][0].eps, wall[wallnum-1].eps))
                    if len(wallOp[wallnum-1]) != 0 :
                        for opnum in range(len(wallOp[wallnum-1])):
                            on = str(opnum+1)
                            QWRS += (sig * wtor[str(i) + wn]['FW' + str(i) +'RSW' + wn + 'Op' + on] *(wallRS[i-1][0].TRS**4 - temp_res_list['Tw' + wn + 'Op' + on]**4))/(oper.eps(wallRS[i-1][0].eps, wallOp[wallnum-1][opnum].eps))
            QWRS += (sig * ftwr['f' + str(i)]['FFWRS'] *(wallRS[i-1][0].TRS**4 - temp_res_list['Tfi']**4))/(oper.eps(wallRS[i-1][0].eps, floor.eps)) 
            QWRS += (sig * ctwr['c' + str(i)]['FCWRS'] *(wallRS[i-1][0].TRS**4 - temp_res_list['Tci']**4))/(oper.eps(wallRS[i-1][0].eps, ceiling.eps))
            Res['Heat power']['Wall ' +str(i)] = str(round(QWRS, 2))
            Res['Heat flux']['Wall ' +str(i)] = str(round(QWRS/oper.parsum(wallRS[i-1], 'area'), 2))
        else:
            Res['Heat power']['Wall ' +str(i)] = '0'
            Res['Heat flux']['Wall ' +str(i)] = '0'
    for i in range(1,5,1):
        if len(wallOp[i-1]) !=0:
            for k in range(len(wallOp[i-1])):
                Res['Heat power']['Wall ' +str(i) + ' Window/Door ' + str(k+1)] = '0'
                Res['Heat flux']['Wall ' +str(i) + ' Window/Door ' + str(k+1)] = '0'

    Res['Heat power']= dict(sorted(Res['Heat power'].items()))
    Res['Heat flux']= dict(sorted(Res['Heat flux'].items()))
    #Summ
    SumHP = 0
    SumHF = 0
    for key in Res['Heat power']:
        SumHP += float(Res['Heat power'][key])
    for key in Res['Heat flux']:
        SumHF += float(Res['Heat flux'][key])
    Res['Heat power']['Total'] = str(round(SumHP, 2))
    Res['Heat flux']['Total'] = str(round(SumHF, 2))    

    return(Res)