from Agents import *
from utilties import *
from graphics import *
import pickle
from GameRun import *
from utilties import *
from options import *
from ParallelRLEvaluator import *
import multiprocessing
import time

def ExperimentRun(paramters_list):
    """
    This will encapculate the run of one only. In a normal experiment, this function will have to run for n number of
    times in order to get a statistical sample to do analyzes on.
    :return:
    """
    paramters_list.reverse()
    experimentNumber=paramters_list.pop()
    primitiveAction=paramters_list.pop()
    optionsEnabled=paramters_list.pop()
    loadOptions=paramters_list.pop()
    mapName=paramters_list.pop()
    FixedStart=paramters_list.pop()
    assert (type(experimentNumber) is int)
    assert (type(primitiveAction) is list)
    assert (type(optionsEnabled) is bool)
    assert (type(loadOptions) is bool)
    assert (type(mapName) is str)
    assert (type(FixedStart) is bool)
    t0 = time.time()
    experimentConfigName = "optionsEnabled_"+str(optionsEnabled)+\
                           "_loadOptions_"+str(loadOptions)+"_mapName_"+mapName+"_FixedStart_"+str(FixedStart)+"_experimentNumber_"+str(experimentNumber)
    print experimentConfigName, " --> Started"
    primitive_actions = primitiveAction
    # primitive_actions = ['LEFT', 'RIGHT', 'UP', 'DOWN']
    # primitive_actions = ['RIGHT'] #to test the current reward system
    # options_enabled = False
    # options_enabled = True
    options_enabled = optionsEnabled
    gameDomain = Domain()
    map_name = mapName
    # map_name = "TestMap2"
    # map_name = "TestMap3"
    gameDomain.loadGameBoad(map_name)
    finalGoal = gameDomain.getGoal()
    loadOptions = loadOptions
    # loadOptions = True
    # loadOptions = False
    options_list = []
    options_parameters_list = []
    if options_enabled:
        if not loadOptions:
            goalsHash = gameDomain.getSubGoals()
            option_index = 0
            for goal in goalsHash: #In this case, I will generate 2 options for each goal (1 for each area)
                for eachArea in goalsHash[goal]:
                    # option_x = Options(goalPosition=goal, area_number=eachArea, LearningAgent=QLearnAgent) #The QLearnAgent is un-updated. Use QLearnAgentWithOptions, which is more robust now
                    option_x = Options(goalPosition=goal, area_number=eachArea, LearningAgent=QLearnAgentWithOptions)
                    QTableFileName_option = 'TRAINED_OPTION_AREA_'+str(eachArea)+'_GOAL_' + str(goal[0]) + '_' + str(goal[1])
                    options_parameters_list.append([option_x, primitive_actions, gameDomain, QTableFileName_option, goal, RLOptions_Parameters, True, False, True])
                    # options_parameters_list.append([option_x, primitive_actions, gameDomain, QTableFileName_option, goal, RLOptions_Parameters, True, True])

    if options_enabled:
        if loadOptions:
                with open("OptionsList.pkl", 'r') as f:
                    options_list = pickle.load(f)
        else:
            options_list = RLOptionTrain(OptionsParam=options_parameters_list, parallel=True)
            with open("OptionsList.pkl", 'w') as f:
                pickle.dump(options_list, f)

        # This is the for testing the options
        # queue = RLOptionsTest(options_list, TestNum=100, parallel=True)
        # DrawSuccessRate(queue, gameDomain.gameMap)

    TrainName = "TrainTotalPolicy_"+str(options_enabled)+"_"+map_name
    gameRunInst = GameRun()
    gameRunInst.run(LearningAgentClass=QLearnAgentWithOptions, ActionsList=primitive_actions+options_list, gameDomain=gameDomain,
                    QTableFileName=TrainName, FinalGoal=finalGoal, RL_Parameters=RLMain_Parameters, train=True, Draw=True,
                    FixedStart=FixedStart, experimentConfigName=experimentConfigName)
    # gameRunInst.run(LearningAgentClass=QLearnAgentWithOptions, ActionsList=primitive_actions, gameDomain=gameDomain,
    #                 QTableFileName="TrainedTotalPolicy", FinalGoal=finalGoal, RL_Parameters=RLMain_Parameters, train=True, Draw=True)

    # gameRunInst.run(LearningAgentClass=QLearnAgent, ActionsList=primitive_actions, gameDomain=gameDomain,
    #                 QTableFileName="TrainedTotalPolicy", FinalGoal=finalGoal, RL_Parameters=RLMain_Parameters, train=True, Draw=True)
    t1 = time.time() - t0
    print experimentConfigName, " --> ENDED, with time: ", t0
    del gameDomain
    del gameRunInst

######################
# This is the main code for the experiment
# I should make this method work in parallel
######################
configurationToTest = {
    "NumberOfExperiments": 30,
    "optionsEnabled": [False, True],
    "loadOptions": [True],
    "mapName": ["TestMap2", "TestMap3"],
    "FixedStart": [True, False],
    "primitiveActions": [['LEFT', 'RIGHT', 'UP', 'DOWN']],  # This is a list of lists. Each list is the set of primitive actions to use
}
# ExperimentRun(optionsEnabled=False)
paramters_list = []
for NumberOfExperiments in range(configurationToTest["NumberOfExperiments"]):
    for optionsEnabled in configurationToTest["optionsEnabled"]:
        for loadOptions in configurationToTest["loadOptions"]:
            for mapName in configurationToTest["mapName"]:
                for FixedStart in configurationToTest["FixedStart"]:
                    for primitiveActions in configurationToTest["primitiveActions"]:
                        # ExperimentRun(experimentNumber=NumberOfExperiments,
                        #               primitiveAction=['LEFT', 'RIGHT', 'UP', 'DOWN'],
                        #               optionsEnabled=optionsEnabled,
                        #               loadOptions=loadOptions,
                        #               mapName=mapName,
                        #               FixedStart=FixedStart)
                        paramters_list.append([NumberOfExperiments, primitiveActions, optionsEnabled, loadOptions, mapName, FixedStart])


pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
# pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()/3)
pool.map(ExperimentRun, paramters_list)
# map(ExperimentRun, paramters_list)