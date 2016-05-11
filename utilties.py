from options import *
import copy
import random
class GameState:
    def __init__(self):
        self.robotPosition = [None, None]
        self.win = False
        self.gameGoal = [None, None]
        self.reward = 0
        self.gameMap = []
        self.boardDim = [None, None]
        self.steps = 0
        self.lastAction = None
        self.macroSteps = 0
        self.InitialPosition = [None, None]
        self.optionTime = 0 # This will communicate to the agent the trace of the options

    def Copy(self, gameState):
        self.robotPosition = copy.deepcopy(gameState.robotPosition)
        self.win = copy.deepcopy(gameState.win)
        self.gameGoal = copy.deepcopy(gameState.gameGoal)
        self.reward = copy.deepcopy(gameState.reward)
        self.gameMap = copy.deepcopy(gameState.gameMap)
        self.boardDim = copy.deepcopy(gameState.boardDim)
        self.steps = copy.deepcopy(gameState.steps)
        self.lastAction = copy.deepcopy(gameState.lastAction)
        self.macroSteps = copy.deepcopy(gameState.macroSteps)
        self.InitialPosition = copy.deepcopy(gameState.InitialPosition)
        self.optionTime = copy.deepcopy(gameState.optionTime)

    def __str__(self):
        final = "robotPosition = " + str(self.robotPosition) + \
                "\nwin = " + str(self.win) + \
                "\ngameGoal = " + str(self.gameGoal) + \
                "\nreward = " + str(self.reward) + \
                "\nboardDim = " + str(self.boardDim) + \
                "\nsteps = " + str(self.steps) + \
                "\nlastAction = " + str(self.lastAction) + \
                "\nmacroSteps = " + str(self.macroSteps) + \
                "\nInitialPosition = " + str(self.InitialPosition) + \
                "\noptionTime = " + str(self.optionTime) + \
                "\n"
        return final

    def gameStepProgress(self):
        self.steps += 1

    def gameMacroStepProgress(self):
        self.macroSteps += 1

