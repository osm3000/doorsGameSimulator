import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import copy
class QValueOnlinePlot:
    """

    """
    def __init__(self, figureName, gameState):
        self.figure_name = figureName

        self.fig = plt.figure(self.figure_name)
        self.ax = self.fig.add_subplot(111)

        self.title = "Achieving Goal: " + str(gameState.gameGoal)
        self.ax.set_title(self.title)
        plot_handle = plt.ion()
        plt.show()

        # print gameState.boardDim
        self.heatMapArray = np.zeros((gameState.boardDim[0], gameState.boardDim[1]))

        self.DrawBar = False # This should happen only once

    def Draw(self, MaxQvalue):
        """

        :param gameState:
        :return:
        """
        # current_state = gameState.robotPosition # This should be changed to the robot prev position.
        # but should work fine now for testing only
        for state in MaxQvalue:
            self.heatMapArray[state[0], state[1]] = MaxQvalue[state]
        # cax = self.ax.imshow(self.heatMapArray, cmap=cm.coolwarm)
        cax = self.ax.imshow(self.heatMapArray, interpolation='nearest', cmap=cm.cool)
        if not self.DrawBar:
            # cbar = self.fig.colorbar(cax, ticks=[-501, -500, 500])
            self.DrawBar = True

        plt.draw()
        # print self.heatMapArray
        # print "HERE"
        # print exit()

    def EndDraw(self):
        plt.close()
        # print self.heatMapArray
        # exit()