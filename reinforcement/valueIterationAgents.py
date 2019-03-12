# valueIterationAgents.py
# -----------------------
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

import mdp, util

from learningAgents import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        # Initial value for all states as 0.
        self.values = util.Counter()  # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        # https://www.cs.swarthmore.edu/~bryce/cs63/s16/slides/3-21_value_iteration.pdf

        # set variable to keep new value that calculated based on state and actions
        new_values = util.Counter() 
         # Loop through all iterations. (100)
        for i in range(0, self.iterations):
            # Keep previous value and use it for calculating with next state possible state
            # new_values = self.values.copy();
           
            # Return list of all states (x,y).
            # ['TERMINAL_STATE', (0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2)]
            all_states = mdp.getStates()
            print all_states
             # For each state, we get all possible actions, skip when action is terminal, no need to calculate.
            for state in all_states:
                print 'current state: ', state
                
                state_actions_values = []
                
                if mdp.isTerminal(state):
                    continue

                
                possible_actions = self.mdp.getPossibleActions(state)
                print 'possible_actions: ', possible_actions
                # For all possible actions which are corresponding to state
                for action in possible_actions:
                    # Go through all actions for current state and calc Q value
                    q_value = self.computeQValueFromValues(state, action)
                    state_actions_values.append(q_value)
                
                new_values[state] = max(state_actions_values)
                      
            self.values = new_values.copy()

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        # Q(s,a) =  Transition probability * ( Reward probability + gamma * value_of_next_state) 
        # Compute Q function for all state action pairs of Q(s, a).
        #  Returns list of (nextState, prob) pairs
        next_state_probs = self.mdp.getTransitionStatesAndProbs(state, action)
        print 'next state prob of action:', action, ':', next_state_probs
        
        q_value = 0;
        for next_state, prob in next_state_probs:
            
            q_value += prob * (self.mdp.getReward(state, action, next_state) + self.discount * self.getValue(next_state))
            print q_value, "=", prob, "* r(", state, ",", action, ",", next_state, ")-->", self.mdp.getReward(state, action, next_state), " + ", self.discount, "*", self.getValue(next_state)
            
        return q_value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        actions = self.mdp.getPossibleActions(state)
        if len(actions) == 0:
            return None
        
        max_value = None;
        optimal_action = None;
        for action in actions:
            temp_value = self.computeQValueFromValues(state, action)
            if max_value == None or temp_value > max_value:
                max_value = temp_value
                optimal_action = action
        return optimal_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
