from View_factor_calculation import VF_analytic_calc_eq as VFC #View factor calculations analytic equations

def WalltoWall(wallnum1, wallnum2, wall, wallRS, wallOp): 
    if wallnum1 < wallnum2 and abs(wallnum2 - wallnum1) == 1:
        side1 = 'R'
        side2 = 'L'
    elif wallnum1 > wallnum2 and abs(wallnum2 - wallnum1) == 1:
        side1 = 'L'
        side2 = 'R'
    elif wallnum1 < wallnum2 and abs(wallnum2 - wallnum1) != 1:
        side1 = 'L'
        side2 = 'R'   
    elif wallnum1 > wallnum2 and abs(wallnum2 - wallnum1) != 1:
        side1 = 'R'
        side2 = 'L'   
    VF = {}
    wn1 = str(wallnum1)
    wn2 = str(wallnum2)
    #Wall to Wall
    VF['FW' + wn1 + 'W' + wn2] = VFC.perp(wall[wallnum1-1].coord, wall[wallnum2-1].coord)
    #Wall to Wall RS
    const = 0
    for i  in range (len(wallRS[wallnum2-1])):
        const += (VFC.perp(wall[wallnum1-1].coord, wallRS[wallnum2-1][i].__dict__['coord' + side2]))
    VF['FW' + wn1 + 'W' + wn2 + 'RS'] = const
    #Wall to Wall Op
    for i  in range (len(wallOp[wallnum2-1])):
        VF['FW' + wn1 + 'W' + wn2 + 'Op' + str(i+1)] = (VFC.perp(wall[wallnum1-1].coord, wallOp[wallnum2-1][i].__dict__['coord' + side2]))
    #Wall RS to Wall
    const = 0
    for i  in range (len(wallRS[wallnum1-1])):
        const += (VFC.perp(wallRS[wallnum1-1][i].__dict__['coord' + side1], wall[wallnum2-1].coord))
        
    VF['FW' + wn1 + 'RS' + 'W' + wn2] = const
    #Wall RS to Wall RS
    for i  in range (len(wallRS[wallnum1-1])):
        for j in range(len(wallRS[wallnum2-1])):
            VF['FW' + wn1 + 'RS' + str(i+1) + 'W' + wn2 +'RS' + str(j+1)] = (VFC.perp(wallRS[wallnum1-1][i].__dict__['coord' + side1], wallRS[wallnum2-1][j].__dict__['coord' + side2]))
    #Wall RS to Wall Op
    for i  in range (len(wallOp[wallnum2-1])):
        const = 0
        for j in range(len(wallRS[wallnum1-1])):
            const += VFC.perp(wallRS[wallnum1-1][j].__dict__['coord' + side1], wallOp[wallnum2-1][i].__dict__['coord' + side2])
        VF['FW' + wn1 + 'RS' + 'W' + wn2 + 'Op' + str(i+1)] = const
    #Wall Op to Wall
    for i  in range (len(wallOp[wallnum1-1])):
        VF['FW' + wn1 + 'Op' + str(i+1) + 'W' + wn2] = (VFC.perp(wallOp[wallnum1-1][i].__dict__['coord' + side1], wall[wallnum2-1].coord))
    #Wall Op to Wall RS
    for i  in range (len(wallOp[wallnum1-1])):
        const = 0
        for j in range(len(wallRS[wallnum2-1])):
            const += (VFC.perp(wallOp[wallnum1-1][i].__dict__['coord' + side1], wallRS[wallnum2-1][j].__dict__['coord' + side2]))
        VF['FW' + wn1 + 'Op' + str(i+1) + 'W' + wn2 + 'RS'] = const
    #Wall Op to Wall Op
    for i  in range (len(wallOp[wallnum1-1])):
        for j in range(len(wallOp[wallnum2-1])):
            VF['FW' + wn1 + 'Op' + str(i+1) + 'W' + wn2 + 'Op' + str(j+1)]  = (VFC.perp(wallOp[wallnum1-1][i].__dict__['coord' + side1], wallOp[wallnum2-1][j].__dict__['coord' + side2]))

        
    return(VF)