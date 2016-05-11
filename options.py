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
        self.legalPosition = None
        self.LearningAgentClass = LearningAgent
        self.ActionsList = None
        self.gameDomain = None
        self.QTableFileName = None
        self.FinalGoal = None
        self.RL_Parameters = None

        self.gameRunInstOption = GameRun()

    def TrainPolicy(self, ActionsList, gameDomain, QTableFileName,
                    FinalGoal, RL_Parameters, train=True, Draw=False):

        self.ActionsList = ActionsList
        self.gameDomain = gameDomain
        self.QTableFileName = QTableFileName
        self.FinalGoal = FinalGoal
        self.RL_Parameters = RL_Parameters


        self.LearningAgentClass, self.legalPosition, _ ,robotInitPos = \
            self.gameRunInstOption.run(LearningAgentClass=self.LearningAgentClass, ActionsList=ActionsList,
            gameDomain=gameDomain, QTableFileName=QTableFileName, FinalGoal=FinalGoal,
            AreaNumber = self.area_number, RL_Parameters=RL_Parameters, train=train, Draw=Draw)

    def PlayOption (self):
        """
        This class is made in order to test the option, by starting from random places, and collect some stats about the quality of the
        policy
        :return:
        """
        _, _ , gameState, robotInitPos = \
             self.gameRunInstOption.run(LearningAgentClass=self.LearningAgentClass, ActionsList=self.ActionsList,
            gameDomain=self.gameDomain, QTableFileName=self.QTableFileName, FinalGoal=self.FinalGoal,
            AreaNumber = self.area_number, RL_Parameters=RLTestParameters, train=False, Draw=False, AgentGiven=True)

        return gameState.win, robotInitPos

    def checkLegality(self, robotPosition):
        # print "Option-",str(self.goalPosition[0])+"-",str(self.goalPosition[1])," - ", self.legalPosition
        robotPosition = list(robotPosition)
        for pos in self.legalPosition:
            if robotPosition == pos:
                # print "YES, this Option is legal, ", self.__str__()
                return True
        return False

    def getOptionGoal(self):
        return self.goalPosition

    def getLegalPosition(self):
        return [tuple(q) for q in self.legalPosition]

    def __str__(self):
        return 'OPTION_AREA_'+str(self.area_number)+'_GOAL_' + str(self.goalPosition[0]) + '_' + str(self.goalPosition[1])