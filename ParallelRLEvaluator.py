import multiprocessing
import os
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
# import MusicPlay


def TrainOneOptionWorker(OptionParameter):
    FixedStart = OptionParameter.pop()
    Draw = OptionParameter.pop()
    Train = OptionParameter.pop()
    RLOptions_Parameters = OptionParameter.pop()
    goal = OptionParameter.pop()
    QTableFileName_option = OptionParameter.pop()
    gameDomain = OptionParameter.pop()
    primitive_actions = OptionParameter.pop()
    option = OptionParameter.pop()
    print option
    option.TrainPolicy(ActionsList=primitive_actions, gameDomain=gameDomain,
                         QTableFileName=QTableFileName_option, FinalGoal=goal, RL_Parameters=RLOptions_Parameters,
                         train=Train, Draw=Draw, FixedStart=FixedStart)
    return option

def RLOptionTrain(OptionsParam=[], parallel=True): # The options parameters is a list of lists
    t0 = time.time()
    if parallel:
        pool = multiprocessing.Pool(processes=3)
        MultiProcessingResultsQueue = pool.map(TrainOneOptionWorker, OptionsParam)
    else:
        MultiProcessingResultsQueue = map(TrainOneOptionWorker, OptionsParam)

    t1 = time.time() - t0
    print "Total Training time = ", t1
    return MultiProcessingResultsQueue

def RunOneOption(OptionClass):
    gameWin,robotInitPos = OptionClass.PlayOption()
    return [OptionClass, gameWin, robotInitPos]

def RLOptionsTest(RLOptionsList, TestNum=1, parallel=True):
    # Repeat every test in the number of TestNum
    final_test_array = list(np.repeat(RLOptionsList, TestNum))

    t0 = time.time()
    if parallel:
        pool = multiprocessing.Pool(processes=3)
        MultiProcessingResultsQueue = pool.map(RunOneOption, final_test_array)
    else:
        MultiProcessingResultsQueue = map(RunOneOption, final_test_array)

    t1 = time.time() - t0
    print "Total Testing time = ", t1
    return MultiProcessingResultsQueue

def DrawSuccessRate(ResultsQueue, GameMap):
    results_hash = {}
    while len(ResultsQueue) > 0: # I first empty the Queue from any data existing
        item = ResultsQueue.pop()
        try:
            results_hash[item[0]].append([item[1], item[2]])
        except:
            results_hash[item[0]] = [[item[1], item[2]]]

    for image in results_hash:
        heatMapArray = np.ones(np.array(GameMap).shape)
        file_name = image.QTableFileName
        for items in results_hash[image]:
            if items[0]: #There is win in this state
                # heatMapArray[items[1][0], items[1][1]] += 1
                heatMapArray[items[1][0], items[1][1]] = 100
            else:
                heatMapArray[items[1][0], items[1][1]] = 5

        plt.figure(file_name)
        plt.imshow(heatMapArray, interpolation='nearest')#, cmap=cm.cool)
        plt.colorbar(ticks=[-1, 1, 100])
        plt.savefig(file_name + '.png')
        plt.close()

    # music_file = MusicPlay.PlayMusic()
    # music_file.play()