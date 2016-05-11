import matplotlib
import matplotlib.pyplot as plt
import sys
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from scipy import stats
matplotlib.use('Agg')

"""
We have N number of runs for X number of configurations.
The input will be the folder containing the reports, and the output will be
comparisons (graphs and statistical significance).
Comparison points

for each map:
    options VS no options in the following conditions: fixedStart (true/false) --> macro and micro

First, we establish a large hash table containing all the data (a separate function), then, I make a high level function
to do the comparisons (in case I want to do extra things in the future).
"""
def buildDataBase(metadataFolderPath):
    database = {}
    fullFilePath = os.getcwd() + '/'+metadataFolderPath+'/'
    onlyfiles = [fullFilePath+f for f in listdir(metadataFolderPath) if isfile(join(metadataFolderPath, f))]
    for file_name in onlyfiles:
        "optionsEnabled_False_loadOptions_True_mapName_TestMap2_FixedStart_True_experimentNumber_19"
        file_name_split = file_name.split("/")[-1].split(".")[0].split("_")
        optionsEnabled = file_name_split[1]
        loadOptions = file_name_split[3] # This will be ignored for now -- IMPORTANT
        mapName = file_name_split[5]
        FixedStart = file_name_split[7]
        experimentNumber = file_name_split[9]
        # databasePath = [mapName, optionsEnabled, FixedStart] # this has to be arranged in the order for the database hierarchy
        if mapName not in database:
            database[mapName] = {}
            database[mapName][optionsEnabled] = {}
            database[mapName][optionsEnabled][FixedStart] = {"micro": [], "macro": [], "avgMacro": [], "avgMicro": []}  # one for micro, one for macro
        elif optionsEnabled not in database[mapName]:
            database[mapName][optionsEnabled] = {}
            database[mapName][optionsEnabled][FixedStart] = {"micro": [], "macro": [], "avgMacro": [], "avgMicro": []}  # one for micro, one for macro
        elif FixedStart not in database[mapName][optionsEnabled]:
            database[mapName][optionsEnabled][FixedStart] = {"micro": [], "macro": [], "avgMacro": [], "avgMicro": []}  # one for micro, one for macro

        with open(file_name, 'r') as currentFile:
            winVector = []
            microstepsVector = []
            macroStepsVector = []
            numEpisodes = 0

            lines = currentFile.read().splitlines()
            newEpisode = False
            for line in lines:
                if "Episode" in line:
                    newEpisode = True
                    numEpisodes += 1
                elif newEpisode:
                    line_split = line.split("=")
                    if "steps" in line_split[0]:
                        microstepsVector.append(int(line_split[1]))
                    elif "macroSteps" in line_split[0]:
                        macroStepsVector.append(int(line_split[1]))
                    elif "win" in line_split[0]:
                        winVector.append(bool(line_split[1]))
                else:
                    newEpisode = False

            database[mapName][optionsEnabled][FixedStart]["micro"].append(microstepsVector)
            database[mapName][optionsEnabled][FixedStart]["macro"].append(macroStepsVector)

    for currentMap in database:
        for optionChoice in database[currentMap]:
            for startChoice in database[currentMap][optionChoice]:
                for micro_macro in database[currentMap][optionChoice][startChoice]:
                    if micro_macro == "micro":
                        database[currentMap][optionChoice][startChoice]["avgMicro"] = \
                            [sum(e)/len(e) for e in zip(*database[currentMap][optionChoice][startChoice][micro_macro])]
                    elif micro_macro == "macro":
                        database[currentMap][optionChoice][startChoice]["avgMacro"] = \
                            [sum(e)/len(e) for e in zip(*database[currentMap][optionChoice][startChoice][micro_macro])]
    return database


# print database["TestMap2"]["True"]["True"]["avgMacro"]
# print database["TestMap2"]["True"]["True"]["avgMicro"]
class EXP0:
    def __init__(self, database):
        self.database = database

    def drawImage(self):
        mico_macro = ["avgMacro", "avgMicro"]


        # Draw the mico comparison first

        for map in database:
            graphLineNames = []
            figureName = "Average_microsteps_comparison_map:"+map
            plt.figure(figureName)
            for option in database[map]:
                for fixedStart in database[map][option]:
                    # print len(database[map][option][fixedStart]["avgMicro"])
                    # print database[map][option][fixedStart]["avgMicro"]
                    plt.plot(range(len(database[map][option][fixedStart]["avgMicro"])), database[map][option][fixedStart]["avgMicro"])
                    graphLine = "options:" + str(option) + ",Fixed:" + str(fixedStart)
                    graphLineNames.append(graphLine)

            plt.legend(graphLineNames)
            plt.grid(True)
            plt.xlabel("Episodes")
            plt.ylabel("Steps per episode")

            plt.savefig(figureName + '.png')
            plt.close()

        for map in database:
            graphLineNames = []
            figureName = "Average_macrosteps_comparison_map:"+map
            plt.figure(figureName)
            for option in database[map]:
                for fixedStart in database[map][option]:
                    # print len(database[map][option][fixedStart]["avgMicro"])
                    # print database[map][option][fixedStart]["avgMicro"]
                    plt.plot(range(len(database[map][option][fixedStart]["avgMacro"])), database[map][option][fixedStart]["avgMacro"])
                    graphLine = "options:" + str(option) + ",Fixed:" + str(fixedStart)
                    graphLineNames.append(graphLine)

            plt.legend(graphLineNames)
            plt.grid(True)
            plt.xlabel("Episodes")
            plt.ylabel("Steps per episode")

            plt.savefig(figureName + '.png')
            plt.close()

database = buildDataBase("meta_reports")
experiment = EXP0(database)
experiment.drawImage()
"""
This is the old code, which takes one run only from each configuration, and make the drawing based on it.
"""
# fileNames = sys.argv[1:]
# mapName = fileNames[0].split("_")[1]
# plt.figure(mapName)
# for i in fileNames:
#     winVector = []
#     microstepsVector = []
#     macroStepsVector = []
#     numEpisodes = 0
#     with open(i, "r") as currentFile:
#         lines = currentFile.read().splitlines()
#         newEpisode = False
#         for line in lines:
#             if "Episode" in line:
#                 newEpisode = True
#                 numEpisodes += 1
#                 dataPoints = 0
#             elif newEpisode:
#                 line_split = line.split("=")
#                 if "steps" in line_split[0]:
#                     microstepsVector.append(int(line_split[1]))
#                 elif "macroSteps" in line_split[0]:
#                     macroStepsVector.append(int(line_split[1]))
#                 elif "win" in line_split[0]:
#                     winVector.append(bool(line_split[1]))
#             else:
#                 newEpisode = False
#
#     episodes = range(1, numEpisodes+1)
#     plt.plot(episodes, microstepsVector)
#     # plt.scatter(episodes, macroStepsVector)
# plt.grid(True)
# plt.xlabel("Episodes")
# plt.ylabel("Steps per episode")
# plt.legend(fileNames)
# plt.show()


