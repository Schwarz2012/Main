import Operations as oper #Additional operations and equations

def walltoopening(wallnum1, wallnum2, wallOp, wallRS, wtw):
    w1 = str(wallnum1)
    w2 = str(wallnum2)
    VF = {}

    #Wall 2 Op to Wall 1
    for i in range(len(wallOp[wallnum2 - 1])):
        const = wtw[w1 + w2]['FW' + w1 + 'W' + w2 + 'Op' + str(i+1)]
        if len(wallRS[wallnum1-1]) != 0:
            const -= wtw[w1 + w2]['FW' + w1 + 'RSW' + w2 + 'Op' + str(i+1)]
        for j in range(len(wallOp[wallnum1 - 1])):
            const -=wtw[w1 + w2]['FW' + w1 + 'Op' + str(j+1) + 'W' + w2 + 'Op' + str(i+1)]
        VF['FW' + w1 + 'W' + w2 + 'Op' + str(i+1)] = const
    #Walls Op to Walls Op
    for i in range(len(wallOp[wallnum2 - 1])):
        for j in range(len(wallOp[wallnum1 - 1])):
            VF['FW' + w1 + 'Op' + str(j+1) + 'W' + w2 + 'Op' + str(i+1)] = wtw[w1 + w2]['FW' + w1 + 'Op' + str(j+1) + 'W' + w2 + 'Op' + str(i+1)]

    #Walls Op to Walls RS
    for i in range(len(wallOp[wallnum2 - 1])):
        if len(wallRS[wallnum1-1]) != 0:
            VF['FW' + w1 + 'RSW' + w2 + 'Op' + str(i+1)] = wtw[w1 + w2]['FW' + w1 + 'RSW' + w2 + 'Op' + str(i+1)]



    return(VF)
