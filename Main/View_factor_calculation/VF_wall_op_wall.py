from View_factor_calculation import VF_analytic_calc_eq as VFC #View factor calculations analytic equations
#WAll to opposite wall
def WalltoOpWall(wallnum1, wallnum2, wall, wallRS, wallOp, RW, RL): 
    if wallnum1%2 != 0:
        R = RW
    else:
        R = RL
    VF = {}
    wn1 = str(wallnum1)
    wn2 = str(wallnum2)
    #Wall to wall
    VF['FW' + wn1 + 'W' + wn2] = VFC.par(wall[wallnum1-1].coord, wall[wallnum2-1].coord, R)
    #Wall to Wall RS
    const = 0
    for i  in range (len(wallRS[wallnum2-1])):
        const += (VFC.par(wall[wallnum1-1].coordCF, wallRS[wallnum2-1][i].coordOPrev, R))
    VF['FW' + wn1 + 'W' + wn2 + 'RS'] = const
    #Wall to Wall Op
    for i  in range (len(wallOp[wallnum2-1])):
        VF['FW' + wn1 + 'W' + wn2 + 'Op' + str(i+1)] = (VFC.par(wall[wallnum1-1].coordCF, wallOp[wallnum2-1][i].coordOPrev, R))
    #Wall RS to Wall
    const = 0
    for i  in range (len(wallRS[wallnum1-1])):
        const += (VFC.par(wallRS[wallnum1-1][i].coordOP, wall[wallnum2-1].coordCF, R))
    VF['FW' + wn1 + 'RS' + 'W' + wn2] = const
    #Wall RS to Wall RS
    for i  in range (len(wallRS[wallnum1-1])):
        for j in range(len(wallRS[wallnum2-1])):
            VF['FW' + wn1 + 'RS' + str(i+1) + 'W' + wn2 +'RS' + str(j+1)] = (VFC.par(wallRS[wallnum1-1][i].coordOP, wallRS[wallnum2-1][j].coordOPrev, R))
    #Wall RS to Wall Op
    for i  in range (len(wallOp[wallnum2-1])):
        const = 0
        for j in range(len(wallRS[wallnum1-1])):
            const += (VFC.par(wallRS[wallnum1-1][j].coordOP, wallOp[wallnum2-1][i].coordOPrev, R))
        VF['FW' + wn1 + 'RS' + 'W' + wn2 + 'Op' + str(i+1)] = const
    #Wall Op to Wall
    for i  in range (len(wallOp[wallnum1-1])):
        VF['FW' + wn1 + 'Op' + str(i+1) + 'W' + wn2] = (VFC.par(wallOp[wallnum1-1][i].coordOPrev, wall[wallnum2-1].coordCF, R))
    #Wall Op to Wall RS
    for i  in range (len(wallOp[wallnum1-1])):
        const = 0
        for j in range(len(wallRS[wallnum2-1])):
            const += (VFC.par(wallOp[wallnum1-1][i].coordOP, wallRS[wallnum2-1][j].coordOPrev, R))
        VF['FW' + wn1 + 'Op' + str(i+1) + 'W' + wn2 + 'RS'] = const
    #Wall Op to Wall Op
    for i  in range (len(wallOp[wallnum1-1])):
        for j in range(len(wallOp[wallnum2-1])):
            VF['FW' + wn1 + 'Op' + str(i+1) + 'W' + wn2 + 'Op' + str(j+1)] = (VFC.par(wallOp[wallnum1-1][i].coordOP, wallOp[wallnum2-1][j].coordOPrev, R))

    return(VF)