from View_factor_calculation import VF_analytic_calc_eq as VFC #View factor calculations analytic equations

def WalltoCeiling(wallnum, wall, wallRS, wallOp, ceiling, ceilingRS):
    #Wall to ceiling
    FWC = VFC.perp(wall[wallnum - 1].coordCF, ceiling.__dict__['coord' + str(wallnum)])
    #Wall to ceiling RS
    FWCRS = []
    for i  in range (len(ceilingRS)):
        FWCRS.append(VFC.perp(wall[wallnum - 1].coordCF, ceilingRS[i].__dict__['coord' + str(wallnum)]))
    #Wall RS to ceiling
    FWRSC = []
    for i  in range (len(wallRS[wallnum - 1])):
        FWRSC.append(VFC.perp(wallRS[wallnum - 1][i].coordUP, ceiling.__dict__['coord' + str(wallnum)]))
    #Wall RS to ceiling RS
    FWRSCRS1 = []
    FWRSCRS = []
    for i  in range (len(ceilingRS)):
        FWRSCRS1.clear()
        for j in range(len(wallRS[wallnum - 1])):
            FWRSCRS1.append(VFC.perp(wallRS[wallnum - 1][j].coordUP, ceilingRS[i].__dict__['coord' + str(wallnum)]))
        FWRSCRS.append(FWRSCRS1)
    #Wall Op to ceiling
    FWOpC = []
    for i  in range (len(wallOp[wallnum - 1])):
        FWOpC.append(VFC.perp(wallOp[wallnum - 1][i].coordUP, ceiling.__dict__['coord' + str(wallnum)]))
    #Wall Op to ceiling RS
    FWOpCRS1 = []
    FWOpCRS = []
    for i  in range (len(wallOp[wallnum - 1])):
        FWOpCRS1 = 0
        for j in range(len(ceilingRS)):
            FWOpCRS1 += (VFC.perp(wallOp[wallnum - 1][i].coordUP, ceilingRS[j].__dict__['coord' + str(wallnum)]))
        FWOpCRS.append(FWOpCRS1)
    return({'FW' + str(wallnum) + 'C':FWC, 'FW' + str(wallnum) + 'CRS':FWCRS, 'FW' + str(wallnum) + 'RSC':FWRSC, 'FW' + str(wallnum) + 'RSCRS':FWRSCRS, 'FW' + str(wallnum) + 'OpC':FWOpC, 'FW' + str(wallnum) + 'OpCRS':FWOpCRS})

