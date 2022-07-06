from math import sqrt

def computeTanimoto(rowI,rowJ):
    sum_num = 0
    sum_squI = 0
    sum_squJ = 0
    for k in range(len(rowJ)):
        sum_num += (rowI[k] * rowJ[k])
        sum_squI += (rowI[k] * rowI[k])
        sum_squJ += (rowJ[k] * rowJ[k])
    den = (sum_squI + sum_squJ - sum_num)
    if(sum_num == 0):
        return 0
    value = sum_num / den
    if(value < 0):
        print("salida")
    return value

def euclideanDistance(rowI,rowJ):
    sum = 0
    for k in range(len(rowJ)):
        d = rowI[k] - rowJ[k]
        sum +=(d * d)
    value = sqrt(sum)
    return 1/(1+value)

def manhattanDistance (rowI,rowJ):
    sum = 0
    for i in range(len(rowJ)):
        sum += abs(rowI[i] - rowJ[i])
    return 1/(1+sum)