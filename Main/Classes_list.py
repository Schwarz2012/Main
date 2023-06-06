#Classes for all structurers, radiant surfaces and oppenings. Include main phys parametres and coordinates to calculate view factors


class Ceiling:
    def __init__(self, eps, U, Tex, RL, RW):
        self.eps = eps
        self.U = U/(1-U*0.17)
        self.Tex = Tex + 273.15
        self.area = RL*RW 
        self.coord1 = [0, RL, 0, RW]
        self.coord2 = [0, RW, 0, RL]
        self.coord3 = [0, RL, 0, RW]
        self.coord4 = [0, RW, 0, RL]

class CeilingRS:
    def __init__(self, eps, TRS, coord, RL, RW):
        self.eps = eps
        self.TRS = TRS + 273.15
        self.area = coord[1]*coord[3]
        # F - floor, 1,2,3,4 - walls number 
        self.coordF = [coord[0], coord[1] + coord[0], coord[2], coord[3] + coord[2]]
        self.coord1 = [coord[2], coord[2] + coord[3], coord[0], coord[1] + coord[0]]
        self.coord2 = [coord[0], coord[1] + coord[0], RL - coord[2] - coord[3], RL - coord[2]]
        self.coord3 = [RL - coord[2] - coord[3], RL - coord[2], RW - coord[0] - coord[1], RW - coord[0]]
        self.coord4 = [RW - coord[0] - coord[1], RW - coord[0], coord[2], coord[3] + coord[2]]

class Floor:
    def __init__(self, eps, U, Tex, RL, RW):
        self.eps = eps
        self.U = U/(1-U*0.1)
        self.Tex = Tex + 273.15
        self.area = RL*RW 
        self.coord1 = [0, RL, 0, RW]
        self.coord2 = [0, RW, 0, RL]
        self.coord3 = [0, RL, 0, RW]
        self.coord4 = [0, RW, 0, RL]

class FloorRS:
    def __init__(self, eps, TRS, coord, RL, RW):
        self.eps = eps
        self.TRS = TRS + 273.15
        self.area = coord[1]*coord[3]
        # F - floor, 1,2,3,4 - walls number 
        self.coordF = [coord[0], coord[1]+coord[0], coord[2], coord[3]+coord[2]]
        self.coord1 = [coord[2], coord[2] + coord[3], coord[0], coord[1] + coord[0]]
        self.coord2 = [coord[0], coord[1] + coord[0], RL - coord[2] - coord[3], RL - coord[2]]
        self.coord3 = [RL - coord[2] - coord[3], RL - coord[2], RW - coord[0] - coord[1], RW - coord[0]]
        self.coord4 = [RW - coord[0] - coord[1], RW - coord[0], coord[2], coord[3] + coord[2]]

class Walls:
    def __init__(self, eps, U, Tex, RH, RW):
        self.eps = eps
        self.U = U/(1-U*0.13)
        self.Tex = Tex + 273.15
        self.area = RH*RW 
        self.coord = [0, RH, 0, RW]
        self.coordCF = [0, RW, 0, RH]

class WallRS:
    def __init__(self, eps, TRS, coord, R, RH):
        self.eps = eps
        self.TRS = TRS + 273.15
        self.area = coord[1]*coord[3]
        # UP - to ceiling, L - to left wall, R - to right wall, D - to floor, OP - opposite, OPrev - reverse opposit
        self.coordUP = [coord[0], coord[0] + coord[1], RH - coord[2] - coord[3], RH - coord[2]]
        self.coordL = [coord[2], coord[2] + coord[3], coord[0], coord[1] + coord[0]]        
        self.coordR = [coord[2], coord[2] + coord[3], R - coord[0] - coord[1], R - coord[0]]
        self.coordD = [coord[0], coord[0] + coord[1], coord[2], coord[2] + coord[3]]
        self.coordOP = [coord[0], coord[0] + coord[1], coord[2], coord[2] + coord[3]]
        self.coordOPrev = [R - coord[0] - coord[1], R - coord[0], coord[2], coord[2] + coord[3]]

class WallOp:
    def __init__(self, eps, U, Tout, coord, R, RH):
        self.eps = eps
        self.Tex = Tout + 273.15
        self.U = U/(1-U*0.13)
        self.area = coord[1]*coord[3]
        # UP - to ceiling, L - to left wall, R - to right wall, D - to floor, OP - opposite, OPrev - reverse opposit 
        self.coordUP = [coord[0], coord[0] + coord[1], RH - coord[2] - coord[3], RH - coord[2]]
        self.coordL = [coord[2], coord[2] + coord[3], coord[0], coord[1] + coord[0]]        
        self.coordR = [coord[2], coord[2] + coord[3], R - coord[0] - coord[1], R - coord[0]]
        self.coordD = [coord[0], coord[0] + coord[1], coord[2], coord[2] + coord[3]]
        self.coordOP = [coord[0], coord[0] + coord[1], coord[2], coord[2] + coord[3]]
        self.coordOPrev = [R - coord[0] - coord[1], R - coord[0], coord[2], coord[2] + coord[3]]