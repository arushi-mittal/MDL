#!/usr/bin/env python
# coding: utf-8

# In[14]:


#Setting the state variables

import numpy as np
import random

positions = ['C', 'W','E', 'N', 'S']
materials = [0, 1, 2]
arrows = [0, 1, 2, 3]
monster_states = ['D', 'R']
monster_health_values = [0, 25, 50, 75, 100]
ij_actions = ['UP', 'DOWN', 'RIGHT', 'LEFT', 'STAY', 'SHOOT', 'HIT', 'CRAFT', 'GATHER', 'NONE']

stepcost = -5
gamma = 0.999
delta = 0.001

penalty = -40


# In[15]:


#Initializing the state set

position_actions = {"C": ['UP', 'DOWN', 'RIGHT', 'LEFT', 'STAY', 'SHOOT', 'HIT'], 
                    "W": ['RIGHT', 'STAY', 'SHOOT'],
                    "E": ['LEFT', 'STAY', 'SHOOT', 'HIT'],
                    "N": ['DOWN', 'STAY', 'CRAFT'],
                    "S": ['UP', 'STAY', 'GATHER']
                   }
state_set = {}
states = []
# key would be the state, value would be a list containing the best action taken and highest utility IN EVERY ITERATION
# so value will be an array of arrays

for position in positions:
    for material in materials:
        for arrow in arrows:
            for monster_state in monster_states:
                for monster_health in monster_health_values:
                    states.append((position, material, arrow, monster_state, monster_health))
                    state_set[(position, material, arrow, monster_state, monster_health)] = []

#INITIALISE ALL UTILITIES AS ZERO FIRST (for all states)
for state in states:
    state_set[state].append(['NONE', 0])

difference = 10000
stepcost = -5


# In[16]:


def west_r (state, i):
    utility = []
    actions = []
    position = state[0]
    material = state[1]
    arrow = state[2]
    monster_state = state[3]
    monster_health = state[4]
    if(monster_health):
        for action in position_actions['W'] :
            if action == 'RIGHT':
                # i think monster can still attack and change his own state, even if it doesnt affect indiana
                newstate_d = ('C', material, arrow, 'D', monster_health)
                newstate_r = ('C', material, arrow, 'R', monster_health)
                right_prob = 1
                right_reward = 0
                util = 0.5*(stepcost + gamma*state_set[newstate_d][i][1]) + 0.5*(stepcost + gamma*state_set[newstate_r][i][1])
                utility.append(util)
                actions.append(action)
                #utility.append(right_prob * right_reward)
                
            elif action == 'STAY':
                newstate_d = ('W', material, arrow, 'D', monster_health)
                newstate_r = ('W', material, arrow, 'R', monster_health)
                stay_prob = 1
                stay_reward = 0
                util = 0.5*(stepcost + gamma*state_set[newstate_d][i][1]) + 0.5*(stepcost + gamma*state_set[newstate_r][i][1])
                utility.append(util)
                actions.append(action)
                
            elif action == 'SHOOT':
                success_prob = 0.25
                #options of newstate: success, dormant   failure, dormant   success, ready   failure, ready
                if (arrow != 0):
                    #shoot(success_prob, state)
                    newstate_sd = (position, material, arrow-1, 'D', max(monster_health-25, 0))
                    newstate_fd = (position, material, arrow-1, 'D', monster_health)
                    newstate_sr = (position, material, arrow-1, 'R', max(monster_health-25, 0))
                    newstate_fr = (position, material, arrow-1, 'R', monster_health)
                    reward = 0
                    if(monster_health-25 == 0):
                        reward = 50
                    util = 0.25*0.5*(stepcost + reward + gamma*state_set[newstate_sd][i][1]) + 0.75*0.5*(stepcost + gamma*state_set[newstate_fd][i][1]) + 0.25*0.5*(stepcost + reward + gamma*state_set[newstate_sr][i][1]) + 0.75*0.5*(stepcost + gamma*state_set[newstate_fr][i][1])
                    utility.append(util)
                    actions.append(action)
                
    if(len(utility) != 0):
        best_utility = max(utility)
        best_action = actions[utility.index(best_utility)]
    else:
        best_utility = state_set[state][i][1]
        best_action = 'NONE'
        
    #now append to dictionary
    state_set[state].append([best_action, best_utility])
    


# In[17]:


