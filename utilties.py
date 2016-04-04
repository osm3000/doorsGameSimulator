import copy
class domain:
    """
    This class will be resposible to hold information about the current map, and the task to be achieved.
    This domain will be overloaded by the options, since each option works in its own domain (start, goal)
    """
    def __init__(self):
        self.map = []

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
            self.map.append(line_items)

        return self.map

    def goalGlobalIndex (self, gameMap):
        for row in range(len(gameMap)):
            for col in range(len(gameMap[row])):
                if gameMap[row][col] == 'G':
                    return row, col

    def getGoal(self):
        """
        This function should be overriden inside the options. The global objective will be to reach the 'G'
        :return:
        """
        return self.goalGlobalIndex(self.map)

def getDoorPositions(map):
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
    doors = []
    doors[0] = [["?", "#", "?"],
                [" ", " ", " "],
                ["?", "#", "?"]]

    doors[1] = [["?", " ", "?"],
                ["#", " ", "#"],
                ["?", " ", "?"]]

    doors[2] = [[" ", "#", " "],
                [" ", " ", " "],
                [" ", "#", " "]]
    for


# map = loadGameBoad("test_map")
# for i in map:
#     print i
# print goalIndex(map)