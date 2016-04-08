from Agents import *
from utilties import *
from graphics import *
import pickle
from GameRun import *
from utilties import *
from options import *

"""
Ideas:
- I want to be able to train the options in parallel. I think this should be feasible
"""

primitive_actions = ['LEFT', 'RIGHT', 'UP', 'DOWN']
options_enabled = True
gameRunInst = GameRun()
gameDomain = Domain()
# gameDomain.loadGameBoad("test_map_2")
gameDomain.loadGameBoad("test_map_3")
finalGoal = gameDomain.getGoal()
# print finalGoal
loadOptions = True
options_list = []
if options_enabled:
    if not loadOptions:
        goalsHash = gameDomain.getSubGoals()
        # print goalsHash.keys()
        # exit()
        options_list = []
        option_index = 0
        for goal in goalsHash: #In this case, I will generate 2 options for each goal (1 for each area)
            for eachArea in goalsHash[goal]:
                option_x = Options(goalPosition=goal, area_number=eachArea, LearningAgent=QLearnAgent)
                QTableFileName_option = 'TRAINED_OPTION_AREA_'+str(eachArea)+'_GOAL_' + str(goal[0]) + '_' + str(goal[1])
                option_x.TrainPolicy(ActionsList=primitive_actions, gameDomain=gameDomain,
                                     QTableFileName=QTableFileName_option, FinalGoal=goal, RL_Parameters=RLOptions_Parameters,
                                     train=True, Draw=False)
                options_list.append(copy.deepcopy(option_x))
                print "-----------------------------------------------------------------------------------------"
        with open("OptionsList.pkl", 'w') as f:
            pickle.dump(options_list, f)
    else:
        with open("OptionsList.pkl", 'r') as f:
            options_list = pickle.load(f)
# exit()

gameRunInst.run(LearningAgentClass=QLearnAgentWithOptions, ActionsList=primitive_actions+options_list, gameDomain=gameDomain,
                QTableFileName="TrainedTotalPolicy", FinalGoal=finalGoal, RL_Parameters=RLMain_Parameters, train=True, Draw=True)
#
# gameRunInst.run(LearningAgentClass=QLearnAgentWithOptions, ActionsList=options_list, gameDomain=gameDomain,
#                 QTableFileName="TrainedTotalPolicy", FinalGoal=finalGoal, RL_Parameters=RLMain_Parameters, train=True, Draw=True)