def south_r (state, i):
    utility = []
    actions = []
    position = state[0]
    material = state[1]
    arrow = state[2]
    monster_state = state[3]
    monster_health = state[4]
    if(monster_health):
        for action in position_actions['S'] :
            if action == 'UP':
                #options of newstate: success, dormant   failure, dormant   success, ready   failure, ready
                newstate_sd = ('C', material, arrow, 'D', monster_health)
                newstate_fd = ('E', material, arrow, 'D', monster_health)
                newstate_sr = ('C', material, arrow, 'R', monster_health)
                newstate_fr = ('E', material, arrow, 'R', monster_health)
                up_prob = 0.85 #otherwise teleport to E
                util = 0.85*0.5*(stepcost + gamma*state_set[newstate_sd][i][1]) + 0.15*0.5*(stepcost + gamma*state_set[newstate_fd][i][1]) + 0.85*0.5*(stepcost + gamma*state_set[newstate_sr][i][1]) + 0.15*0.5*(stepcost + gamma*state_set[newstate_fr][i][1])
                utility.append(util)
                actions.append(action)

            elif action == 'STAY':
                newstate_sd = ('S', material, arrow, 'D', monster_health)
                newstate_fd = ('E', material, arrow, 'D', monster_health)
                newstate_sr = ('S', material, arrow, 'R', monster_health)
                newstate_fr = ('E', material, arrow, 'R', monster_health)
                stay_prob = 0.85
                util = 0.85*0.5*(stepcost + gamma*state_set[newstate_sd][i][1]) + 0.15*0.5*(stepcost + gamma*state_set[newstate_fd][i][1]) + 0.85*0.5*(stepcost + gamma*state_set[newstate_sr][i][1]) + 0.15*0.5*(stepcost + gamma*state_set[newstate_fr][i][1])
                utility.append(util)
                actions.append(action)

            elif action == 'GATHER':
                #options of newstate: success, dormant   failure, dormant   success, ready   failure, ready
                new_material = material
                if material < 2:
                    new_material = material + 1
                newstate_sd = (position, new_material, arrow, 'D', monster_health)
                newstate_fd = (position, material, arrow, 'D', monster_health)
                newstate_sr = (position, new_material, arrow, 'R', monster_health)
                newstate_fr = (position, material, arrow, 'R', monster_health)
                gather_prob = 0.75
                util = 0.75*0.5*(stepcost + gamma*state_set[newstate_sd][i][1]) + 0.25*0.5*(stepcost + gamma*state_set[newstate_fd][i][1]) + 0.75*0.5*(stepcost + gamma*state_set[newstate_sr][i][1]) + 0.25*0.5*(stepcost + gamma*state_set[newstate_fr][i][1])
                utility.append(util)
                actions.append(action)
                
    if(len(utility) != 0):
        best_utility = max(utility)
        best_action = actions[utility.index(best_utility)]
    else:
        best_utility = state_set[state][i][1]
        best_action = 'NONE'
    
    #now append to dictionary
    state_set[state].append([best_action, best_utility])


# In[18]:


def north_r (state, i):
    utility = []
    actions = []
    position = state[0]
    material = state[1]
    arrow = state[2]
    monster_state = state[3]
    monster_health = state[4]
    if(monster_health):
        for action in position_actions['N'] :
            if action == 'DOWN':
                #options of newstate: success, dormant   failure, dormant   success, ready   failure, ready
                newstate_sd = ('C', material, arrow, 'D', monster_health)
                newstate_fd = ('E', material, arrow, 'D', monster_health)
                newstate_sr = ('C', material, arrow, 'R', monster_health)
                newstate_fr = ('E', material, arrow, 'R', monster_health)
                down_prob = 0.85 #otherwise teleport to E
                util = 0.85*0.5*(stepcost + gamma*state_set[newstate_sd][i][1]) + 0.15*0.5*(stepcost + gamma*state_set[newstate_fd][i][1]) + 0.85*0.5*(stepcost + gamma*state_set[newstate_sr][i][1]) + 0.15*0.5*(stepcost + gamma*state_set[newstate_fr][i][1])
                utility.append(util)
                actions.append(action)

            elif action == 'STAY':
                newstate_sd = ('N', material, arrow, 'D', monster_health)
                newstate_fd = ('E', material, arrow, 'D', monster_health)
                newstate_sr = ('N', material, arrow, 'R', monster_health)
                newstate_fr = ('E', material, arrow, 'R', monster_health)
                down_prob = 0.85 #otherwise teleport to E
                util = 0.85*0.5*(stepcost + gamma*state_set[newstate_sd][i][1]) + 0.15*0.5*(stepcost + gamma*state_set[newstate_fd][i][1]) + 0.85*0.5*(stepcost + gamma*state_set[newstate_sr][i][1]) + 0.15*0.5*(stepcost + gamma*state_set[newstate_fr][i][1])
                utility.append(util)
                actions.append(action)

            elif action == 'CRAFT' and material > 0:
                p1 = 0.5
                p2 = 0.35
                p3 = 0.15
                newstate_d1 = ('N', material-1, min(arrow+1, 3), 'D', monster_health) 
                newstate_d2 = ('N', material-1, min(arrow+2, 3), 'D', monster_health) 
                newstate_d3 = ('N', material-1, min(arrow+3, 3), 'D', monster_health) 
                newstate_r1 = ('N', material-1, min(arrow+1, 3), 'R', monster_health) 
                newstate_r2 = ('N', material-1, min(arrow+2, 3), 'R', monster_health) 
                newstate_r3 = ('N', material-1, min(arrow+3, 3), 'R', monster_health)
                util = p1*0.5*(stepcost + gamma*state_set[newstate_d1][i][1]) + p2*0.5*(stepcost + gamma*state_set[newstate_d2][i][1]) + p3*0.5*(stepcost + gamma*state_set[newstate_d3][i][1]) + p1*0.5*(stepcost + gamma*state_set[newstate_r1][i][1]) + p2*0.5*(stepcost + gamma*state_set[newstate_r2][i][1]) + p3*0.5*(stepcost + gamma*state_set[newstate_r3][i][1])
                utility.append(util)
                actions.append(action)

    if(len(utility) != 0):
        best_utility = max(utility)
        best_action = actions[utility.index(best_utility)]
    else:
        best_utility = state_set[state][i][1]
        best_action = 'NONE'
        
    #now append to dictionary
    state_set[state].append([best_action, best_utility])


