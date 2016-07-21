#Centralization-reduction for a list of values
import numpy as np

from misc import inf

#Hypothesis of uniform probability for the occurrence of any bacteria whatever the clinic data may be (which is a strong hypothesis...)
def expectList(vList):
    n = len(vList)
    if not n:
        print "\n/!\ ERROR: Empty list."
        raise ValueError
    exp = 0
    for i in range(n):
        if vList[i]:
            exp += vList[i]/n
    return exp

def standardDeviationList(vList):
    vProductList = [x*x for x in vList if x]
    expProd = expectList(vProductList)
    exp = expectList(vList)
    expS = exp*exp
    return np.sqrt(expProd-expS),exp

def normalizeList(valueList):
    stDeviation,exp = standardDeviationList(valueList)
    if not stDeviation:
        print "\n/!\ ERROR: Math problem (Division by zero)."
        raise ValueError
    normList = []
    for value in valueList:
        if value:
            normList.append((value-exp)/stDeviation)
    return normList
