import Operations as oper #Additional operations and equations
def results(Texwall, Texfloor, Texceiling, wallOp, ceiling, ceilingRS, floor, floorRS, wall, wallRS):
    Res = {}
    areas = {}
    Res['Ceiling'] = str(Texceiling)
    areas['Ceiling'] = oper.areacf(ceiling, ceilingRS)
    Res['Floor'] = str(Texfloor)
    areas['Floor'] = oper.areacf(floor, floorRS)
    for i in range (1,5,1):
        Res['Wall ' + str(i)] = Texwall[i-1]
        areas['Wall ' + str(i)] = oper.area(i, wall, wallRS, wallOp)
        if len(wallOp[i-1]) != 0:
            for k in range (len(wallOp[i-1])):
                Res['Wall ' + str(i) + ' Window/Door ' + str(k+1)] = Texwall[i-1]
                areas['Wall ' + str(i) + ' Window/Door ' + str(k+1)] = wallOp[i-1][k - 1].area
    
    Res = dict(sorted(Res.items()))
    temp_sum = 0
    for key in Res:
        temp_sum += float(Res[key])*float(areas[key])
    total_area = sum(areas.values())
    Res['Average room temperature'] = str(round(temp_sum/total_area, 1))
    return(Res)