# In[19]:


def east_r (state, i, penalty, attack_state):
    utility = []
    actions = []
    position = state[0]
    material = state[1]
    arrow = state[2]
    monster_state = state[3]
    monster_health = state[4]
    if(monster_health):
        for action in position_actions['E'] :
            if action == 'LEFT':
                #options for newstate: succes, ready   attacked, dormant
                newstate_r = ('C', material, arrow, 'R', monster_health)
                left_prob = 1
                right_reward = 0
                util = 0.5*(stepcost + gamma*state_set[newstate_r][i][1]) + 0.5*(stepcost + penalty + state_set[attack_state][i][1])
                utility.append(util)
                actions.append(action)
                #utility.append(right_prob * right_reward)

            elif action == 'STAY':
                newstate_r = ('E', material, arrow, 'R', monster_health)
                stay_prob = 1
                stay_reward = 0
                util = 0.5*(stepcost + gamma*state_set[newstate_r][i][1]) + 0.5*(stepcost + penalty + gamma*state_set[attack_state][i][1])
                utility.append(util)
                actions.append(action)

            elif action == 'SHOOT':
                success_prob = 0.9
                if (arrow != 0):
                    #shoot(success_prob, state)
                    newstate_sr = (position, material, arrow-1, 'R', max(monster_health-25, 0))
                    newstate_fr = (position, material, arrow-1, 'R', monster_health)
                    reward = 0
                    if(monster_health-25 == 0):
                        reward = 50
                    util = 0.5*(0.9*(stepcost + reward + gamma*state_set[newstate_sr][i][1]) + 0.1*(stepcost + gamma*state_set[newstate_fr][i][1])) + 0.5*(stepcost + penalty + gamma*state_set[attack_state][i][1])
                    actions.append(action)
                    utility.append(util)

            elif action == 'HIT':
                success_prob = 0.2
                #options of newstate: success, ready   failure, ready   attacked, dormant
                newstate_sr = (position, material, arrow, 'R', max(monster_health-50, 0))
                newstate_fr = (position, material, arrow, 'R', monster_health)
                reward = 0
                if(monster_health-50 == 0):
                    reward = 50
                util = 0.5*(0.2*(stepcost + reward + gamma*state_set[newstate_sr][i][1]) + 0.8*(stepcost + gamma*state_set[newstate_fr][i][1])) + 0.5*(stepcost + penalty + gamma*state_set[attack_state][i][1])
                utility.append(util)
                actions.append(action)

    if(len(utility) != 0):
        best_utility = max(utility)
        best_action = actions[utility.index(best_utility)]
    else:
        best_utility = state_set[state][i][1]
        best_action = 'NONE'
        
    #now append to dictionary
    state_set[state].append([best_action, best_utility])
    


# In[20]:


