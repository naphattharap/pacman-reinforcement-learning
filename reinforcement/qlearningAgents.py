# qlearningAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random, util, math
import numpy as np


class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """

    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        # Initialize Q value table
        # util.Counter will return 0 if key is not found.
        self.q_values = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        return self.q_values[(state, action)]

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        actions = self.getLegalActions(state)
        
        # In case of terminal state (no legal action)
        if len(actions) == 0:
            return 0
        
        values = []
        for action in actions:
            values.append(self.getQValue(state, action))
        
        # Returns max value from all possible action at a state.
        return max(values)

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        
        actions = self.getLegalActions(state)
        
        # in case it is at terminal state
        if len(actions) == 0:
            return None
        
        # Get the action that return highest Q value based on the state.
        q_value_actions = util.Counter()
        for action in actions:
            q_value_actions[action] = self.getQValue(state, action)
                
        return q_value_actions.argMax()
    
    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Question 5: Epsilon Greedy
        # Pick Action
        legalActions = self.getLegalActions(state)
        
        action = None
       
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        
        # if there are no legal actions, 
        # which is the case at the terminal state, 
        # you should choose None as the action.
        if len(legalActions) == 0:
            return action
        
        # Compute the action to take in the current state.  
        # With probability self.epsilon 
        # flipCoin returns true or false
        if util.flipCoin(self.epsilon):
            action = random.choice(legalActions)
        else: 
            action = self.computeActionFromQValues(state)
 
        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        
        # Update the value estimation of an action based on the reward we got 
        # and the reward we expect next.
        """
            Q-Learning update equation:
            Q(s, a) <-- (1 - alpha) * Q(s_t, a_t) 
                        + alpha * [reward + discount_factor * max(Q(s_t+1, action)]
        """
        updated_q_value = (1 - self.alpha) * self.getQValue(state, action) + self.alpha * (reward + (self.discount * self.computeValueFromQValues(nextState)))
        
        # update q_value to table
        self.q_values[(state, action)] = updated_q_value

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self, state)
        self.doAction(state, action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """

    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        # approximate Q-function is dot product between feature and weight
        q_value = np.dot(self.weights, self.featExtractor.getFeatures(state, action)) 
        return q_value

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        """
        Update Q-Value: http://ai.berkeley.edu/reinforcement.html
            different = (r + discount_factor * max(Q(s',a')) - Q(s,a)
            
            w_i <-- w_i + alpha * difference * feature_i(s,a)
        """
        # plug equation 
        diff = (reward + self.discount * self.computeValueFromQValues(nextState)) - self.getQValue(state, action)
        # Loop through all feature to update weight
        features = self.featExtractor.getFeatures(state, action)
        for i in features:
            self.weights[i] = self.weights[i] + self.alpha * diff * features[i]

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            # pass
            print self.weights
