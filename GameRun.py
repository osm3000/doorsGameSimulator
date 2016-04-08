from Agents import *
from utilties import *
from graphics import *
import pickle
from OnlinePlotUility import *
from options import *
import copy

class RLMain_Parameters:
    maxSteps = 100
    maxEpisodes = 20

class RLOptions_Parameters:
    maxSteps = 1000
    maxEpisodes = 200

class GameRun:
    def run(self, LearningAgentClass, ActionsList, gameDomain, QTableFileName, FinalGoal, RL_Parameters, AreaNumber=None, train=True, Draw=False):
        gameDomain.setGoal(FinalGoal)
        gameDomain.initialSet(AreaNumber)
        goal = gameDomain.gameGoal
        gameAgent = LearningAgentClass(actions=ActionsList)
        gameState = GameState()
        gameState = gameDomain.ReadyState()
        if train == False:
            with open(QTableFileName, 'r') as f:
                gameAgent.q = pickle.load(f)

        if Draw:
            QValueHeatMap = QValueOnlinePlot(figureName=QTableFileName, gameState=gameState)

        for episode in range(RL_Parameters.maxEpisodes):
            steps = 0
            print gameDomain.initRobot(), "\t", AreaNumber, "\t", gameDomain.gameGoal
            # gameDomain.initRobotFIXED()
            gameState = gameDomain.ReadyState()
            prevGameState = GameState()
            gameLogic = GameLogic()
            while True:
                # print gameState
                # if Draw:
                    # ConsoleDraw(gameState)
                prevGameState.Copy(gameState)
                gameState = gameLogic.update(gameState, gameAgent)
                steps += gameState.steps
                # print gameState
                # if Draw:
                #     print gameState

                if gameState.win:
                    # if Draw:
                        # ConsoleDraw(gameState)
                        # QValueHeatMap.Draw(gameState=gameState, MaxQvalue=gameAgent.returnLastMaxQ())

                    print "Great Winnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn!!"
                    try:
                        if train:
                            gameAgent.learn(state1=tuple(prevGameState.robotPosition), action1=gameState.lastAction,
                                            state2=tuple(gameState.robotPosition), reward=gameState.reward)
                    except:
                        pass
                    break

                try:
                    if train:
                        gameAgent.learn(state1=tuple(prevGameState.robotPosition), action1=gameState.lastAction,
                                        state2=tuple(gameState.robotPosition), reward=gameState.reward)
                except:
                    pass
                if steps >= RL_Parameters.maxSteps:
                    break
            if not train:
                break
            if Draw:
                QValueHeatMap.Draw(MaxQvalue=gameAgent.returnLastMaxQ())
            print "Episode number : ", episode

        if train:
            with open(QTableFileName, 'w') as f:
                pickle.dump(gameAgent.q, f)

            # for item in gameAgent.q:
            #     print item, " ==== ", gameAgent.q[item]
        if Draw:
            QValueHeatMap.EndDraw()
        return gameAgent, gameDomain.empty_poses, gameState # It will return the agent after it has learned how to do the task well.
        # This can be used for other purposes.