def center_r (state, i, penalty, attack_state) :
    utility = []
    actions = []
    position = state[0]
    material = state[1]
    arrow = state[2]
    monster_state = state[3]
    monster_health = state[4]
    if(monster_health):
        for action in position_actions['C'] :
            if action == 'DOWN':
                #options of newstate: success, ready   failure, ready   attacked, dormant
                newstate_sr = ('S', material, arrow, 'R', monster_health)
                newstate_fr = ('E', material, arrow, 'R', monster_health)
                down_prob = 0.85 #otherwise teleport to E
                util = 0.5*(0.85*(stepcost + gamma*state_set[newstate_sr][i][1]) + 0.15*(stepcost + gamma*state_set[newstate_fr][i][1])) + 0.5*(stepcost + penalty + gamma*state_set[attack_state][i][1])
                utility.append(util)
                actions.append(action)

            elif action == 'UP':
                #options of newstate: success, ready   failure, ready   attacked, dormant
                newstate_sr = ('N', material, arrow, 'R', monster_health)
                newstate_fr = ('E', material, arrow, 'R', monster_health)
                up_prob = 0.85 #otherwise teleport to E
                util = 0.5*(0.85*(stepcost + gamma*state_set[newstate_sr][i][1]) + 0.15*(stepcost + gamma*state_set[newstate_fr][i][1])) + 0.5*(stepcost + penalty + gamma*state_set[attack_state][i][1])
                utility.append(util)
                actions.append(action)
                
            elif action == 'RIGHT':
                #options of newstate: success, ready  attacked, dormant
                newstate_sd = ('E', material, arrow, 'D', monster_health)
                newstate_sr = ('E', material, arrow, 'R', monster_health)
                right_prob = 1 #otherwise teleport to E
                util = 0.5*(stepcost + gamma*state_set[newstate_sr][i][1]) + 0.5*(stepcost + penalty + gamma*state_set[attack_state][i][1])
                utility.append(util)
                actions.append(action)
                
            elif action == 'LEFT':
                newstate_sr = ('W', material, arrow, 'R', monster_health)
                newstate_fr = ('E', material, arrow, 'R', monster_health)
                west_prob = 0.85 #otherwise teleport to E
                util = 0.5*(0.85*(stepcost + gamma*state_set[newstate_sr][i][1]) + 0.15*(stepcost + gamma*state_set[newstate_fr][i][1])) + 0.5*(stepcost + penalty + gamma*state_set[attack_state][i][1])
                utility.append(util)
                actions.append(action)

            elif action == 'STAY':
                newstate_sr = ('C', material, arrow, 'R', monster_health)
                newstate_fr = ('E', material, arrow, 'R', monster_health)
                stay_reward = 0
                util = 0.5*(0.85*(stepcost + gamma*state_set[newstate_sr][i][1]) + 0.15*(stepcost + gamma*state_set[newstate_fr][i][1])) + 0.5*(stepcost + penalty + gamma*state_set[attack_state][i][1])
                utility.append(util)
                actions.append(action)

            elif action == 'SHOOT':
                shoot_prob = 0.5
                if arrow != 0:
                    #new state can be sr, fr, ad
                    newstate_sr = ('C', material, arrow - 1, 'R', max(monster_health - 25, 0))
                    newstate_fr = ('C', material, arrow - 1, 'R', monster_health)
                    reward = 0
                    if monster_health == 25:
                        reward = 50
                    util = 0.5*(shoot_prob*(stepcost + reward + gamma * (state_set[newstate_sr][i][1])) + shoot_prob*(stepcost + gamma * (state_set[newstate_fr][i][1]))) + 0.5*(stepcost + penalty + gamma*state_set[attack_state][i][1])
                    utility.append(util)
                    actions.append(action)
                    
            elif action == 'HIT':
                hit_prob = 0.1
                #new state can be sr, fr, ad
                newstate_sr = ('C', material, arrow, 'R', max(monster_health - 50, 0))
                newstate_fr = ('C', material, arrow, 'R', monster_health)
                reward = 0
                if monster_health == 50:
                    reward = 50
                util = 0.5*(hit_prob*(stepcost + reward + gamma * (state_set[newstate_sr][i][1])) + (1 - hit_prob)*(stepcost + gamma * (state_set[newstate_fr][i][1]))) + 0.5*(stepcost + penalty + gamma*state_set[attack_state][i][1])
                utility.append(util)
                actions.append(action)

    if(len(utility) != 0):
        best_utility = max(utility)
        best_action = actions[utility.index(best_utility)]
    else:
        best_utility = state_set[state][i][1]
        best_action = 'NONE'

    #now append to dictionary
    state_set[state].append([best_action, best_utility])


# In[21]:


