# analysis.py
# -----------
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

######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.


def question2():
    answerDiscount = 0.9
    # answerNoise = 0.2
    # the value started to change from nagative to positive value at 0.09
    # then we try to reduce noise value and found that at 0.01, it makes all cells green.
    answerNoise = 0.01
    return answerDiscount, answerNoise


def question3a():
    answerDiscount = 0.9
    answerNoise = 0.1
    answerLivingReward = -3  # reward
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


def question3b():
    #  A discount factor closer to zero on the other hand indicates 
    # that only rewards in the immediate future are being considered
    answerDiscount = 0.2
    answerNoise = 0.2
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


def question3c():
    # Prefer the distant exit (+10), risking the cliff (-10)
    # discount factor should be high in order not to select intermediate reward.
    # living reward, no need to be high, we don't care
    # noise is low
    answerDiscount = 0.9
    answerNoise = 0.01
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


def question3d():
    # Prefer the distant exit (+10), avoiding the cliff (-10)
    # exit at +10: discount factor should be high in order not to select intermediate reward.
    # avoid cliff, increase noise
    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


def question3e():
    # Avoid both exits and the cliff (so an episode should never terminate)
    answerDiscount = 0.9
    answerNoise = 0.9
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


def question6():
    # Is there an epsilon and a learning rate 
    # for which it is highly likely (greater than 99%) 
    # that the optimal policy will be learned after 50 iterations?
    
    # greedy method ( epsilon = 0 )
    # hen we are always selecting the highest q value among the all the q values for a specific state.
    answerEpsilon = None
    # Learning rate is how big you take a leap in finding optimal policy. 
    # In the terms of simple QLearning it's how much you are updating the Q value with each step.
    answerLearningRate = None
    
    # learning rate is associated with how big you take a leap 
    # and epsilon is associated with how random you take an action.
    # return answerEpsilon, answerLearningRate
    # If not possible, return 'NOT POSSIBLE'
    return 'NOT POSSIBLE'


if __name__ == '__main__':
    print 'Answers to analysis questions:'
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print '  Question %s:\t%s' % (q, str(response))
