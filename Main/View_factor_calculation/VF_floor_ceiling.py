from View_factor_calculation import VF_analytic_calc_eq as VFC #View factor calculations analytic equations

def FloortoCeiling(ceiling, ceilingRS, floor, floorRS, RH): 
    #Ceiling to floor
    FCF = VFC.par(ceiling.coord1, floor.coord1, RH)
    #Ceiling to floor RS
    FCFRS = []
    for i in range(len(floorRS)):
        FCFRS.append(VFC.par(ceiling.coord1, floorRS[i].coordF, RH))
    #Ceiling RS to floor
    FCRSF = []
    for i in range(len(ceilingRS)):
        FCRSF.append(VFC.par(ceilingRS[i].coordF, floor.coord1, RH))
    #Ceiling RS to floor RS
    FCRSFRS = []
    FCRSFRS1 = []
    for i in range(len(ceilingRS)):
        FCRSFRS1.clear()
        for j in range(len(floorRS)):
            FCRSFRS1.append(VFC.par(ceilingRS[i].coordF, floorRS[j].coordF, RH))
        FCRSFRS.append(FCRSFRS1)



    return({'FCF': FCF, 'FCFRS': FCFRS, 'FCRSF': FCRSF, 'FCRSFRS': FCRSFRS})