class GameLogic:
    """
    This should be very generic, since I can change the game domain (and hence, the goals of the game)
    """
    def __init__(self):
        self.win = False
        self.robotPosition = [None, None]

    def update(self, gameState, AgentClass):
        """
        The agent will take an action. Here, I want to update the robot position, and see if it reached the
        required goal or not.
        The mechanics of the game will be to stay in your place if you take an illegal action, otherwise you move
        forward
        :return:
        """
        assert (isinstance(gameState, GameState))
        currentAction = AgentClass.getAction(tuple(gameState.robotPosition))
        current_pos = gameState.robotPosition
        temp_pos = current_pos[:]
        tempReward = 0

        optionTimeLength = 0
        if type(currentAction) is str: # A primitive action
            new_pos = temp_pos[:]
            if currentAction == 'LEFT':
                new_pos[1] -= 1
            elif currentAction == 'RIGHT':
                new_pos[1] += 1
            elif currentAction == 'UP':
                new_pos[0] -= 1
            elif currentAction == 'DOWN':
                new_pos[0] += 1

            if self.isLegal(new_pos, gameState):
                if not self.detectWall(new_pos, gameState):
                    temp_pos = new_pos
                    if self.detectGoal(new_pos, gameState):
                        self.win = True
                        gameState.reward = 3.0
                        tempReward += 100
                else:
                    tempReward -= 0.5 #Negative reward for hitting the wall!
                    temp_pos = current_pos
            else:
                temp_pos = current_pos
        # elif isinstance(currentAction, Options):
        else:
            # print "An option has been selected = ", currentAction
            newGameState = GameState()
            newGameState.Copy(gameState)
            # New direction: Here, the option will take control of the execution.
            newGameState.gameGoal = currentAction.getOptionGoal()
            # new_pos = temp_pos[:]
            while not newGameState.win: #The option has to terminate. I can add a random probability/interruption options here in the future as well.
                optionTimeLength += 1
                new_pos = temp_pos[:]
                # print "optionTimeLength = ", optionTimeLength
                if optionTimeLength == 100: # This number is a parameter, to be changed and modified for further testing
                    tempReward -= 0 #Negative reward for hitting the wall!
                    # temp_pos = new_pos[:] # No need for this line, since temp_pos will be already updated at this point
                    break

                actions_option = currentAction.LearningAgentClass.getAction(tuple(newGameState.robotPosition))
                # print "Actions from the option = ", actions_option
                if type(actions_option) is str:
                    # print "From Option : ", currentAction, " - robot position = ", new_pos
                    # print "Legal action from options = ", current_action_OPTION, new_pos
                    if actions_option == 'LEFT':
                        new_pos[1] -= 1
                    elif actions_option == 'RIGHT':
                        new_pos[1] += 1
                    elif actions_option == 'UP':
                        new_pos[0] -= 1
                    elif actions_option == 'DOWN':
                        new_pos[0] += 1
                    # print "Position after option = ", new_pos
                    if self.isLegal(new_pos, newGameState):
                        if not self.detectWall(new_pos, newGameState):
                            temp_pos = new_pos[:]
                            newGameState.robotPosition = new_pos [:]
                            if self.detectGoal(new_pos, gameState): #This will check for the final goal
                                self.win = True
                                # gameState.reward = 3.0
                                tempReward += 100
                                break # No need to continue the rest of the actions!
                            elif self.detectGoal(new_pos, newGameState): #This will check for subgoal - which is the end of the option
                                print "Goal is done I swear!!!"
                                newGameState.win = True
                                # gameState.reward = 3.0 # TODO: Do I really reward the completion of a subgoal like this during the main RL process?
                                # tempReward += 100 # TODO: Do I really reward the completion of a subgoal like this during the main RL process?
                                break
                            else:
                                tempReward -= 0 #Negative in general if it doesn't reach any goal!
                        else:
                            tempReward -= 0.5 #Negative reward for hitting the wall!
                            temp_pos = current_pos [:]
                            newGameState.robotPosition = current_pos [:]
                    else:
                        temp_pos = current_pos
                        newGameState.robotPosition = current_pos [:]
            # tempReward += 10

        gameState.steps = 1 + optionTimeLength
        gameState.robotPosition = temp_pos
        gameState.win = self.win
        gameState.lastAction = currentAction # Since we know it is only action!
        gameState.reward = -1.0 + tempReward
        return gameState

    def detectWall(self, position, gameState):
        x, y = position
        if gameState.gameMap[x][y] == "#":
            return True
        return False

    def detectGoal(self, position, gameState):
        # print "Goal check = ", position, gameState.gameGoal
        if list(position) == list(gameState.gameGoal):
            return True
        return False

    def isLegal(self, position, gameState):
        x,y = position

        if (x < gameState.boardDim[0]) and (y < gameState.boardDim[1]):
            return True
        return False

