from Agents import *
from utilties import *
from graphics import *
import pickle
from OnlinePlotUility import *
from options import *
import copy

class RLMain_Parameters:
    maxSteps = 1000
    maxEpisodes = 500
    # maxEpisodes = 10
    # maxEpisodes = 4

class RLOptions_Parameters:
    maxSteps = 1000
    maxEpisodes = 1000

class RLTestParameters:
    maxSteps = 1000
    maxEpisodes = 1

class GameRun:
    def run(self, LearningAgentClass, ActionsList, gameDomain, QTableFileName, FinalGoal, RL_Parameters,
            AreaNumber=None, train=True, Draw=False, AgentGiven=False, FixedStart=False, experimentConfigName=""):

        filePath = "./"+timeStamp+"/"+experimentConfigName+".txt"
        logFile = open(filePath, "w")

        gameDomain.setGoal(FinalGoal)
        gameDomain.initialSet(AreaNumber)
        # goal = gameDomain.gameGoal
        # gameAgent = LearningAgentClass(actions=ActionsList)
        # gameState = GameState()
        gameState = gameDomain.ReadyState()

        if AgentGiven:
            gameAgent = LearningAgentClass
        else:
            gameAgent = LearningAgentClass(actions=ActionsList, finalGoal=FinalGoal)

        robot_init_pos = None
        image_num = 0 # I need to number the image in a sequence in order to make the movie!
        for episode in range(RL_Parameters.maxEpisodes):
            steps = -1
            # robot_init_pos = gameDomain.initRobot()
            if FixedStart:
                robot_init_pos = gameDomain.initRobotFIXED()
            else:
                robot_init_pos = gameDomain.initRobot()
            if Draw:
                print >> logFile, robot_init_pos, "\t", AreaNumber, "\t", gameDomain.gameGoal
            gameState = gameDomain.ReadyState()
            gameState.InitialPosition = robot_init_pos
            prevGameState = GameState()
            gameLogic = GameLogic2(PrimitiveActions=['LEFT', 'RIGHT', 'UP', 'DOWN']) # Test the new modular and enhanced GameLogic2
            while True:
                prevGameState.Copy(gameState)
                # gameState = gameLogic.update(gameState, gameAgent)
                gameState = gameLogic.update2(gameState, gameAgent)
                steps += 1

                if gameState.win: # I think this condition is wrong. The game should stop when there is no further actions. This should be declared by the game logic.
                    # print "Episode : ", episode ," -- Great Winnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn!!"
                    if train:
                        try:
                            gameAgent.learn(state1=tuple(prevGameState.robotPosition), action1=gameState.lastAction,
                                            state2=tuple(gameState.robotPosition), reward=prevGameState.reward, timesteps=gameState.steps-prevGameState.steps, finalGoal=FinalGoal)
                        except:
                            pass
                    ####################################
                    # lastMaxQ = gameAgent.returnLastMaxQ()
                    # for item in lastMaxQ:
                    #     print item, " -- ", lastMaxQ[item]
                    # exit()
                    ####################################
                    # exit()
                    break

                if train:
                    try:
                        # gameAgent.learn(state1=tuple(prevGameState.robotPosition), action1=gameState.lastAction,
                        #                 state2=tuple(gameState.robotPosition), reward=gameState.reward, timesteps=gameState.steps)
                        gameAgent.learn(state1=tuple(prevGameState.robotPosition), action1=gameState.lastAction,
                                        state2=tuple(gameState.robotPosition), reward=prevGameState.reward, timesteps=gameState.steps-prevGameState.steps, finalGoal=FinalGoal)
                    except:
                        pass
                if steps >= RL_Parameters.maxSteps:
                    # print "steps = ", steps
                    break

                # print "Current gameState :\n", gameState
                # print "\nCurrent prevGameState :\n", prevGameState
            if Draw:
                print >> logFile, "Episode = ", episode
                #print "Current gameState :\n", gameState
                print >> logFile, gameState
                print >> logFile, "========================================================================"
                image_num += 1
                QValueDraw(figureName=QTableFileName+"_imageNum_"+str(image_num),
                           gameState=prevGameState,
                           MaxQvalue=gameAgent.returnLastMaxQ(),
                           episode_num=episode,
                           experimentConfigName=experimentConfigName)
        logFile.close()
        return gameAgent, gameDomain.empty_poses, gameState, robot_init_pos # It will return the agent after it has learned how to do the task well.
        # This can be used for other purposes.