def west_d (state, i):
    utility = []
    actions = []
    position = state[0]
    material = state[1]
    arrow = state[2]
    monster_state = state[3]
    monster_health = state[4]
    if monster_health:
        for action in position_actions['W'] :
            if action == 'RIGHT':
                newstate_d = ('C', material, arrow, 'D', monster_health)
                newstate_r = ('C', material, arrow, 'R', monster_health)
                right_prob = 1
                right_reward = 0
                util = 0.8*(stepcost + gamma*state_set[newstate_d][i][1]) + 0.2*(stepcost + gamma*state_set[newstate_r][i][1])
                utility.append(util)
                actions.append(action)
                #utility.append(right_prob * right_reward)

            elif action == 'STAY':
                newstate_d = ('W', material, arrow, 'D', monster_health)
                newstate_r = ('W', material, arrow, 'R', monster_health)
                stay_prob = 1
                stay_reward = 0
                util = 0.8*(stepcost + gamma*state_set[newstate_d][i][1]) + 0.2*(stepcost + gamma*state_set[newstate_r][i][1])
                utility.append(util)
                actions.append(action)

            elif action == 'SHOOT':
                success_prob = 0.25
                #options of newstate: success, dormant   failure, dormant   success, ready   failure, ready
                if (arrow != 0):
                    #shoot(success_prob, state)
                    newstate_sd = (position, material, arrow-1, 'D', max(monster_health-25, 0))
                    newstate_fd = (position, material, arrow-1, 'D', monster_health)
                    newstate_sr = (position, material, arrow-1, 'R', max(monster_health-25, 0))
                    newstate_fr = (position, material, arrow-1, 'R', monster_health)
                    reward = 0
                    if(monster_health-25 == 0):
                        reward = 50
                    util = 0.25*0.8*(stepcost + reward + gamma*state_set[newstate_sd][i][1]) + 0.75*0.8*(stepcost + gamma*state_set[newstate_fd][i][1]) + 0.25*0.2*(stepcost + reward + gamma*state_set[newstate_sr][i][1]) + 0.75*0.2*(stepcost + gamma*state_set[newstate_fr][i][1])
                    utility.append(util)
                    actions.append(action)

    if(len(utility) != 0):
        best_utility = max(utility)
        best_action = actions[utility.index(best_utility)]
    else:
        best_utility = state_set[state][i][1]
        best_action = 'NONE'

    #now append to dictionary
    state_set[state].append([best_action, best_utility])
    


# In[22]:


def south_d (state, i):
    utility = []
    actions = []
    position = state[0]
    material = state[1]
    arrow = state[2]
    monster_state = state[3]
    monster_health = state[4]
    if monster_health:
        for action in position_actions['S'] :
            if action == 'UP':
                #options of newstate: success, dormant   failure, dormant   success, ready   failure, ready
                newstate_sd = ('C', material, arrow, 'D', monster_health)
                newstate_fd = ('E', material, arrow, 'D', monster_health)
                newstate_sr = ('C', material, arrow, 'R', monster_health)
                newstate_fr = ('E', material, arrow, 'R', monster_health)
                up_prob = 0.85 #otherwise teleport to E
                util = 0.85*0.8*(stepcost + gamma*state_set[newstate_sd][i][1]) + 0.15*0.8*(stepcost + gamma*state_set[newstate_fd][i][1]) + 0.85*0.2*(stepcost + gamma*state_set[newstate_sr][i][1]) + 0.15*0.2*(stepcost + gamma*state_set[newstate_fr][i][1])
                utility.append(util)
                actions.append(action)

            elif action == 'STAY':
                newstate_sd = ('S', material, arrow, 'D', monster_health)
                newstate_fd = ('E', material, arrow, 'D', monster_health)
                newstate_sr = ('S', material, arrow, 'R', monster_health)
                newstate_fr = ('E', material, arrow, 'R', monster_health)
                stay_prob = 0.85
                util = 0.85*0.8*(stepcost + gamma*state_set[newstate_sd][i][1]) + 0.15*0.8*(stepcost + gamma*state_set[newstate_fd][i][1]) + 0.85*0.2*(stepcost + gamma*state_set[newstate_sr][i][1]) + 0.15*0.2*(stepcost + gamma*state_set[newstate_fr][i][1])
                utility.append(util)
                actions.append(action)

            elif action == 'GATHER':
                #options of newstate: success, dormant   failure, dormant   success, ready   failure, ready
                new_material = material
                if material < 2:
                    new_material = material + 1
                newstate_sd = (position, new_material, arrow, 'D', monster_health)
                newstate_fd = (position, material, arrow, 'D', monster_health)
                newstate_sr = (position, new_material, arrow, 'R', monster_health)
                newstate_fr = (position, material, arrow, 'R', monster_health)
                gather_prob = 0.75
                util = 0.75*0.8*(stepcost + gamma*state_set[newstate_sd][i][1]) + 0.25*0.8*(stepcost + gamma*state_set[newstate_fd][i][1]) + 0.75*0.2*(stepcost + gamma*state_set[newstate_sr][i][1]) + 0.25*0.2*(stepcost + gamma*state_set[newstate_fr][i][1])
                utility.append(util)
                actions.append(action)

    if(len(utility) != 0):
        best_utility = max(utility)
        best_action = actions[utility.index(best_utility)]
    else:
        best_utility = state_set[state][i][1]
        best_action = 'NONE'

    #now append to dictionary
    state_set[state].append([best_action, best_utility])


# In[23]:


