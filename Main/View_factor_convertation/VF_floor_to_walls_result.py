import Operations as oper #Additional operations and equations

def floortowall(wallnum, ftw):
    #Floor radiant surfaces to wall
    FFRSW = sum(ftw['f' + str(wallnum)]['FW' + str(wallnum) + 'FRS']) - oper.merge(ftw['f' + str(wallnum)]['FW' + str(wallnum) + 'RSFRS']) - sum(ftw['f' + str(wallnum)]['FW' + str(wallnum) + 'OpFRS'])
    #Floor radiant surfaces to wall op
    FFRSWOp = ftw['f' + str(wallnum)]['FW' + str(wallnum) + 'OpFRS']
    #Floor to wall
    FFW = ftw['f' + str(wallnum)]['FW' + str(wallnum) + 'F'] - sum(ftw['f' + str(wallnum)]['FW' + str(wallnum) + 'FRS']) - (sum(ftw['f' + str(wallnum)]['FW' + str(wallnum) + 'RSF']) - oper.merge(ftw['f' + str(wallnum)]['FW' + str(wallnum) + 'RSFRS'])) - (sum(ftw['f' + str(wallnum)]['FW' + str(wallnum) + 'OpF']) - sum(ftw['f' + str(wallnum)]['FW' + str(wallnum) + 'OpFRS']))
    #Floor to walls RS
    FFWRS = sum(ftw['f' + str(wallnum)]['FW' + str(wallnum) + 'RSF']) - oper.merge(ftw['f' + str(wallnum)]['FW' + str(wallnum) + 'RSFRS'])
    #Floor to walls Op
    FFWOp = []
    for i in range(len(ftw['f' + str(wallnum)]['FW' + str(wallnum) + 'OpF'])):
        FFWOps = ftw['f' + str(wallnum)]['FW' + str(wallnum) + 'OpF'][i]
        FFWOps -= ftw['f' + str(wallnum)]['FW' + str(wallnum) + 'OpFRS'][i]
        FFWOp.append(FFWOps)
    return({'FFRSW':FFRSW, 'FFRSWOp':FFRSWOp, 'FFW':FFW, 'FFWRS':FFWRS, 'FFWOp':FFWOp})
