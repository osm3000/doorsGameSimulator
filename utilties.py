import copy
import random
import pygame
from options import *

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

    def Copy(self, gameState):
        self.robotPosition = copy.deepcopy(gameState.robotPosition)
        self.win = copy.deepcopy(gameState.win)
        self.gameGoal = copy.deepcopy(gameState.gameGoal)
        self.reward = copy.deepcopy(gameState.reward)
        self.gameMap = copy.deepcopy(gameState.gameMap)
        self.boardDim = copy.deepcopy(gameState.boardDim)
        self.steps = copy.deepcopy(gameState.steps)
        self.lastAction = copy.deepcopy(gameState.lastAction)

    def __str__(self):
        final = "robotPosition = " + str(self.robotPosition) + \
                "\nwin = " + str(self.win) + \
                "\ngameGoal = " + str(self.gameGoal) + \
                "\nreward = " + str(self.reward) + \
                "\nboardDim = " + str(self.boardDim) + \
                "\nsteps = " + str(self.steps) + \
                "\nlastAction = " + str(self.lastAction) + \
                "\n"
        return final

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
        actions_list = AgentClass.getAction(tuple(gameState.robotPosition))
        current_pos = gameState.robotPosition
        temp_pos = current_pos[:]
        current_action = None
        OptionsLen = 0
        tempReward = 0
        for current_action in actions_list:

            if type(current_action) is str:
                new_pos = temp_pos[:]
                if current_action == 'LEFT':
                    new_pos[1] -= 1
                elif current_action == 'RIGHT':
                    new_pos[1] += 1
                elif current_action == 'UP':
                    new_pos[0] -= 1
                elif current_action == 'DOWN':
                    new_pos[0] += 1

                if self.isLegal(new_pos, gameState):
                    if not self.detectWall(new_pos, gameState):
                        temp_pos = new_pos
                        if self.detectGoal(new_pos, gameState):
                            self.win = True
                            gameState.reward = 3.0
                            break # No need to continue the rest of the actions!
                    else:
                        tempReward -= 0.5 #Negative reward for hitting the wall!
                        temp_pos = current_pos
                else:
                    temp_pos = current_pos
            # elif isinstance(current_action, Options):
            else:
                print "An option has been selected = ", current_action
                newGameState = GameState()
                newGameState.Copy(gameState)
                # New direction: Here, the option will take control of the execution.
                newGameState.gameGoal = current_action.getOptionGoal()
                # new_pos = temp_pos[:]
                debugCounter = 0
                while not newGameState.win: #The option has to terminate. I can add a random probability here in the future as well.
                    debugCounter += 1
                    print "debugCounter = ", debugCounter
                    # if debugCounter == 30:
                    #     exit()
                    actions_list_option = current_action.LearningAgentClass.getAction(tuple(newGameState.robotPosition))
                    print "Actions from the option = ", actions_list_option
                    for current_action_OPTION in actions_list_option:
                        OptionsLen += 1 # TODO: This assumes the option uses primitive action. This update should change for future generalization

                        if type(current_action_OPTION) is str:
                            print "YES, it is a string!"
                            new_pos = temp_pos[:]
                            print "From Option - robot position = ", new_pos
                            # print "Legal action from options = ", current_action_OPTION, new_pos
                            if current_action_OPTION == 'LEFT':
                                new_pos[1] -= 1
                            elif current_action_OPTION == 'RIGHT':
                                new_pos[1] += 1
                            elif current_action_OPTION == 'UP':
                                new_pos[0] -= 1
                            elif current_action_OPTION == 'DOWN':
                                new_pos[0] += 1
                            # print "Position after option = ", new_pos
                            if self.isLegal(new_pos, newGameState):
                                if not self.detectWall(new_pos, newGameState):
                                    temp_pos = new_pos[:]
                                    newGameState.robotPosition = new_pos [:]
                                    if self.detectGoal(new_pos, gameState): #This will check for the final goal
                                        # print "WE WOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOON"
                                        # print new_pos
                                        self.win = True
                                        gameState.reward = 3.0
                                        break # No need to continue the rest of the actions!
                                    elif self.detectGoal(new_pos, newGameState): #This will check for subgoal - which is the end of the option
                                        print "Goal is done I swear!!!"
                                        newGameState.win = True
                                        gameState.reward = 3.0
                                        break
                                else:
                                    tempReward -= 0.5 #Negative reward for hitting the wall!
                                    temp_pos = current_pos [:]
                                    newGameState.robotPosition = current_pos [:]
                            else:
                                temp_pos = current_pos
                                newGameState.robotPosition = current_pos [:]
                # tempReward += 10

        gameState.steps = len(actions_list) + OptionsLen
        gameState.robotPosition = temp_pos
        gameState.win = self.win
        gameState.lastAction = current_action # Since we know it is only action!
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
        self.empty_poses.append(self.gameGoal)
        return self.empty_poses

    def initRobot(self):
        """
        Here, I will assume a random position anywhere in the list of empty positions I have
        :return:
        """
        assert (len(self.empty_poses) != 0) # make sure there are empty places.
        self.robot_position = list(random.choice(self.empty_poses))
        assert (self.robot_position != self.gameGoal) #Just to make sure!
        return self.robot_position

    def initRobotFIXED(self):
        """
        Here, I will assume a random position anywhere in the list of empty positions I have
        :return:
        """
        assert (len(self.empty_poses) != 0) # make sure there are empty places.
        self.robot_position = self.empty_poses[0]
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
