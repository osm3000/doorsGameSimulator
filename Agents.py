import pygame
import random
from options import *

class ManualAgent:
    def __init__(self, actions = ['LEFT', 'RIGHT', 'UP', 'DOWN']):
        self.actions = actions
        pass


    def getAction(self, gameState = None):
        """
        This function will read events from keyboard
        :return:
        """
        while True:
            consoleInput = raw_input("Enter your move: ")
            if consoleInput == 'a':
                return ['LEFT']
            elif consoleInput == 'd':
                return ['RIGHT']
            elif consoleInput == 'w':
                return ['UP']
            elif consoleInput == 's':
                return ['DOWN']
            else:
                print "Invalid entry. Enter again"

class RandomAgent:
    def __init__(self, actions = ['LEFT', 'RIGHT', 'UP', 'DOWN']):
        self.actions = actions
        pass

    def getAction(self, gameState = None):
        actions_list = [random.choice(self.actions) for i in range(3)]
        return actions_list

class QLearnAgent:
    def __init__(self, actions, epsilon=0.1, alpha=0.2, gamma=0.9):
        self.q = {}

        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.actions = actions
        self.MaxQ = None

    def getQ(self, state, action):
        # return self.q.get((state, action), 0.0)
        return self.q.get((state, action), 1.0)

    def learnQ(self, state, action, reward, value):
        oldv = self.q.get((state, action), None)
        if oldv is None:
            self.q[(state, action)] = reward
        else:
            self.q[(state, action)] = oldv + self.alpha * (value - oldv)

    def getAction(self, state, return_q = False):
        q = [self.getQ(state, a) for a in self.actions]
        # print state
        # print q , " -- ", state
        maxQ = max(q)

        if random.random() < self.epsilon:
            #action = random.choice(self.actions)
            minQ = min(q); mag = max(abs(minQ), abs(maxQ))
            q = [q[i] + random.random() * mag - .5 * mag for i in range(len(self.actions))] # add random values to all the actions, recalculate maxQ
            maxQ = max(q)

        count = q.count(maxQ)
        if count > 1:
            best = [i for i in range(len(self.actions)) if q[i] == maxQ]
            i = random.choice(best)
        else:
            i = q.index(maxQ)

        action = [self.actions[i]]
        # print action
        self.MaxQ = maxQ
        if return_q: # if they want it, give it!
            return action, q

        return action

    def learn(self, state1, action1, reward, state2):
        maxqnew = max([self.getQ(state2, a) for a in self.actions])
        self.learnQ(state1, action1, reward, reward + self.gamma*maxqnew)

    def returnLastMaxQ(self):
        StatesMaxQ = {}
        for item_pair in self.q:
            state, _ = item_pair
            if state not in StatesMaxQ.keys():
                q = [self.getQ(state, a) for a in self.actions]
                StatesMaxQ[state] = max(q)
        return StatesMaxQ

class QLearnAgentWithOptions:
    """
    There is a trick in the case of options here: The initiation set. Every option is train to start from a specific
    initiation set. If I want to take this into account during the selection of the best action - in getAction method -,
    it could be hideous - although it worth trying to think about it.
    For now, I will ignore this issue. I will bet that the learning process in the main RL will be able to learn this
    on its own.
    An idea for this is to introduce a new primitive action, we call it NoAction. Each option will check if the current
    state of the game is part of its initiation set. If yes, it will return its policy. If not, it will return this
    NoAction, which will lead to nothing at all.

    Another idea is make a check in the getAction method if the state is legal state for the selected option or not.
    If yes: select the option.
    If not: reduce the option's Q value, and select a new action to make
    """
    def __init__(self, actions, epsilon=0.1, alpha=0.2, gamma=0.9):
        self.q = {}

        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.actions = actions
        self.MaxQ = None

    def getQ(self, state, action):
        return self.q.get((state, action), 0.0)
        # return self.q.get((state, action), 1.0)

    def learnQ(self, state, action, reward, value):
        oldv = self.q.get((state, action), None)
        if oldv is None:
            self.q[(state, action)] = round(reward, 3)
        else:
            # self.q[(state, action)] = oldv + self.alpha * (value - oldv)
            self.q[(state, action)] = round(oldv + self.alpha * (value - oldv), 3)

    def getAction(self, state, return_q=False):
        q = [self.getQ(state, a) for a in self.actions]
        maxQ = max(q)
        # print self.actions
        # print q, " -- ", state
        # print self.actions
        # print q

        if random.random() < self.epsilon:
            #action = random.choice(self.actions)
            minQ = min(q); mag = max(abs(minQ), abs(maxQ))
            q = [round(q[i] + random.random() * mag - .5 * mag, 3) for i in range(len(self.actions))] # add random values to all the actions, recalculate maxQ
            maxQ = max(q)

        action = []
        while True:
            # print "here --- ",q
            maxQ = max(q)
            count = q.count(maxQ)

            if count > 1:
                best = [i for i in range(len(self.actions)) if q[i] == maxQ]
                i = random.choice(best)
            else:
                i = q.index(maxQ)

            # Check if the action is an option.
            if isinstance(self.actions[i], Options):
                """
                This is a complete heuristic from my side. I have no clue if there is a formal treatment for this
                problem.
                This is inspired from the random selection process used in this Qlearn algorithm (just few lines above).
                """
                # First, check if this state is a legal state for the action
                if self.actions[i].checkLegality(state):
                    action = [self.actions[i]]
                    break
                else:
                    # If not, reduce its Q-Value
                    minQ = min(q); mag = max(abs(minQ), abs(maxQ))
                    q[i] -= random.random() * mag
                    continue
            else:
                action = [self.actions[i]]
                break # Since this is a primitive action in this case

        assert (len(action) != 0) #Because in this case, no action is selected
        self.MaxQ = maxQ
        if return_q: #if they want it, give it!
            return action, q

        return action

    def returnLastMaxQ(self):
        return self.MaxQ

    def learn(self, state1, action1, reward, state2):
        # print "I am fucking learning!, \n", state1, action1, state2, reward
        maxqnew = max([self.getQ(state2, a) for a in self.actions])
        # print "maxqnew = ", maxqnew
        self.learnQ(state1, action1, reward, reward + self.gamma*maxqnew)

    def addOptions(self, optionsList):
        for option in optionsList:
            self.actions.append(option)