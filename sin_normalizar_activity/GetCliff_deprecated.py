# Press the green button in the gutter to run the script.
import statistics
import numpy as np
import ComputeMatrix
import matplotlib.pyplot as plt

def printCliff(x,y,thr_x,folder,model,name,function,title):
    thr_y = 2
    fig, ax = plt.subplots()
    plt.scatter(x=x, y=y)
    point_in_x = np.arange(0, max(x), 0.1)
    point_in_y = np.arange(min(y), max(y), 0.1)

    plt.title(title)
    plt.plot(point_in_x, [thr_y] * len(point_in_x), color="red")
    plt.plot([thr_x] * len(point_in_y), point_in_y, color="red")
    ax.set_xlabel(f'Similarity({function})')
    ax.set_ylabel(r'$\Delta$Act')
    plt.savefig(f'{folder}/{model}/cliff_{model}_{name}_{function}.png')
    plt.show()

def printBox(x,y,folder,model,name,function):
    fig1, ax1 = plt.subplots()
    data = [x, y]
    plt.boxplot(data)
    plt.xticks([1, 2], [f'Similarity({function})', "act"])
    plt.title("Boxplot Using Matplotlib")
    plt.savefig(f'{folder}/{model}/boxplot_{model}_{name}_{function}.png')
    plt.show()

def getPercentes(thr_x,matSim,matDif,idxTest,opt):

    thr_y = 2

    uncertainty = 0
    cliffs = 0
    smooth = 0
    hops = 0
    # fList = open(f'{folder}/{model}/list_{model}_{name}_{function}', 'w')
    setCliff = dict()
    for xKey in matSim:
        xV = matSim[xKey]
        yV = matDif[xKey]
        area = determineArea(xV,yV,thr_x,thr_y,opt)
        if( area == "cliff"):
            cliffs+=1
            if (float(xKey[0]) in idxTest and not (float(xKey[1]) in idxTest)):
                if (float(xKey[0]) in setCliff.keys()):
                    setCliff[float(xKey[0])] = setCliff[float(xKey[0])] + 1
                else:
                    setCliff[float(xKey[0])] = 1

            if (float(xKey[1]) in idxTest and not (float(xKey[0]) in idxTest)):
                if (float(xKey[1]) in setCliff.keys()):
                    setCliff[float(xKey[1])] = setCliff[float(xKey[1])] + 1
                else:
                    setCliff[float(xKey[1])] = 1
        elif area == "uncertainty":
            uncertainty+=1
        elif area == "hop":
            hops+=1
    #     if xV < thr_x and yV >= thr_y:
    #         # fList.write(f'{xKey[0]},{xKey[1]}' + '\n')
    #         cliffs = cliffs + 1
    #         # print(str(xKey)+" cliff")
    #
    #         if( float(xKey[0]) in idxTest and not(float(xKey[1]) in idxTest)  ):
    #                 if( float(xKey[0]) in setCliff.keys() ):
    #                     setCliff[float(xKey[0])] = setCliff[float(xKey[0])]+1
    #                 else:
    #                     setCliff[float(xKey[0])] = 1
    #
    #         if (float(xKey[1]) in idxTest and not (float(xKey[0]) in idxTest)):
    #             if (float(xKey[1]) in setCliff.keys()):
    #                 setCliff[float(xKey[1])] = setCliff[float(xKey[1])] + 1
    #             else:
    #                 setCliff[float(xKey[1])] = 1
    #
    #         # if (float(xKey[1]) in idxTest and float(xKey[0]) in idxTest):
    #         #     if (float(xKey[1]) in setCliff.keys()):
    #         #         setCliff[float(xKey[1])] = setCliff[float(xKey[1])] + 1
    #         #     else:
    #         #         setCliff[float(xKey[1])] = 1
    #         #     if (float(xKey[0]) in setCliff.keys()):
    #         #         setCliff[float(xKey[0])] = setCliff[float(xKey[0])] + 1
    #         #     else:
    #         #         setCliff[float(xKey[0])] = 1
    #
    #     elif (xV >= thr_x and yV >= thr_y):
    #         uncertainty = uncertainty + 1
    #         # print(str(xKey)+" uncertainty")
    #     elif (xV >= thr_x and yV < thr_y):
    #         hops = hops + 1
    #         # print(str(xKey) + " hops")
    #     else:
    #         smooth = smooth + 1
    #         # print(str(xKey) + " smooth")
    it = setCliff.items()
    print(sorted(it))

    return [uncertainty*100,hops*100,cliffs*100,smooth*100]
    # fList.close()

def searchCliff(mat,act,folder, model, name, function,idxTest,opt):
    matSim = ComputeMatrix.computeSimilarity(mat, function)
    matDif = ComputeMatrix.computeSimilarityAct(act)

    x = []
    y = []

    for idx in matSim:
        x.append(matSim[idx])
        y.append(matDif[idx])

    thr_x = statistics.mean(x)/(2*statistics.stdev(x)) if function == "tanimato" else statistics.quantiles(x)[0]

    [uncertainty, hops, cliffs, smooth] = getPercentes(thr_x, matSim, matDif,idxTest,opt)
    uncertainty /= len(matSim)
    hops /= len(matSim)
    smooth /= len(matSim)
    cliffs /= len(matSim)
    title = "uncertainty={:.2f}".format(uncertainty) + "," + "hops={:.2f}".format(hops) + "\n" + "smooth={:.2f}".format(
        smooth) + "," + "cliffs={:.2f}".format(cliffs)

    print(title)

    printCliff(x, y, thr_x, folder, model, name, function, title)
    printBox(x, y, folder, model, name, function)

def determineArea(x,y,thr_x, thr_y, opt):
    if(opt == 0): # minimize function
        if x < thr_x and y >= thr_y:
            return "cliff"
        elif (x >= thr_x and y >= thr_y):
            return "uncertainty"
        elif (x >= thr_x and y < thr_y):
            return "hop"
        else:
            "smooth"
    else:
        if x >= thr_x and y >= thr_y:
            return "cliff"
        elif (x < thr_x and y >= thr_y):
            return "uncertainty"
        elif (x < thr_x and y < thr_y):
            return "hop"
        else:
            "smooth"
