from numbers import Real
from symtable import Symbol
from scipy.optimize import fsolve
import numpy as np
import scipy
import sympy
import Operations as oper #Additional operations and equations
import Classes_list as Classes #Classes list for walls, oppenings and radiant surfaces
from View_factor_calculation import VF_wall_ceiling as VFWC #View factor calculations analytic equations
from View_factor_calculation import VF_wall_floor as VFWF #View factor calculations analytic equations
from View_factor_calculation import VF_wall_wall as VFWW #View factor calculations analytic equations
from View_factor_calculation import VF_wall_op_wall as VFWoW #View factor calculations analytic equations
from View_factor_calculation import VF_floor_ceiling as VFFC #View factor calculations analytic equations
from View_factor_convertation import VF_ceiling_to_walls_result as VFWCr #Result convertation of view factors from ceiling to walls
from View_factor_convertation import VF_floor_to_walls_result as VFWFr #Result convertation of view factors from floor to walls
from View_factor_convertation import VF_walls_to_walls_result as VFWWr #Result convertation of view factors from floor to walls
from View_factor_convertation import VF_walls_to_openings_result as VFWOpr
from Equation_configurate import Wall_equations as weq
from Equation_configurate import Variables_list as vl
from Equation_configurate import Floor_equation as feq
from Equation_configurate import Ceiling_equation as ceq
from Equation_configurate import Heat_balance_equation as hbeq
from Equation_configurate import Openings_equations as opeq
from Results import TempResults as Tres
from Results import QResults as Qres
from Results import LossResults as Lres
from Results import TempInit as TIres
import time

