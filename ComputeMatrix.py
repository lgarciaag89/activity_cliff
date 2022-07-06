from math import fabs
from function import *
def readData(pathCsv):
    fCsv = open(pathCsv, "r")

    mat = dict()
    act = dict()
    line = fCsv.readline()
    line = fCsv.readline()

    while (line):
        linS = line.split(",")
        newRow = []
        act[linS[0]] = float(linS[1])
        for x in range(2, len(linS)):
            newRow.append(float(linS[x]))
        line = fCsv.readline()
        mat[linS[0]] = newRow
    fCsv.close()
    return mat, act

def computeSimilarity(mat, function):
    simMat = dict()
    for i in range(len(mat)):
        rowI = mat[list(mat)[i]]
        for j in range(i+1, len(mat)):
            rowJ = mat[list(mat)[j]]
            value = 0
            if(function == "tanimoto"):
                value = computeTanimoto(rowI,rowJ)
            elif(function == "euclidean"):
                value = euclideanDistance(rowI, rowJ)
            elif(function == "manhattan"):
                value = manhattanDistance(rowI, rowJ)
            simMat[(list(mat)[i],list(mat)[j])] = value
    return simMat

def computeSimilarityAct(act):
    simMat = dict()
    for i in range(len(act)):
        valueI = act[list(act)[i]]
        for j in range(i+1, len(act)):
            valuej = act[list(act)[j]]
            value = fabs(valueI-valuej)
            simMat[(list(act)[i],list(act)[j])] = value
    return simMat

def computeNormSimilarityAct(act):
    simMat = dict()
    maxV = max(act.values())
    minV = min(act.values())
    den = maxV-minV
    for i in range(len(act)):
        valueI = act[list(act)[i]]
        for j in range(i+1, len(act)):
            valuej = act[list(act)[j]]
            value = fabs(valueI-valuej)
            value /= den
            simMat[(list(act)[i],list(act)[j])] = 1-value
    return simMat
