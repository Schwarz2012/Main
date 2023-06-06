import Operations as oper #Additional operations and equations

def walltowall(wallnum1, wallnum2, wallRS, wallOp, wtw):
    w1 = str(wallnum1)
    w2 = str(wallnum2)
    VF = {}
    #Walls 2 RS to Walls 1
    const = wtw[w1 + w2]['FW' + w1 + 'W' + w2 + 'RS']
    for i  in range (len(wallRS[wallnum1 - 1])):
        for j in range(len(wallRS[wallnum2 - 1])):
            const -= wtw[w1 + w2]['FW' + w1 + 'RS' + str(i+1) + 'W' + w2 +'RS' + str(j+1)]
    for i  in range (len(wallOp[wallnum1-1])):
        if len(wallRS[wallnum2 - 1]) != 0:
            const -= wtw[w1 + w2]['FW' + w1 + 'Op' + str(i+1) + 'W' + w2 + 'RS']
    VF['FW' + w1 + 'W' + w2 + 'RS'] = const 

    #Walls to Walls
    const = wtw[w1 + w2]['FW' + w1 + 'W' + w2] - wtw[w1 + w2]['FW' + w1 + 'RS' + 'W' + w2 ] 
    for i in range(len(wallOp[wallnum1-1])):
        const -= (wtw[w1 + w2]['FW' + w1 + 'Op' + str(i+1) + 'W' + w2 ]) 
    const -= VF['FW' + w1 + 'W' + w2 + 'RS']
    VF['FW' + w1 + 'W' + w2] = const                                                      
   
    return(VF)

