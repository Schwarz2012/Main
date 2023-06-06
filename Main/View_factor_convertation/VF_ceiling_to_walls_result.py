import Operations as oper #Additional operations and equations

def ceilingtowall(wallnum, ctw):
    #Ceiling radiant surfaces to wall
    FCRSW = sum(ctw['c' + str(wallnum)]['FW' + str(wallnum) + 'CRS']) - oper.merge(ctw['c' + str(wallnum)]['FW' + str(wallnum) + 'RSCRS']) - sum(ctw['c' + str(wallnum)]['FW' + str(wallnum) + 'OpCRS'])
    #Ceiling radiant surfaces to wall op
    FCRSWOp = ctw['c' + str(wallnum)]['FW' + str(wallnum) + 'OpCRS']
    #Ceiling to wall
    FCW = ctw['c' + str(wallnum)]['FW' + str(wallnum) + 'C'] - sum(ctw['c' + str(wallnum)]['FW' + str(wallnum) + 'CRS']) - (sum(ctw['c' + str(wallnum)]['FW' + str(wallnum) + 'RSC']) - oper.merge(ctw['c' + str(wallnum)]['FW' + str(wallnum) + 'RSCRS'])) - (sum(ctw['c' + str(wallnum)]['FW' + str(wallnum) + 'OpC']) - sum(ctw['c' + str(wallnum)]['FW' + str(wallnum) + 'OpCRS']))
    #Ceiling to walls RS
    FCWRS = sum(ctw['c' + str(wallnum)]['FW' + str(wallnum) + 'RSC']) - oper.merge(ctw['c' + str(wallnum)]['FW' + str(wallnum) + 'RSCRS'])
    #Ceiling to walls Op
    FCWOp = []
    for i in range(len(ctw['c' + str(wallnum)]['FW' + str(wallnum) + 'OpC'])):
        FCWOps = ctw['c' + str(wallnum)]['FW' + str(wallnum) + 'OpC'][i]
        FCWOps -= ctw['c' + str(wallnum)]['FW' + str(wallnum) + 'OpCRS'][i]
        FCWOp.append(FCWOps)
    return({'FCRSW':FCRSW, 'FCRSWOp':FCRSWOp, 'FCW':FCW, 'FCWRS':FCWRS, 'FCWOp':FCWOp})
