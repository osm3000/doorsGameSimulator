"""
Here, I do the implementation of the options. Ya Mosahel :-)
Note: After consideration, the options should be generated before the start of the main RL. They should be parameters
for the main RL. This is how I can make this as modular as possible
"""
from Agents import *
from utilties import *
from GameRun import *


class Options:
    """
    Note: Options will have a time out timer, to make sure they will not work indifintely.
    """

    def __init__(self, area_number, goalPosition, LearningAgent):
        self.area_number = area_number
        self.goalPosition = goalPosition
        self.legalPosition = [goalPosition]
        self.LearningAgentClass = LearningAgent

    def TrainPolicy(self, ActionsList, gameDomain, QTableFileName,
                    FinalGoal, RL_Parameters, train=True, Draw=False):

        gameRunInstOption = GameRun()
        self.LearningAgentClass, self.legalPosition,_ = gameRunInstOption.run(LearningAgentClass=self.LearningAgentClass, ActionsList=ActionsList,
            gameDomain=gameDomain, QTableFileName=QTableFileName, FinalGoal=FinalGoal,
            AreaNumber = self.area_number, RL_Parameters=RL_Parameters,train=train, Draw=Draw)

    # def getAction(self, state):
    #     # print self.LearningAgentClass.q
    #     gameLogicLocal = GameLogic()
    #     gameState = copy.deepcopy(state)
    #     gameState.gameGoal = list(self.goalPosition)
    #     gameState.win = False
    #     #gameState = gameLogicLocal.update(gameState, self.LearningAgentClass)
    #     while not gameState.win:
    #         gameState = gameLogicLocal.update(gameState, self.LearningAgentClass)
    #         print "No win yet!", gameState
    #     print "----------------------------------------------------------------------------------------"
    #     return gameState

    def checkLegality(self, robotPosition):
        # print "Option-",str(self.goalPosition[0])+"-",str(self.goalPosition[1])," - ", self.legalPosition
        robotPosition = list(robotPosition)
        for pos in self.legalPosition:
            if robotPosition == pos:
                print "YES"
                return True
        return False

    def getOptionGoal(self):
        return self.goalPosition
    def __str__(self):
        return 'OPTION_AREA_'+str(self.area_number)+'_GOAL_' + str(self.goalPosition[0]) + '_' + str(self.goalPosition[1])