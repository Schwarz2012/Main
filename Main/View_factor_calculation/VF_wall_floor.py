from View_factor_calculation import VF_analytic_calc_eq as VFC #View factor calculations analytic equations

def WalltoFloor (wallnum, wall, wallRS, wallOp, floor, floorRS):
    #Wall to floor
    FWF = VFC.perp(wall[wallnum - 1].coordCF, floor.__dict__['coord' + str(wallnum)])
    #Wall to floor RS
    FWFRS = []
    for i  in range (len(floorRS)):
        FWFRS.append(VFC.perp(wall[wallnum - 1].coordCF, floorRS[i].__dict__['coord' + str(wallnum)]))
    #Wall RS to floor
    FWRSF = []
    for i  in range (len(wallRS[wallnum - 1])):
        FWRSF.append(VFC.perp(wallRS[wallnum - 1][i].coordD, floor.__dict__['coord' + str(wallnum)]))
    #Wall RS to floor RS
    FWRSFRS1 = []
    FWRSFRS = []
    for i  in range (len(floorRS)):
        FWRSFRS1.clear()
        for j in range(len(wallRS[wallnum - 1])):
            FWRSFRS1.append(VFC.perp(wallRS[wallnum - 1][j].coordD, floorRS[i].__dict__['coord' + str(wallnum)]))
        FWRSFRS.append(FWRSFRS1)
    #Wall Op to floor
    FWOpF = []
    for i  in range (len(wallOp[wallnum - 1])):
        FWOpF.append(VFC.perp(wallOp[wallnum - 1][i].coordD, floor.__dict__['coord' + str(wallnum)]))
    #Wall Op to floor RS
    FWOpFRS1 = []
    FWOpFRS = []
    for i  in range (len(wallOp[wallnum - 1])):
        FWOpFRS1 = 0
        for j in range(len(floorRS)):
            print(j)
            FWOpFRS1 += (VFC.perp(wallOp[wallnum - 1][i].coordD, floorRS[j].__dict__['coord' + str(wallnum)]))
        FWOpFRS.append(FWOpFRS1)
    return({'FW' + str(wallnum) + 'F':FWF, 'FW' + str(wallnum) + 'FRS':FWFRS, 'FW' + str(wallnum) + 'RSF':FWRSF, 'FW' + str(wallnum) + 'RSFRS':FWRSFRS, 'FW' + str(wallnum) + 'OpF':FWOpF, 'FW' + str(wallnum) + 'OpFRS':FWOpFRS})