class GameLogic2(GameLogic):
    def __init__(self, PrimitiveActions):
        GameLogic.__init__(self)
        self.PrimitiveActions = PrimitiveActions

    def GetLegalOptions(self, gameState):
        """
        This method will return the list of legal actions/options that can be taken starting from the current state.
        :param gameState:
        :return:
        """
        pass

    def update2(self, gameState, AgentClass, stoppingCondition=False, insideOption=False):
        assert (isinstance(gameState, GameState))
        currentAction = AgentClass.getAction(tuple(gameState.robotPosition))
        current_robot_pos = gameState.robotPosition
        immediateReward = 0

        # if not insideOption:
        #     print "Action selected = ", currentAction, " -- Current position = ", current_robot_pos
        if self.detectGoal(current_robot_pos, gameState):
            # print "Goal detected, ", current_robot_pos
            self.win = True
            temp_pos = current_robot_pos
            gameState.win = self.win

        elif self.IsPrimitiveAction(currentAction):
            new_pos = self.updatePosPrimitiveAction(currentAction, current_robot_pos)

            if self.isLegal(new_pos, gameState):  # not outside the game borders
                if not self.detectWall(new_pos, gameState):  # doesn't get inside the wall
                    temp_pos = new_pos
                else:
                    temp_pos = current_robot_pos
            else:
                temp_pos = current_robot_pos

            gameState = self.UpdateGameState(currentGameState=gameState, newRobotPosition=temp_pos,
                                             totalImmediateReward=immediateReward, winFlag=False,  # I made the winFlag a hard false, since it should not be updated here
                                             lastAction=currentAction, macroSteps=not insideOption, steps_bias=1)

        else: #In this case, we are dealing with an option
            newGameState = GameState()
            newGameState.Copy(gameState)
            # finalGoal = gameState.gameGoal
            newGameState.gameGoal = currentAction.getOptionGoal()
            optionWatchDogTimer = 0
            while (not newGameState.win) and (optionWatchDogTimer < 200) and (newGameState.lastAction != None):  # TODO: use a parametrized class to set this number.
                newGameState = self.update2(newGameState, currentAction.LearningAgentClass, stoppingCondition=True, insideOption=True) #Hope this will work
                # immediateReward += AgentClass.getStateValue(newGameState.robotPosition)**optionWatchDogTimer #The delayed reward
                optionWatchDogTimer += 1

            gameState = self.UpdateGameState(currentGameState=gameState, newRobotPosition=newGameState.robotPosition,
                                             totalImmediateReward=immediateReward, winFlag=False, # I made the winFlag a hard false, since it should not be updated here
                                             lastAction=currentAction, macroSteps=not insideOption, steps_bias=optionWatchDogTimer) #maybe I need to review the parameters of this class
            # print "newGameState.win = ", newGameState.win, " - optionWatchDogTimer = ", optionWatchDogTimer, " - newGameState.lastAction = ", newGameState.lastAction
            temp_pos = newGameState.robotPosition

        # if not insideOption:
        #     print "Update -- old Pos : ", current_robot_pos, " -- action : ", currentAction, " -- newPos : ", temp_pos
        # else:
        #     print "Update insideOption -- old Pos : ", current_robot_pos, " -- action : ", currentAction, " -- newPos : ", temp_pos
        return gameState

    def update(self, gameState, AgentClass, stoppingCondition=False, insideOption=False):
        assert (isinstance(gameState, GameState))
        currentAction = AgentClass.getAction(tuple(gameState.robotPosition))
        current_robot_pos = gameState.robotPosition
        # print "UPDATE -- ", gameState.robotPosition, " -- Action selected : ", currentAction
        immediateReward = 0

        #Check here if the robot is in the goal state --> No actions is returned
        if currentAction == None:
            # print "No more Actions! -- Option = ", insideOption, " -- action = ", currentAction
            temp_pos = (None, None)
            # temp_pos = current_robot_pos
            self.win = True
            immediateReward = 0
            # immediateReward = 100

            gameState = self.UpdateGameState(currentGameState=gameState, newRobotPosition=temp_pos,
                                             totalImmediateReward=immediateReward, winFlag=self.win,
                                             lastAction=currentAction, macroSteps=not insideOption)

        elif self.IsPrimitiveAction(currentAction):
            new_pos = self.updatePosPrimitiveAction(currentAction, current_robot_pos)

            if self.isLegal(new_pos, gameState):  # not outside the game borders
                if not self.detectWall(new_pos, gameState):  # doesn't get inside the wall
                    temp_pos = new_pos
                    if insideOption:
                        # If my understanding is correct (from the paper and from the talks with Nicolas),
                        # I should put the value of this state from the Q-table inside the options agent
                        # immediateReward = 0
                        immediateReward = AgentClass.getStateValue(temp_pos)
                        print "Action = ", currentAction, " - Immediate reward ", immediateReward

                    elif self.detectGoal(new_pos, gameState):
                        # self.win = True
                        # immediateReward = 100
                        # This if condition is experimental. I am not sure if it is correct.
                        if insideOption:
                            immediateReward = 0
                        else:
                            immediateReward = 100
                    else:
                        immediateReward = 0
                else:
                    temp_pos = current_robot_pos
            else:
                temp_pos = current_robot_pos

            gameState = self.UpdateGameState(currentGameState=gameState, newRobotPosition=temp_pos,
                                             totalImmediateReward=immediateReward, winFlag=False,  # I made the winFlag a hard false, since it should not be updated here
                                             lastAction=currentAction, macroSteps=not insideOption)

        else: #In this case, we are dealing with an option
            """
            My idea here is that the function will recurse on itself.
            If it works (recursion inside the class is usually a bad idea), then it should generalize beautifully.
            Otherwise, I may have to take this function outside the class in order to enable the recursion
            """
            # print "UPDATE - OPTION - ", currentAction
            newGameState = GameState()
            newGameState.Copy(gameState)
            finalGoal = gameState.gameGoal
            newGameState.gameGoal = currentAction.getOptionGoal()
            optionWatchDogTimer = 0
            while (not newGameState.win) and (optionWatchDogTimer < 200) and (newGameState.lastAction != None): #TODO: use a parametrized class to set this number.
                # print "newGameState.win = ", newGameState.win
                newGameState = self.update(newGameState, currentAction.LearningAgentClass, stoppingCondition=True, insideOption=True) #Hope this will work
                optionWatchDogTimer += 1
                print "optionWatchDogTimer = ", optionWatchDogTimer

            print "State after options completion = ", newGameState
            # Make a check on the goal flag
            # print "I reached here :D , optionWatchDogTimer = ", optionWatchDogTimer
            # print "UPDATE -- Option is OVER -- ", currentAction, " -- with Reward : ", newGameState.reward, " -- optionWatchDogTimer = ", optionWatchDogTimer
            # if self.detectGoal(newGameState.robotPosition, gameState): #This also has the same problem. It gives the reward before actually taking the step.
            #     immediateReward = 100
            # else:
            #     self.win = False
            #     immediateReward = 0

            gameState = self.UpdateGameState(currentGameState=gameState, newRobotPosition=newGameState.robotPosition,
                                             totalImmediateReward=immediateReward, winFlag=False, # I made the winFlag a hard false, since it should not be updated here
                                             lastAction=currentAction, macroSteps=not insideOption) #maybe I need to review the parameters of this class

        return gameState


    def IsPrimitiveAction(self, action):
        return type(action) is str

    def UpdateGameState (newPos, currentGameState, newRobotPosition, totalImmediateReward, winFlag, lastAction,
                         macroSteps, steps_bias=1):
        newGameState = GameState()
        newGameState.Copy(currentGameState)
        newGameState.reward = totalImmediateReward
        newGameState.win = winFlag
        newGameState.robotPosition = newRobotPosition
        newGameState.lastAction = lastAction
        newGameState.steps += steps_bias
        if macroSteps:
            newGameState.macroSteps += 1
        return newGameState

    def updatePosPrimitiveAction(self, action, current_pos):
        assert (type(action) is str)
        assert (action in self.PrimitiveActions)

        new_pos = list(current_pos[:])
        if action == 'LEFT':
            new_pos[1] -= 1
        elif action == 'RIGHT':
            new_pos[1] += 1
        elif action == 'UP':
            new_pos[0] -= 1
        elif action == 'DOWN':
            new_pos[0] += 1

        return tuple(new_pos)


