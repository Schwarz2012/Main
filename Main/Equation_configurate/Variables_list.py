from numbers import Real
from symtable import Symbol
import numpy
import scipy
import sympy

def variables(wallOp):
    Twi = {}
    for i in range(1,5,1):
        Twi[i] = sympy.Symbol('Twi' + str(i), real=True, positive=True)
    Tfi = sympy.Symbol('Tfi', real=True, positive=True)
    Tci = sympy.Symbol('Tci', real=True, positive=True)
    TwOpi = {}
    for i in range(len(wallOp)):
        for j in range(len(wallOp[i])):
            TwOpi[str(i+1) + str(j+1)] = sympy.Symbol('Tw' + str(i+1) + 'Op' + str(j+1), real=True, positive=True)
    return({'Twi1':Twi[1], 'Twi2':Twi[2], 'Twi3':Twi[3], 'Twi4':Twi[4], 'Tfi':Tfi, 'Tci':Tci, 'TwOpi':TwOpi})