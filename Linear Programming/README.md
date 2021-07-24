# **MDL Assignnment 2 Part 2**

## **Arushi Mittal (2019101120), Meghna Mishra (2019111030)**

### ***Generation of the Action Matrix***

The action matrix is a matrix used to store the permissible actions from a given state and the probability of entering that state when that action is taken. The rows consist of all the possible states and the columns are the state action pairs, representing each action and the valid actions possible from it. 

Matrix Dimensions: `600 x 1936`

We had previously initialized a list `states` to store all the states possible during the duration of the game. We used the values from this list as the keys for a dictionary entitles `state_action_pairs` which stores a list containing all possible actions, their respective probabilities and the corresponding next state. This is used in order to populate the matrix later. Additionally, in a list named `next_state_actions` we stored the names of all the actions possible from all given states, in addition to the starting indices for the actions of each particular state. This was used in order to determine the columns that would need to be altered. After this, all we had to do was use the state as an identifier for the list of actions, probabilities and next states. The action matrix `A` was indexed using `i` and `k`, two variables to denote the row and column. For each index, the required rows were populated with the probabilities, and the `next state` was filled with the negative of that value, since we are calculating the probability of leaving that state.


### ***Finding the Policy***

We used the `cvpxy` Python library in order to determine the policy. We used the `action matrix` and created a variable `x`, with dimensions `1936 x 1`. The constraints we gave were that the product of the `action matrix` and `x` had to be equal to `alpha`. In this case, `alpha` is another vector used to store information about the start state. It was 0 at all indices except that of the start state, which in this case is `(C, 2, 3, R, 100)`. Another constraint was that `x` was always greater than or equal to 0. Using these constraints, we also mentioned that the objective was to maximize the product of the `reward matrix` and `x`. The reward matrix stores the rewards at each state, and the intention is to complete the game with the highest reward possible. We used the `matmul()` function from the cvpxy library in order to multiply the matrices.


### ***Multiple Policies***

Yes, there can be multiple policies. Changing the probabilities of various actions, changing the step cost, rewards and penalties would impact the policy. Changing rewards would obviously affect the `reward matrix` leading to a policy that attempts to get to states with higher rewards in order to maximize the reward matrix and x product. Additionally, changing probabilities would change the `action matrix` leading to a different set of policies being used in order to accomodate `alpha` being the product of `action matrix` and `x`. Changing the `start state` would definitely change the policy because the steps from a particular state would differ depending on the ending state. Additionally, if the terminal condition was changed, this would impact the policy as well.