class Domain:
    """
    This class will be resposible to hold information about the current map, and the task to be achieved.
    This domain will be overloaded by the options, since each option works in its own domain (start, goal)
    """
    def __init__(self):
        self.gameMap = []
        self.empty_poses = []
        self.robot_position = [None, None]
        self.boardDim = [None, None]
        self.gameGoal = [None, None]

    def ReadyState(self):
        """
        This method will prepare the game state
        :return:
        """
        gameState = GameState()
        gameState.gameGoal = self.gameGoal
        gameState.gameMap = self.gameMap
        gameState.robotPosition = self.robot_position
        gameState.boardDim = self.boardDim
        gameState.reward = 0.0
        return gameState

    def copy_domain(self):
        """
        Here I will define how this class can be copied
        :return:
        """
        pass

    def loadGameBoad(self, filename=""):
        """
        This function will load a map from a text file, and will return the structure of the map
        :param filename:
        :return:
        """
        with open(filename, "r") as map_file:
            map_raw_data = map_file.read().splitlines()

        for line in map_raw_data:
            line_items = []
            for item in line:
                line_items.append(item)
            self.gameMap.append(line_items)

        self.boardDim[0] = len(self.gameMap)
        self.boardDim[1] = len(self.gameMap[0])


        self.gameGoal = self.goalGlobalIndex(self.gameMap)
        # self.empty_poses = self.initialSet()
        return self.gameMap

    def goalGlobalIndex(self, gameMap):
        for row in range(len(gameMap)):
            for col in range(len(gameMap[row])):
                if gameMap[row][col] == 'G':
                    return [row, col]

    def getGoal(self):
        """
        This function should be overridden inside the options. The global objective will be to reach the 'G'
        :return:
        """
        return self.gameGoal

    def getSubGoals(self):
        return getDoorPositions(self.gameMap)

    def initialSet(self, area_number=None):
        """
        This function will get the legal starting set for the robot
        It should be overriden in the options
        In this case, it is all the empty places in the map
        :return:
        """
        self.empty_poses = []
        for row_index in range(len(self.gameMap)):
            for col_index in range(len(self.gameMap[row_index])):
                if area_number==None: # all free areas are okay
                    if (self.gameMap[row_index][col_index] != "#") and (self.gameMap[row_index][col_index] != "G"):
                        self.empty_poses.append((row_index, col_index))
                else:
                    for row_index in range(len(self.gameMap)):
                        for col_index in range(len(self.gameMap[row_index])):
                            if (self.gameMap[row_index][col_index] != "#") and (self.gameMap[row_index][col_index] != "G")\
                                    and (self.gameMap[row_index][col_index] == str(area_number)):
                                self.empty_poses.append([row_index, col_index])
        # return self.empty_poses
        # self.empty_poses.append(self.gameGoal)
        return self.empty_poses

    def initRobot(self):
        """
        Here, I will assume a random position anywhere in the list of empty positions I have
        :return:
        """
        assert (len(self.empty_poses) != 0) # make sure there are empty places.
        self.robot_position = list(random.choice(self.empty_poses))
        # assert (self.robot_position != self.gameGoal) #Just to make sure!
        return self.robot_position

    def initRobotFIXED(self):
        """
        Here, I will assume a random position anywhere in the list of empty positions I have
        :return:
        """
        assert (len(self.empty_poses) != 0) # make sure there are empty places.
        # self.robot_position = list(self.empty_poses[0])
        self.robot_position = [2, 2]
        # self.robot_position = [10, 14]
        return self.robot_position

    def setGoal(self, newGoal):
        self.gameGoal = list(newGoal)

    def setInitiationSet(self, newInitSet):
        self.empty_poses = newInitSet