def north_d (state, i):
    utility = []
    actions = []
    position = state[0]
    material = state[1]
    arrow = state[2]
    monster_state = state[3]
    monster_health = state[4]
    if monster_health:
        for action in position_actions['N'] :
            if action == 'DOWN':
                #options of newstate: success, dormant   failure, dormant   success, ready   failure, ready
                newstate_sd = ('C', material, arrow, 'D', monster_health)
                newstate_fd = ('E', material, arrow, 'D', monster_health)
                newstate_sr = ('C', material, arrow, 'R', monster_health)
                newstate_fr = ('E', material, arrow, 'R', monster_health)
                down_prob = 0.85 #otherwise teleport to E
                util = 0.85*0.8*(stepcost + gamma*state_set[newstate_sd][i][1]) + 0.15*0.8*(stepcost + gamma*state_set[newstate_fd][i][1]) + 0.85*0.2*(stepcost + gamma*state_set[newstate_sr][i][1]) + 0.15*0.2*(stepcost + gamma*state_set[newstate_fr][i][1])
                utility.append(util)
                actions.append(action)

            elif action == 'STAY':
                newstate_sd = ('N', material, arrow, 'D', monster_health)
                newstate_fd = ('E', material, arrow, 'D', monster_health)
                newstate_sr = ('N', material, arrow, 'R', monster_health)
                newstate_fr = ('E', material, arrow, 'R', monster_health)
                down_prob = 0.85 #otherwise teleport to E
                util = 0.85*0.8*(stepcost + gamma*state_set[newstate_sd][i][1]) + 0.15*0.8*(stepcost + gamma*state_set[newstate_fd][i][1]) + 0.85*0.2*(stepcost + gamma*state_set[newstate_sr][i][1]) + 0.15*0.2*(stepcost + gamma*state_set[newstate_fr][i][1])
                utility.append(util)
                actions.append(action)

            elif action == 'CRAFT' and material > 0:
                p1 = 0.5
                p2 = 0.35
                p3 = 0.15
                newstate_d1 = ('N', material-1, min(arrow+1, 3), 'D', monster_health) 
                newstate_d2 = ('N', material-1, min(arrow+2, 3), 'D', monster_health) 
                newstate_d3 = ('N', material-1, min(arrow+3, 3), 'D', monster_health) 
                newstate_r1 = ('N', material-1, min(arrow+1, 3), 'R', monster_health) 
                newstate_r2 = ('N', material-1, min(arrow+2, 3), 'R', monster_health) 
                newstate_r3 = ('N', material-1, min(arrow+3, 3), 'R', monster_health)
                util = p1*0.8*(stepcost + gamma*state_set[newstate_d1][i][1]) + p2*0.8*(stepcost + gamma*state_set[newstate_d2][i][1]) + p3*0.8*(stepcost + gamma*state_set[newstate_d3][i][1]) + p1*0.2*(stepcost + gamma*state_set[newstate_r1][i][1]) + p2*0.2*(stepcost + gamma*state_set[newstate_r2][i][1]) + p3*0.2*(stepcost + gamma*state_set[newstate_r3][i][1])
                utility.append(util)
                actions.append(action)

    if(len(utility) != 0):
        best_utility = max(utility)
        best_action = actions[utility.index(best_utility)]
    else:
        best_utility = state_set[state][i][1]
        best_action = 'NONE'

    #now append to dictionary
    state_set[state].append([best_action, best_utility])


# In[24]:


def east_d (state, i):
    utility = []
    actions = []
    position = state[0]
    material = state[1]
    arrow = state[2]
    monster_state = state[3]
    monster_health = state[4]
    if monster_health:
        for action in position_actions['E'] :
            if action == 'LEFT':
                newstate_d = ('C', material, arrow, 'D', monster_health)
                newstate_r = ('C', material, arrow, 'R', monster_health)
                left_prob = 1
                right_reward = 0
                util = 0.8*(stepcost + gamma*state_set[newstate_d][i][1]) + 0.2*(stepcost + gamma*state_set[newstate_r][i][1])
                utility.append(util)
                actions.append(action)
                #utility.append(right_prob * right_reward)

            elif action == 'STAY':
                newstate_d = ('E', material, arrow, 'D', monster_health)
                newstate_r = ('E', material, arrow, 'R', monster_health)
                stay_prob = 1
                stay_reward = 0
                util = 0.8*(stepcost + gamma*state_set[newstate_d][i][1]) + 0.2*(stepcost + gamma*state_set[newstate_r][i][1])
                utility.append(util)
                actions.append(action)

            elif action == 'SHOOT':
                success_prob = 0.9
                #options of newstate: success, dormant   failure, dormant   success, ready   failure, ready
                if (arrow != 0):
                    #shoot(success_prob, state)
                    newstate_sd = (position, material, arrow-1, 'D', max(monster_health-25, 0))
                    newstate_fd = (position, material, arrow-1, 'D', monster_health)
                    newstate_sr = (position, material, arrow-1, 'R', max(monster_health-25, 0))
                    newstate_fr = (position, material, arrow-1, 'R', monster_health)
                    reward = 0
                    if(monster_health-25 == 0):
                        reward = 50
                    util = 0.9*0.8*(stepcost + reward + gamma*state_set[newstate_sd][i][1]) + 0.1*0.8*(stepcost + gamma*state_set[newstate_fd][i][1]) + 0.9*0.2*(stepcost + reward + gamma*state_set[newstate_sr][i][1]) + 0.1*0.2*(stepcost + gamma*state_set[newstate_fr][i][1])
                    utility.append(util)
                    actions.append(action)

            elif action == 'HIT':
                success_prob = 0.2
                #options of newstate: success, dormant   failure, dormant   success, ready   failure, ready
                newstate_sd = (position, material, arrow, 'D', max(0, monster_health-50))
                newstate_fd = (position, material, arrow, 'D', monster_health)
                newstate_sr = (position, material, arrow, 'R', max(monster_health-50, 0))
                newstate_fr = (position, material, arrow, 'R', monster_health)
                reward = 0
                if(monster_health-50 == 0):
                    reward = 50
                util = 0.2*0.8*(stepcost + reward + gamma*state_set[newstate_sd][i][1]) + 0.8*0.8*(stepcost + gamma*state_set[newstate_fd][i][1]) + 0.2*0.2*(stepcost + reward + gamma*state_set[newstate_sr][i][1]) + 0.8*0.2*(stepcost + gamma*state_set[newstate_fr][i][1])
                utility.append(util)
                actions.append(action)
                
    if(len(utility) != 0):
        best_utility = max(utility)
        best_action = actions[utility.index(best_utility)]
    else:
        best_utility = state_set[state][i][1]
        best_action = 'NONE'

    #now append to dictionary
    state_set[state].append([best_action, best_utility])
    


