import copy

def ConsoleDraw(gameState):
    robotPosition = gameState.robotPosition
    gameMap = copy.deepcopy(gameState.gameMap)

    gameMap[robotPosition[0]][robotPosition[1]] = "R" # Put the robot on the map

    final_output = ""
    for row in gameMap:
        for element in row:
            try:
                x = int(element)
                final_output += " "
            except:
                final_output += element
        final_output += "\n"

    print final_output