def getDoorPositions(gameMap):
    """
    This function will extract some pattern from the map, to identify the subgoals we have
    The pattern will be something like
    [" ", "#", " "]
    [" ", " ", " "]
    [" ", "#", " "]
    The pattern will always be a 3x3 matrix
    The '?' means we don't care about the status of this block
    :param pattern:
    :return:
    """
    doors_pos = {}
    doors = []
    doors.append([["?", "#", "?"],
                  ["x", " ", "x"],
                  ["?", "#", "?"]])

    doors.append([["?", "x", "?"],
                  ["#", " ", "#"],
                  ["?", "x", "?"]])
    # Start with 3x3 window moving
    for door in doors:
        row_index = 0
        while (row_index < len(gameMap)-2):
            col_index = 0
            mapRows = gameMap[row_index:row_index+3]
            while (col_index < len(gameMap[row_index])-2):
                mapWindow = []
                for row_loc in mapRows:
                    mapWindow.append(row_loc[col_index:col_index+3])

                if (door[1][1] == mapWindow[1][1]) or (mapWindow[1][1] == "G"):
                    try:
                        area = [int(mapWindow[1][0]), int(mapWindow[1][2])]
                    except:
                        area = [int(mapWindow[0][1]), int(mapWindow[2][1])]

                    # Then, the element in the middle is the door
                    y = col_index + 1
                    x = row_index + 1
                    doors_pos[(x, y)] = area
                col_index += 1
            row_index += 1
    return doors_pos
