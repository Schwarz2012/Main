#List merge
def merge(a):
    m = 0
    for i in range(len(a)):
        m += sum(a[i])
    return(m)

#EPS calculations
def eps(a, b):
    c = 1/a + 1/b - 1
    return(c)

#Area calculations
def area(wallnum, wall, wallRS, wallOp):
    S = wall[wallnum-1].area
    for i in range(len(wallRS[wallnum-1])):
        S -= wallRS[wallnum-1][i].area
    for j in range(len(wallOp[wallnum-1])):
        S -= wallOp[wallnum-1][j].area
    return(S)


def areacf(surface, surfaceRS):
    S = surface.area
    for i in range(len(surfaceRS)):
        S -= surfaceRS[i].area

    return(S)

#Values variables
def varnum(x):
    v = list(x.values())
    vlast = list(v[6].values())
    v.pop()
    v = v + vlast
    return(v)

#Keys variables
def varkey(x):
    v = list(x.keys())
    v.pop()
    for i in range(len(list(x['TwOpi'].values()))):
        v.append(str(list(x['TwOpi'].values())[i]))
    return(v)

def parsum(listdict, key):
    sum = 0
    for i in range(len(listdict)):
        sum += listdict[i].__dict__[key]
    return(sum)