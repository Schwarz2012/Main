import Operations as oper #Additional operations and equations
from Equation_configurate import Variables_list as vl
sig = 5.67*10**(-8)


def results(sol, ceilingRS, floorRS, wallRS, wallOp, cfr, ctwr, ftwr, wtwr, wtor, ceiling, floor, wall):
    var_list = oper.varkey(vl.variables(wallOp))
    areas = {}
    var_list_correct = []
    for var in var_list:
        if ('Twi' in var) == True:
            var_list_correct.append('Wall ' + var[-1])
            areas['Wall ' + var[-1]] = oper.area(int(var[-1]), wall, wallRS, wallOp)
        elif ('Tfi' in var) == True:
            var_list_correct.append('Floor')
            areas['Floor'] = oper.areacf(floor, floorRS)
        elif ('Tci' in var) == True:
            var_list_correct.append('Ceiling')
            areas['Ceiling'] = oper.areacf(ceiling, ceilingRS)
        elif ('Op' in var) == True:
            var_list_correct.append('Wall ' + var[-4] + ' Window/Door ' + var[-1])
            areas['Wall ' + var[-4] + ' Window/Door ' + var[-1]] = wallOp[int(var[-4])-1][int(var[-1]) - 1].area
    
    sol1 = []
    for temp in sol:
        sol1.append(str(round(temp - 273.15, 1)))
    Res = dict(zip(var_list_correct, sol1))
    Res = dict(sorted(Res.items()))
    temp_sum = 0
    for key in Res:
        temp_sum += float(Res[key])*float(areas[key])
    total_area = sum(areas.values())
    Res['Average room temperature'] = str(round(temp_sum/total_area, 1))

    return(Res)