def calculation(result):
    # Geometry and phys parametres of structures, radiant surfaces and oppenings
    start = time.time()
    #Room geometry
    RL = result['RG'][0]
    RW = result['RG'][1]
    RH = result['RG'][2]
    #Walls parametres
    Uwall = result['Uwall']
    #[0,0,0,0]
    EPSwall = result['EPSwall']
    Texwall = result['Texwall']
    #Walls RS parametres
    wallRScoord = result['wallRScoord']
    EPSwallRS = result['EPSwallRS']
    TinwallRS = result['TinwallRS']
    #Walls OP parametres
    wallOpcoord = result['wallOpcoord']
    EPSwallOp = result['EPSwallOp']
    TexwallOp = Texwall
    UwallOp = result['UwallOp']
    #Floor parametres
    floorRScoord = result['floorRScoord']
    EPSfloorRS = result['EPSfloorRS']
    TfloorRS = result['TfloorRS']
    Ufloor = result['Ufloor']
    EPSfloor = result['EPSfloor']
    Texfloor = result['Texfloor']
    #Ceiling parametres
    ceilingRScoord = result['ceilingRScoord']
    EPSceilingRS = result['EPSceilingRS']
    TceilingRS = result['TceilingRS']
    Uceiling = result['Uceiling']
    EPSceiling = result['EPSceiling']
    Texceiling = result['Texceiling']
    
    #Objects initiation from classes_list
    #region
    #Ceiling
    ceiling = Classes.Ceiling(EPSceiling, Uceiling, Texceiling, RL, RW)
    #Ceiling RS objects
    ceilingRS = []
    for i in range(len(ceilingRScoord)):
        ceilingRS.append(Classes.CeilingRS(EPSceilingRS[i], TceilingRS[i], ceilingRScoord[i], RL, RW))
    #Floor
    floor = Classes.Floor(EPSfloor, Ufloor, Texfloor, RL, RW)
    #Floor RS objects
    floorRS = []
    for i in range(len(floorRScoord)):
        floorRS.append(Classes.FloorRS(EPSfloorRS[i], TfloorRS[i], floorRScoord[i], RL, RW))
    #Walls
    wall = []
    for i in range(4):
        if i%2 == 0: 
            wall.append(Classes.Walls(EPSwall[i], Uwall[i], Texwall[i], RH, RL))
        else:
            wall.append(Classes.Walls(EPSwall[i], Uwall[i], Texwall[i], RH, RW))
    #Walls RS objects
    wallRS = [[], [], [], []]
    for i in range(len(wallRScoord)):
        for j in range(len(wallRScoord[i])):
            if i%2 == 0: 
                wallRS[i].append(Classes.WallRS(EPSwallRS[i][j], TinwallRS[i][j], wallRScoord[i][j], RL, RH))
            else:
                wallRS[i].append(Classes.WallRS(EPSwallRS[i][j], TinwallRS[i][j], wallRScoord[i][j], RW, RH)) 
    #Walls Op objects
    wallOp = [[], [], [], []]
    for i in range(len(wallOpcoord)):
        for j in range(len(wallOpcoord[i])):
            if i%2 == 0: 
                wallOp[i].append(Classes.WallOp(EPSwallOp[i][j], UwallOp[i][j], TexwallOp[i], wallOpcoord[i][j], RL, RH))
            else:
                wallOp[i].append(Classes.WallOp(EPSwallOp[i][j], UwallOp[i][j], TexwallOp[i], wallOpcoord[i][j], RW, RH)) 
    #endregion

    #View factors calculation
    #region
    #Walls to Walls
    wtw = {} 
    for j in range(1,5,1):
        for i in range(1, 5, 1):
            if i == j:
                continue
            elif abs(i-j) == 2:
                wtw[str(j) + str(i)] = VFWoW.WalltoOpWall(j, i, wall, wallRS, wallOp, RW, RL)
            else:
                wtw[str(j) + str(i)] = VFWW.WalltoWall(j, i, wall, wallRS, wallOp)
    #Ceiling to Wall 1,2,3,4
    ctw = {} 
    for i in range(1,5,1):
        ctw ['c' + str(i)] = VFWC.WalltoCeiling(i, wall, wallRS, wallOp, ceiling, ceilingRS)
    #Floor to Wall 1,2,3,4
    ftw = {} 
    for i in range(1,5,1):
        ftw ['f' + str(i)] = VFWF.WalltoFloor(i, wall, wallRS, wallOp, floor, floorRS)
    #Ceiling to Floor
    cf = VFFC.FloortoCeiling(ceiling, ceilingRS, floor, floorRS, RH)
    #endregion

    #View factors result convertation 
    #region 
    #Ceiling to floor
    cfr = {}
    #Ceiling area to floor area
    cfr['FCF'] = (cf['FCF'] - sum(cf['FCFRS']) ) - (sum(cf['FCRSF'])  - oper.merge(cf['FCRSFRS']))
    #Ceiling RS to floor
    cfr['FCRSF'] = sum(cf['FCRSF']) - oper.merge(cf['FCRSFRS'])
    #Floor RS to ceiling
    cfr['FCFRS'] = sum(cf['FCFRS']) - oper.merge(cf['FCRSFRS'])
    #Ceiling to walls
    ctwr = {}
    for i in range(1,5,1):
        ctwr['c' + str(i)] = VFWCr.ceilingtowall(i, ctw)
    #Floor to walls
    ftwr = {}
    for i in range(1,5,1):
        ftwr['f' + str(i)] = VFWFr.floortowall(i, ftw)
    ##Walls to walls
    wtwr = {}
    for i in range(1,5,1):
        for j in range(1,5,1):
            if i == j:
                continue
            else:
                wtwr[str(i) + str(j)] = VFWWr.walltowall(i, j, wallRS, wallOp, wtw)
    #Walls to Op
    wtor = {}
    for i in range(1,5,1):
        for j in range(1,5,1):
            if i == j:
                continue
            else:
                wtor[str(i) + str(j)] = VFWOpr.walltoopening(i, j, wallOp, wallRS, wtw)
    #endregion
 
    #Equation configurer
    #region
    #var = vl.variables(wallOp)
    Eq = []
    #Wall equations
    for i in range(1,5,1):
        Eq.append(weq.walleq(i, ceiling, ceilingRS, floor, floorRS, wall, wallRS, wallOp, ctwr, ftwr, wtwr, wtor))
    #Floor equation
    Eq.append(feq.flooreq(ceiling, ceilingRS, floor, floorRS, wall, wallRS, wallOp, cfr, ftwr))
    #Ceiling equation
    Eq.append(ceq.ceilingeq(ceiling, ceilingRS, floor, floorRS, wall, wallRS, wallOp, cfr, ctwr)) 
    #Windows equations
    for i in range(1,5,1):
        for j in range(len(wallOp[i-1])):
            Eq.append(opeq.openingeq(i, j+1, ceiling, ceilingRS, floor, floorRS, wall, wallRS, wallOp, ctwr, ftwr, wtor))
    #endregion

    #Equations system formulation
    #region

    def eqsys(x):
        v = oper.varnum(vl.variables(wallOp))
        Eqc = Eq.copy()
        for j in range(len(Eqc)):
            for i in range(len(v)):
                Eqc[j] = Eqc[j].subs(v[i],x[i])
        return(Eqc)
    #endregion

    #Calculation
    #region
    sol = []
    x = np.full((len(oper.varnum(vl.variables(wallOp)))), 273)
    sol = fsolve(eqsys,x)
    #endregion

    #Results
    #region
    Results = {}
    Results['Temperatures'] = Tres.results(sol, ceilingRS, floorRS, wallRS, wallOp, cfr, ctwr, ftwr, wtwr, wtor, ceiling, floor, wall)
    Results['TemperaturesOut'] = TIres.results(Texwall, Texfloor, Texceiling, wallOp, ceiling, ceilingRS, floor, floorRS, wall, wallRS)
    Results['Heat'] = Qres.results(sol, ceilingRS, floorRS, wallRS, wallOp, cfr, ctwr, ftwr, wtwr, wtor, ceiling, floor, wall)
    Results['Losses'] = Lres.results(sol, ceilingRS, floorRS, wallRS, wallOp, cfr, ctwr, ftwr, wtwr, wtor, ceiling, floor, wall)
    Results['Solution time'] = str(round(time.time() - start, 3))
    #endregion



    return(Results)