import ComputeMatrix
import statistics

import numpy as np
import matplotlib.pyplot as plt


def searchCliff(mat, act, folder, model, name, function, idxTest=None):
    matSim = ComputeMatrix.computeSimilarity(mat, function)
    matDif = ComputeMatrix.computeSimilarityAct(act)

    x = []
    y = []

    for idx in matSim:
        x.append(matSim[idx])
        y.append(matDif[idx])

    thr_x = statistics.mean(x) + (2 * statistics.stdev(x))

    [uncertainty, hops, cliffs, smooth], cliffSet, cliffSetBetween = getPercentes(thr_x, matSim, matDif, idxTest)
    uncertainty /= len(matSim)
    hops /= len(matSim)
    smooth /= len(matSim)
    cliffs /= len(matSim)
    title = "uncertainty={:.2f}".format(uncertainty) + "," + "hops={:.2f}".format(hops) + "\n" + "smooth={:.2f}".format(
        smooth) + "," + "cliffs={:.2f}".format(cliffs)

    print(title)

    printCliff(x, y, thr_x, 2, folder, model, name, function, cliffSet, cliffSetBetween, title)
    printBox(x, y, folder, model, name, function)

    printBoxActividad(act, folder, model, name, function)


def getPercentes(thr_x, matSim, matDif, idxTest=None):
    thr_y = 2

    uncertainty = 0
    cliffs = 0
    smooth = 0
    hops = 0
    setCliffIds = dict()
    setCliffValues = set()
    setCliffValuesTest = set()
    for xKey in matSim:
        xV = matSim[xKey]
        yV = matDif[xKey]
        area = determineArea(xV, yV, thr_x, thr_y)
        if (area == "cliff"):
            cliffs += 1
            # print(str(xKey[0])+"\t"+str(xKey[1]))
            # if(xKey[0]=="56.0" or xKey[1]=="56.0"):
            print(str(xKey[0]) + "\t" + str(xKey[1]) + "\t" + str(xV) + "\t" + str(yV))

            if (float(xKey[0]) in setCliffIds.keys()):
                setCliffIds[float(xKey[0])] = setCliffIds[float(xKey[0])] + 1
            else:
                setCliffIds[float(xKey[0])] = 1
            if (float(xKey[1]) in setCliffIds.keys()):
                setCliffIds[float(xKey[1])] = setCliffIds[float(xKey[1])] + 1
            else:
                setCliffIds[float(xKey[1])] = 1

            if (float(xKey[0]) in idxTest and not (float(xKey[1]) in idxTest)):
                setCliffValues.add((xV, yV))
            if (float(xKey[1]) in idxTest and not (float(xKey[0]) in idxTest)):
                setCliffValues.add((xV, yV))
            if (float(xKey[1]) in idxTest and (float(xKey[0]) in idxTest)):
                setCliffValuesTest.add((xV, yV))
        elif area == "uncertainty":
            uncertainty += 1

        elif area == "hop":
            hops += 1
        else:
            smooth += 1

    setCliffIds = {k: v for k, v in sorted(setCliffIds.items(), key=lambda item: item[1], reverse=True)}

    print("cant")
    for i in setCliffIds.items():
        print(str(i[0]) + "\t" + str(i[1]))
    return [uncertainty * 100, hops * 100, cliffs * 100, smooth * 100], setCliffValues, setCliffValuesTest


def determineArea(x, y, thr_x, thr_y):
    if x >= thr_x and y >= thr_y:
        return "cliff"
    elif (x < thr_x and y >= thr_y):
        return "uncertainty"
    elif (x < thr_x and y < thr_y):
        return "hop"
    else:
        "smooth"


def printCliff(x, y, thr_x, thr_y, folder, model, name, function, cliffSet, cliffSetBetween, title):
    fig, ax = plt.subplots()
    plt.scatter(x=x, y=y)

    xCliffTest = []
    yCliffTest = []
    for i in cliffSet:
        xCliffTest.append(i[0])
        yCliffTest.append(i[1])
    plt.scatter(xCliffTest, yCliffTest, c="red")

    xCliffTest = []
    yCliffTest = []
    for i in cliffSetBetween:
        xCliffTest.append(i[0])
        yCliffTest.append(i[1])
    plt.scatter(xCliffTest, yCliffTest, c="green")

    point_in_x = np.arange(0, max(x) + 0.1, 0.1)
    point_in_y = np.arange(0, max(y) + 0.1, 0.1)

    plt.title(title)
    plt.plot(point_in_x, [thr_y] * len(point_in_x), color="red")
    plt.plot([thr_x] * len(point_in_y), point_in_y, color="red")
    ax.set_xlabel(f'Similarity({function})')
    ax.set_ylabel(r'$\Delta$(Act)')
    plt.savefig(f'{folder}/{model}/cliff_{model}_{name}_{function}.png')
    plt.show()


def printBox(x, y, folder, model, name, function):
    fig1, ax1 = plt.subplots()
    data = [x, y]
    plt.boxplot(data)
    plt.xticks([1, 2], [f'Similarity({function})', "act"])
    plt.savefig(f'{folder}/{model}/boxplot_{model}_{name}_{function}.png')
    plt.show()


def printBoxActividad(y, folder, model, name, function):
    fig1, ax1 = plt.subplots()
    data = [list(y.values())]
    box = plt.boxplot(data)
    plt.xticks([1], ["act"])
    make_labels(ax1, box)
    plt.savefig(f'{folder}/{model}/boxplot_act_{model}_{name}_{function}.png')
    plt.show()


def make_labels(ax, boxplot):
    # Grab the relevant Line2D instances from the boxplot dictionary
    iqr = boxplot['boxes'][0]
    caps = boxplot['caps']
    med = boxplot['medians'][0]
    fly = boxplot['fliers'][0]

    # The x position of the median line
    xpos = med.get_xdata()

    # Lets make the text have a horizontal offset which is some
    # fraction of the width of the box
    xoff = 0.10 * (xpos[1] - xpos[0])

    # The x position of the labels
    xlabel = xpos[1] + xoff

    # The median is the y-position of the median line
    median = med.get_ydata()[1]

    # The 25th and 75th percentiles are found from the
    # top and bottom (max and min) of the box
    pc25 = iqr.get_ydata().min()
    pc75 = iqr.get_ydata().max()

    # The caps give the vertical position of the ends of the whiskers
    capbottom = caps[0].get_ydata()[0]
    captop = caps[1].get_ydata()[0]

    # Make some labels on the figure using the values derived above
    ax.text(xlabel, median,
            'Median = {:6.3g}'.format(median), va='center')
    ax.text(xlabel, pc25,
            '25th percentile = {:6.3g}'.format(pc25), va='center')
    ax.text(xlabel, pc75,
            '75th percentile = {:6.3g}'.format(pc75), va='center')
    ax.text(xlabel, capbottom,
            'Bottom cap = {:6.3g}'.format(capbottom), va='center')
    ax.text(xlabel, captop,
            'Top cap = {:6.3g}'.format(captop), va='center')

    # Many fliers, so we loop over them and create a label for each one
    for flier in fly.get_ydata():
        ax.text(1 + xoff, flier,
                'outlier = {:6.3g}'.format(flier), va='center')
