from options import *
import random

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
                return 'LEFT'
            elif consoleInput == 'd':
                return 'RIGHT'
            elif consoleInput == 'w':
                return 'UP'
            elif consoleInput == 's':
                return 'DOWN'
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
        return self.q.get((state, action), 0.0)
        # return self.q.get((state, action), 1.0)

    def learnQ(self, state, action, reward, value):
        oldv = self.q.get((state, action), None)
        if oldv is None:
            self.q[(state, action)] = reward
        else:
            self.q[(state, action)] = oldv + self.alpha * (value - oldv)

    def getAction(self, state, return_q = False):
        q = [self.getQ(state, a) for a in self.actions]
        # print state, " -- ", q
        maxQ = max(q)

        if random.random() < self.epsilon:
            # 1st way of selecting actions
            #action = random.choice(self.actions)

            # 2nd way of selecting actions
            minQ = min(q); mag = max(abs(minQ), abs(maxQ))
            q = [q[i] + random.random() * mag - .5 * mag for i in range(len(self.actions))] # add random values to all the actions, recalculate maxQ
            maxQ = max(q)

        count = q.count(maxQ)
        if count > 1:
            best = [i for i in range(len(self.actions)) if q[i] == maxQ]
            i = random.choice(best)
        else:
            i = q.index(maxQ)

        action = self.actions[i]
        # print maxQ, " -- ", q
        self.MaxQ = maxQ
        if return_q: # if they want it, give it!
            return action, q

        return action

    def learn(self, state1, action1, reward, state2, timesteps=1):
        maxqnew = max([self.getQ(state2, a) for a in self.actions])
        self.learnQ(state1, action1, reward, reward + (self.gamma**timesteps)*maxqnew)

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
    def __init__(self, actions, finalGoal=None, epsilon=0.1, alpha=0.2, gamma=0.9):
        self.q = {}

        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.actions = actions
        self.MaxQ = None
        self.finalGoal = finalGoal

    def getQ(self, state, action):
        # print state, " -- ", action, " -- ", self.finalGoal
        return self.q.get((state, action), 0.0)
        # return self.q.get((state, action), 1.0)

    # This is the old learnQ
    # def learnQ(self, state, action, reward, value):
    #     oldv = self.q.get((state, action), None)
    #     if oldv is None:
    #         # self.q[(state, action)] = round(reward, 3)
    #         self.q[(state, action)] = round(reward + self.alpha * (value - reward), 3)
    #     else:
    #         # self.q[(state, action)] = oldv + self.alpha * (value - oldv)
    #         self.q[(state, action)] = round(oldv + self.alpha * (value - oldv), 3)
    #     # self.q[(state, action)] = round(reward + self.alpha * (value - reward), 3)
    #     # print "self.q[(", state, ", ", action, ")] = ", self.q[(state, action)]


    # This new learnQ is working to match with Sutton's paper
    def learnQ(self, state, action, reward, value):
        oldv = self.q.get((state, action), None)
        if self.checkFinalGoal(state):
            self.q[(state, action)] = 100
        else:
            if oldv is None:
                self.q[(state, action)] = round(reward + self.alpha * (value - reward), 3)
            else:
                self.q[(state, action)] = round(oldv + self.alpha * (value - oldv), 3)
        # print "self.q[(", state, ", ", action, ")] = ", self.q[(state, action)]

    def getAction(self, state, return_q=False):
        # Check if the current state is the goal state or not. If yes, return None Actions
        if self.checkFinalGoal(state) or (state == (None, None)):
            return None

        actions_list = self.actions[:]
        q = [self.getQ(state, a) for a in actions_list]
        maxQ = max(q)

        if random.random() < self.epsilon:
            #action = random.choice(self.actions)
            minQ = min(q); mag = max(abs(minQ), abs(maxQ))
            q = [round(q[i] + random.random() * mag - .5 * mag, 3) for i in range(len(actions_list))] # add random values to all the actions, recalculate maxQ
            maxQ = max(q)

        action = None

        # This while loop is introduced in case of options, in order to make sure that we select a legal option.
        while True:
            maxQ = max(q)
            count = q.count(maxQ)

            if count > 1:
                best = [i for i in range(len(actions_list)) if q[i] == maxQ]
                i = random.choice(best)
            else:
                i = q.index(maxQ)

            # Check if the action is an option.
            if isinstance(actions_list[i], Options):
                """
                This is a complete heuristic from my side. I have no clue if there is a formal treatment for this
                problem.
                This is inspired from the random selection process used in this Qlearn algorithm (just few lines above).
                """
                # First, check if this state is a legal state for the action
                if actions_list[i].checkLegality(state):
                    action = actions_list[i]
                    break
                else:
                    # 1. Reduce its Q-Value --> I tried this hypothesis before, and it can lead to an infinite loop
                    # minQ = min(q); mag = max(abs(minQ), abs(maxQ))
                    # q[i] -= random.random() * mag

                    # 2. Remove the troubling action and its Q-value
                    del actions_list[i]
                    del q[i]
                    continue
            else:
                action = actions_list[i]
                break # Since this is a primitive action in this case

        self.MaxQ = maxQ

        if return_q: #if they want it, give it!
            return action, q

        return action

    def returnLastMaxQ(self):
        return self.MaxQ

    def checkFinalGoal(self, state):
        if tuple(state) == tuple(self.finalGoal):
            maxqnew = 100
            return True
        return False

    def learn(self, state1, action1, reward, state2, timesteps=1, finalGoal = None):
        maxqnew = max([self.getQ(state2, a) for a in self.actions+[None]])
        # print "I am doing Q-Value Learning !! :\t", state1, action1, state2, reward, maxqnew, timesteps

        if self.detectOptionType(action1):  # In case of an option, I must update all its initiation state
            self.learnQ(state1, action1, reward, reward + (self.gamma**timesteps)*maxqnew)
        else: #This will update with primitive action or None action (in case of the goal state)
            self.learnQ(state1, action1, reward, reward + (self.gamma)*maxqnew)
        # Qvalue = [self.getQ(state1, a) for a in self.actions]
        # print Qvalue

    def detectOptionType(self, action):
        """
        This method will detect whether this action is a primitive action or an option
        :param action:
        :return:
        """
        return isinstance(action, Options)

    def getStateDistanceOptions(self, action1, state):
        """
        This will calculate the L1 distance
        Note here that I assume we have an optimal policy for each option. Later, I must play the option multiple times,
        like what I did in the testing, and what is the likelihood of this states ending in the goal of the option.
        :param action1:
        :param state:
        :return:
        """
        goal = action1.getOptionGoal()
        return abs(goal[0] - state[0]) + abs(goal[1] - state[1])

    def getStateDistanceStates(self, state1, state2):
        """
        This will calculate the L1 distance
        Note here that I assume we have an optimal policy for each option. Later, I must play the option multiple times,
        like what I did in the testing, and what is the likelihood of this states ending in the goal of the option.
        :param action1:
        :param state:
        :return:
        """
        return abs(state1[0] - state2[0]) + abs(state1[1] - state2[1])


    def returnLastMaxQ(self):
        StatesQ = {}
        StatesMaxQ = {}
        for item_pair in self.q:
            state, _ = item_pair
            # if state not in StatesMaxQ.keys():
            #     q = [self.getQ(state, a) for a in self.actions]
            #     StatesMaxQ[state] = max(q)
            try:
                StatesQ[state].append(self.q[item_pair])
            except:
                StatesQ[state] = [self.q[item_pair]]
        for state in StatesQ:
            StatesMaxQ[state] = max(StatesQ[state])
        return StatesMaxQ

    def getStateValue(self, state):

        return max([self.getQ(state, a) for a in self.actions+[None]])