# In[25]:


def center_d (state, i) :
    utility = []
    actions = []
    position = state[0]
    material = state[1]
    arrow = state[2]
    monster_state = state[3]
    monster_health = state[4]
    if(monster_health):
        for action in position_actions['C'] :
            if action == 'DOWN':
                #options of newstate: success, dormant   failure, dormant   success, ready   failure, ready
                newstate_sd = ('S', material, arrow, 'D', monster_health)
                newstate_fd = ('E', material, arrow, 'D', monster_health)
                newstate_sr = ('S', material, arrow, 'R', monster_health)
                newstate_fr = ('E', material, arrow, 'R', monster_health)
                down_prob = 0.85 #otherwise teleport to E
                util = 0.85*0.8*(stepcost + gamma*state_set[newstate_sd][i][1]) + 0.15*0.8*(stepcost + gamma*state_set[newstate_fd][i][1]) + 0.85*0.2*(stepcost + gamma*state_set[newstate_sr][i][1]) + 0.15*0.2*(stepcost + gamma*state_set[newstate_fr][i][1])
                utility.append(util)
                actions.append(action)

            elif action == 'UP':
                #options of newstate: success, dormant   failure, dormant   success, ready   failure, ready
                newstate_sd = ('N', material, arrow, 'D', monster_health)
                newstate_fd = ('E', material, arrow, 'D', monster_health)
                newstate_sr = ('N', material, arrow, 'R', monster_health)
                newstate_fr = ('E', material, arrow, 'R', monster_health)
                up_prob = 0.85 #otherwise teleport to E
                util = 0.85*0.8*(stepcost + gamma*state_set[newstate_sd][i][1]) + 0.15*0.8*(stepcost + gamma*state_set[newstate_fd][i][1]) + 0.85*0.2*(stepcost + gamma*state_set[newstate_sr][i][1]) + 0.15*0.2*(stepcost + gamma*state_set[newstate_fr][i][1])
                utility.append(util)
                actions.append(action)
                
            elif action == 'RIGHT':
                #options of newstate: success, dormant    success, ready
                newstate_sd = ('E', material, arrow, 'D', monster_health)
                newstate_sr = ('E', material, arrow, 'R', monster_health)
                right_prob = 1 #otherwise teleport to E
                util = 0.8*(stepcost + gamma*state_set[newstate_sd][i][1]) + 0.2*(stepcost + gamma*state_set[newstate_sr][i][1])
                utility.append(util)
                actions.append(action)
                
            elif action == 'LEFT':
                #options of newstate: success, dormant   failure, dormant   success, ready   failure, ready
                newstate_sd = ('W', material, arrow, 'D', monster_health)
                newstate_fd = ('E', material, arrow, 'D', monster_health)
                newstate_sr = ('W', material, arrow, 'R', monster_health)
                newstate_fr = ('E', material, arrow, 'R', monster_health)
                west_prob = 0.85 #otherwise teleport to E
                util = 0.85*0.8*(stepcost + gamma*state_set[newstate_sd][i][1]) + 0.15*0.8*(stepcost + gamma*state_set[newstate_fd][i][1]) + 0.85*0.2*(stepcost + gamma*state_set[newstate_sr][i][1]) + 0.15*0.2*(stepcost + gamma*state_set[newstate_fr][i][1])
                utility.append(util)
                actions.append(action)

            elif action == 'STAY':
                #options of newstate: success, dormant   failure, dormant   success, ready   failure, ready
                newstate_sd = ('C', material, arrow, 'D', monster_health)
                newstate_fd = ('E', material, arrow, 'D', monster_health)
                newstate_sr = ('C', material, arrow, 'R', monster_health)
                newstate_fr = ('E', material, arrow, 'R', monster_health)
                stay_reward = 0
                util = 0.85*0.8*(stepcost + gamma*state_set[newstate_sd][i][1]) + 0.85*0.2*(stepcost + gamma*state_set[newstate_sr][i][1]) + 0.15*0.8*(stepcost + gamma*state_set[newstate_fd][i][1]) + 0.15*0.2*(stepcost + gamma*state_set[newstate_fr][i][1])
                utility.append(util)
                actions.append(action)

            elif action == 'SHOOT':
                shoot_prob = 0.5
                if arrow > 0:
                    #new state can be sd, sr, fd, fr
                    newstate_sd = ('C', material, arrow - 1, 'D', max(monster_health - 25, 0))
                    newstate_sr = ('C', material, arrow - 1, 'R', max(monster_health - 25, 0))
                    newstate_fd = ('C', material, arrow - 1, 'D', monster_health)
                    newstate_fr = ('C', material, arrow - 1, 'R', monster_health)
                    reward = 0
                    if monster_health == 25:
                        reward = 50
                    util = 0.8*shoot_prob*(stepcost + reward + gamma*state_set[newstate_sd][i][1]) + 0.8*shoot_prob*(stepcost + gamma*state_set[newstate_fd][i][1]) + 0.2*shoot_prob*(stepcost + reward + gamma * (state_set[newstate_sr][i][1])) + 0.2*shoot_prob*(stepcost + gamma * (state_set[newstate_fr][i][1]))
                    utility.append(util)
                    actions.append(action)

            elif action == 'HIT':
                hit_prob = 0.1
                #new state can be sd, sr, fd, fr
                newstate_sd = ('C', material, arrow, 'D', max(monster_health - 50, 0))
                newstate_sr = ('C', material, arrow, 'R', max(monster_health - 50, 0))
                newstate_fd = ('C', material, arrow, 'D', monster_health)
                newstate_fr = ('C', material, arrow, 'R', monster_health)

                reward = 0
                if monster_health == 50:
                    reward = 50
                util = 0.8*hit_prob*(stepcost + reward + gamma*state_set[newstate_sd][i][1]) + 0.8*(1 - hit_prob)*(stepcost + gamma*state_set[newstate_fd][i][1]) + 0.2*hit_prob*(stepcost + reward + gamma * (state_set[newstate_sr][i][1])) + 0.2*(1 - hit_prob)*(stepcost + gamma * (state_set[newstate_fr][i][1]))
                utility.append(util)
                actions.append(action)

    if(len(utility) != 0):
        best_utility = max(utility)
        best_action = actions[utility.index(best_utility)]
    else:
        best_utility = state_set[state][i][1]
        best_action = 'NONE'

    #now append to dictionary
    state_set[state].append([best_action, best_utility])


