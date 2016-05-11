import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import matplotlib as mpl
import copy
import warnings
from sklearn import preprocessing
import datetime
import os


timeStamp = 'Results_{:%Y-%m-%d_%H:%M:%S}'.format(datetime.datetime.now())
if not os.path.exists(timeStamp):
    os.makedirs(timeStamp)

def QValueDraw(figureName, gameState, MaxQvalue, episode_num=0, experimentConfigName=""):
    global timeStamp
    plt.figure(figureName)
    plt.title("Achieving Goal: " + str(gameState.gameGoal) + "_episode=" + str(episode_num))
    heatMapArray = np.zeros((gameState.boardDim[0], gameState.boardDim[1]))

    try:
        for state in MaxQvalue:
            heatMapArray[state[0], state[1]] = MaxQvalue[state]
            # print state, " -- Value = ", MaxQvalue[state]
        # exit()
    except TypeError:
        warnings.warn("MaxQvalue returns a single float value, instead of a hashtable!!", UserWarning)


    # I want to scale the matrix here to be between -1 and +1, in order to ease the drawing
    # min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1, 1))
    # heatMapArray = min_max_scaler.fit_transform(heatMapArray)
    ############################################
    # This addition is to insert the robot last place in the map
    # heatmap = plt.pcolor(heatMapArray)
    x, y = gameState.robotPosition
    # print "final position = ", x,y
    plt.text(y, x, "R", horizontalalignment='center', verticalalignment='center')
    x, y = gameState.InitialPosition
    plt.text(y, x, "I", horizontalalignment='center', verticalalignment='center')

    # print "Initial Position position = ", gameState.InitialPosition
    ############################################
    plt.imshow(heatMapArray, interpolation='nearest')#, norm=norm)
    plt.colorbar(ticks=[0, 50, 100])
    # plt.colorbar(heatmap)
    plt.grid(True)
    imagePath = "./"+timeStamp+"/"+experimentConfigName+"/images/"
    if not os.path.exists(imagePath):
        os.makedirs(imagePath)
    plt.savefig(imagePath+figureName + '.png')
    # plt.show()
    plt.close()

    # np.savetxt(imagePath+figureName+"_HeatMap.txt", heatMapArray.round(decimals=3)) # No need for this anymore