# In[26]:


i = 0


f = open('part_2_trace.txt', 'w')
while difference > delta:
    f.write("iteration=" + str(i) + '\n')
    for state in states:
#         print(state)
        position = state[0]
        monster_state = state[3]
        monster_health = state[4]
        #if monster_health == 0:
         #   print("Monster is dead :( (but shouldn't we print happy face xD)")
          #  break
        
        attack_state = (position, material, 0, 'D', min(monster_health + 25, 100))
        if monster_state == 'D':
            if position == 'C':
                center_d(state, i)
            elif position == 'W':
                west_d(state, i)
            elif position == 'E':
                east_d(state, i)
            elif position == 'N':
                north_d(state, i)
            elif position == 'S':
                south_d(state, i)
        else:
            if position == 'C':
                center_r(state, i, penalty, attack_state)
            elif position == 'W':
                west_r(state, i)
            elif position == 'E':
                east_r(state, i, penalty, attack_state)
            elif position == 'N':
                north_r(state, i)
            elif position == 'S':
                south_r(state, i)
        
    #calculate difference variable
    arr = np.array(list(state_set.values()))
    difference = np.max(abs(arr[:, i+1, 1].astype(float) - arr[:, i, 1].astype(float)))
#     print(difference)
    
    for state in state_set:
       f.write(str(state) + ':' + str(state_set[state][-1][0]) + '=' + str(round(state_set[state][-1][1], 3)) + '\n')

    
    
    i = i + 1
f.close()       


# In[ ]:




